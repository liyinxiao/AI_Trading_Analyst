from pydantic import BaseModel
import pandas as pd
import numpy as np


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
        prices_df = PriceResponse.prices_to_df(self.prices)
        # Date
        date = pd.to_datetime(prices_df.iloc[-1]["time"]).strftime("%Y-%m-%d")

        # Calculate EMAs for multiple timeframes
        ema_8 = PriceResponse.calculate_ema(prices_df, 8)
        ema_21 = PriceResponse.calculate_ema(prices_df, 21)
        ema_55 = PriceResponse.calculate_ema(prices_df, 55)

        # Calculate ADX for trend strength
        adx = PriceResponse.calculate_adx(prices_df, 14)

        # Calculate Bollinger Bands
        bb_upper, bb_lower = PriceResponse.calculate_bollinger_bands(prices_df)

        # Calculate RSI with multiple timeframes
        rsi_14 = PriceResponse.calculate_rsi(prices_df, 14)
        rsi_28 = PriceResponse.calculate_rsi(prices_df, 28)

        prompt = f"""
### Key Stock Statistics
Date: {prices_df.iloc[-1]['ds']}
Ticker: {self.ticker}
Previous Close: {prices_df.iloc[-2]['close']}
Open: {prices_df.iloc[-1]['open']}
Close: {prices_df.iloc[-1]['close']}
High: {prices_df.iloc[-1]['high']}
Low: {prices_df.iloc[-1]['low']}
Volume: {prices_df.iloc[-1]['volume']}

### Technical Indicators
8-day EMA: {round(ema_8.iloc[-1], 2)}
21-day EMA: {round(ema_21.iloc[-1], 2)}
55-day EMA: {round(ema_55.iloc[-1], 2)}
ADX: {round(adx["adx"].iloc[-1], 2)} 
+DI: {round(adx["+di"].iloc[-1], 2)}
-DI: {round(adx["-di"].iloc[-1], 2)}
Bollinger Bands: upper band = {round(bb_upper.iloc[-1], 2)}, lower band = {round(bb_lower.iloc[-1], 2)}
14-day RSI: {round(rsi_14.iloc[-1], 2)}
28-day RSI: {round(rsi_28.iloc[-1], 2)}

"""
        return prompt

    @staticmethod
    def prices_to_df(prices: list[Price]) -> pd.DataFrame:
        """Convert prices to a DataFrame."""
        df = pd.DataFrame([p.model_dump() for p in prices])
        df["Date"] = pd.to_datetime(df["time"])
        df["ds"] = [x.strftime("%Y-%m-%d") for x in df["Date"]]
        df.set_index("Date", inplace=True)
        numeric_cols = ["open", "close", "high", "low", "volume"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df.sort_index(inplace=True)
        return df

    @staticmethod
    def calculate_ema(df: pd.DataFrame, window: int) -> pd.Series:
        """
        Calculate Exponential Moving Average

        Args:
            df: DataFrame with price data
            window: EMA period

        Returns:
            pd.Series: EMA values
        """
        return df["close"].ewm(span=window, adjust=False).mean()

    @staticmethod
    def calculate_rsi(prices_df: pd.DataFrame, period: int = 14) -> pd.Series:
        delta = prices_df["close"].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def calculate_bollinger_bands(
        prices_df: pd.DataFrame, window: int = 20
    ) -> tuple[pd.Series, pd.Series]:
        sma = prices_df["close"].rolling(window).mean()
        std_dev = prices_df["close"].rolling(window).std()
        upper_band = sma + (std_dev * 2)
        lower_band = sma - (std_dev * 2)
        return upper_band, lower_band

    @staticmethod
    def calculate_adx(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        Calculate Average Directional Index (ADX)

        Args:
            df: DataFrame with OHLC data
            period: Period for calculations

        Returns:
            DataFrame with ADX values
        """
        # Calculate True Range
        df["high_low"] = df["high"] - df["low"]
        df["high_close"] = abs(df["high"] - df["close"].shift())
        df["low_close"] = abs(df["low"] - df["close"].shift())
        df["tr"] = df[["high_low", "high_close", "low_close"]].max(axis=1)

        # Calculate Directional Movement
        df["up_move"] = df["high"] - df["high"].shift()
        df["down_move"] = df["low"].shift() - df["low"]

        df["plus_dm"] = np.where(
            (df["up_move"] > df["down_move"]) & (df["up_move"] > 0), df["up_move"], 0
        )
        df["minus_dm"] = np.where(
            (df["down_move"] > df["up_move"]) & (df["down_move"] > 0),
            df["down_move"],
            0,
        )

        # Calculate ADX
        df["+di"] = 100 * (
            df["plus_dm"].ewm(span=period).mean() / df["tr"].ewm(span=period).mean()
        )
        df["-di"] = 100 * (
            df["minus_dm"].ewm(span=period).mean() / df["tr"].ewm(span=period).mean()
        )
        df["dx"] = 100 * abs(df["+di"] - df["-di"]) / (df["+di"] + df["-di"])
        df["adx"] = df["dx"].ewm(span=period).mean()

        return df[["adx", "+di", "-di"]]


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
