from pydantic import BaseModel
import pandas as pd
import numpy as np
from ta.trend import ADXIndicator
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands


class Price(BaseModel):
    open: float
    close: float
    high: float
    low: float
    volume: int
    time: str


class PriceResponse(BaseModel):
    ticker: str
    prices: list[Price]

    def create_prompt(self) -> str:
        def format_volume(volume):
            if volume >= 1_000_000:
                return f"{volume // 1_000_000}M"
            elif volume >= 1_000:
                return f"{volume // 1_000}K"
            else:
                return str(volume)

        prices_df = pd.DataFrame([p.model_dump() for p in self.prices])
        prices_df["date"] = pd.to_datetime(prices_df["time"])
        prices_df.set_index("date", inplace=True)
        numeric_cols = ["open", "close", "high", "low", "volume"]
        for col in numeric_cols:
            prices_df[col] = pd.to_numeric(prices_df[col], errors="coerce")
        prices_df.sort_index(inplace=True)
        print(prices_df)

        # Compute Moving Averages
        ma_20 = prices_df["close"].rolling(window=20).mean()
        ma_50 = prices_df["close"].rolling(window=50).mean()

        # Z-score for mean reversion (50-day mean)
        std_50 = prices_df["close"].rolling(window=50).std()
        z_score = (prices_df["close"] - ma_50) / std_50

        # Calculate Bollinger Bands
        bb = BollingerBands(close=prices_df["close"], window=20, window_dev=2)
        bb_upper = bb.bollinger_hband()
        bb_lower = bb.bollinger_lband()
        price_vs_bb = (prices_df["close"].iloc[-1] - bb_lower.iloc[-1]) / (
            bb_upper.iloc[-1] - bb_lower.iloc[-1]
        )

        # Calculate ADX for trend strength
        adx = ADXIndicator(
            high=prices_df["high"],
            low=prices_df["low"],
            close=prices_df["close"],
            window=14,
        )

        # Calculate RSI
        rsi_14 = RSIIndicator(close=prices_df["close"], window=14)
        rsi_28 = RSIIndicator(close=prices_df["close"], window=28)

        # Price momentum
        returns = prices_df["close"].pct_change()
        mom_1m = returns.rolling(21).sum()
        mom_3m = returns.sum()

        # Volume momentum
        volume_ma = prices_df["volume"].rolling(21).mean()
        volume_momentum = prices_df["volume"] / volume_ma

        prompt = f"""
### Key Statistics
Date: {pd.to_datetime(prices_df.iloc[-1]["time"]).strftime("%Y-%m-%d")}
Previous Close: {prices_df.iloc[-2]['close']}
Open: {prices_df.iloc[-1]['open']}
Close: {prices_df.iloc[-1]['close']}
High: {prices_df.iloc[-1]['high']}
Low: {prices_df.iloc[-1]['low']}
Volume: {format_volume(prices_df.iloc[-1]['volume'])}
Average Volume (3M): {format_volume(prices_df["volume"].mean())}

### Technical Indicators
Trend Indicators
- 20-day Moving Average: {round(ma_20.iloc[-1], 2)}
- 50-day Moving Average: {round(ma_50.iloc[-1], 2)}
- ADX (Average Directional Index): {round(adx.adx().iloc[-1], 2)} 
- +DI: {round(adx.adx_pos().iloc[-1], 2)}
- -DI: {round(adx.adx_neg().iloc[-1], 2)}

Mean Reversion Indicators
- Bollinger Bands (20-day)
  - Upper band = {round(bb_upper.iloc[-1], 2)}
  - Lower band = {round(bb_lower.iloc[-1], 2)}
  - Current price position within bands (0 = lower, 1 = upper): {round(price_vs_bb, 2)}
- Z-score (50-day): {round(z_score.iloc[-1], 2)}

Momentum Indicators
- 14-day RSI: {round(rsi_14.rsi().iloc[-1], 2)}
- 28-day RSI: {round(rsi_28.rsi().iloc[-1], 2)}
- 1-month return: {round(mom_1m.iloc[-1] * 100, 2)}%
- 3-month return: {round(mom_3m * 100, 2)}%
- Volume Momentum (current vs 21-day average): {round(volume_momentum.iloc[-1], 2)}

"""
        return prompt


class InsiderTrade(BaseModel):
    ticker: str
    issuer: str | None
    name: str | None
    title: str | None
    is_board_director: bool | None
    transaction_date: str | None
    transaction_shares: float | None
    transaction_price_per_share: float | None
    transaction_value: float | None
    shares_owned_before_transaction: float | None
    shares_owned_after_transaction: float | None
    security_title: str | None
    filing_date: str


class InsiderTradeResponse(BaseModel):
    insider_trades: list[InsiderTrade]

    def create_prompt(self) -> str:
        insider_trades = [
            x
            for x in self.insider_trades
            if x.transaction_shares != 0.0
            or x.shares_owned_before_transaction != x.shares_owned_after_transaction
        ]

        if not insider_trades:
            return "No insider trades available from past 45 days."

        prompt_lines = ["### Insider Trades from Past 60 days"]
        i = 0
        for trade in insider_trades:
            i += 1
            lines = [
                f"Insider Trade #{i} of {trade.ticker}",
                f"- Issuer: {trade.issuer}" if trade.issuer else None,
                f"- Name: {trade.name}" if trade.name else None,
                f"- Title: {trade.title}" if trade.title else None,
                (
                    f"- Board Director: {trade.is_board_director}"
                    if trade.is_board_director is not None
                    else None
                ),
                (
                    f"- Transaction Date: {trade.transaction_date}"
                    if trade.transaction_date
                    else None
                ),
                (
                    f"- Shares Traded: {trade.transaction_shares}"
                    if trade.transaction_shares is not None
                    else None
                ),
                (
                    f"- Price per Share: ${trade.transaction_price_per_share}"
                    if trade.transaction_price_per_share is not None
                    else None
                ),
                (
                    f"- Transaction Value: ${trade.transaction_value}"
                    if trade.transaction_value is not None
                    else None
                ),
                (
                    f"- Shares Before: {trade.shares_owned_before_transaction}"
                    if trade.shares_owned_before_transaction is not None
                    else None
                ),
                (
                    f"- Shares After: {trade.shares_owned_after_transaction}"
                    if trade.shares_owned_after_transaction is not None
                    else None
                ),
                (
                    f"- Security Title: {trade.security_title}"
                    if trade.security_title
                    else None
                ),
                f"- Filing Date: {trade.filing_date}",
            ]
            # Filter out None and join lines
            trade_block = "\n".join(line for line in lines if line)
            prompt_lines.append(trade_block)

        return "\n".join(prompt_lines)
