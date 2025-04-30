from pydantic import BaseModel
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.volume import OnBalanceVolumeIndicator
from ta import add_all_ta_features
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


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
            sign = 1 if volume > 0 else -1
            volume = abs(volume)
            if volume >= 1_000_000_000:
                return f"{sign * volume // 1_000_000_000}B"
            if volume >= 1_000_000:
                return f"{sign * volume // 1_000_000}M"
            elif volume >= 1_000:
                return f"{sign * volume // 1_000}K"
            else:
                return str(sign * volume)

        prices_df = pd.DataFrame([p.model_dump() for p in self.prices])
        prices_df["date"] = pd.to_datetime(prices_df["time"])
        prices_df.set_index("date", inplace=True)
        numeric_cols = ["open", "close", "high", "low", "volume"]
        for col in numeric_cols:
            prices_df[col] = pd.to_numeric(prices_df[col], errors="coerce")
        prices_df.sort_index(inplace=True)

        df_ta = add_all_ta_features(
            prices_df.copy(),
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            fillna=True,
        )

        latest = df_ta.iloc[-1]
        close_price = latest["close"]

        # ========== TREND INDICATORS ==========
        trend = f"""Trend Indicators
- SMA (20-day): {latest['trend_sma_fast']:.2f}
- SMA (50-day): {latest['trend_sma_slow']:.2f}
- EMA (20-day): {latest['trend_ema_fast']:.2f}
- EMA (50-day): {latest['trend_ema_slow']:.2f}
- MACD: {latest['trend_macd']:.2f}, Signal: {latest['trend_macd_signal']:.2f}, Diff: {latest['trend_macd_diff']:.2f}
- ADX (Average Directional Index): {latest['trend_adx']:.2f}
  - +DI: {latest['trend_adx_pos']:.2f}
  - -DI: {latest['trend_adx_neg']:.2f}
- CCI (Commodity Channel Index): {latest['trend_cci']:.2f}
- DPO (Detrended Price Oscillator): {latest['trend_dpo']:.2f}
- Vortex Indicator:
  - VI+ : {latest['trend_vortex_ind_pos']:.2f}
  - VI- : {latest['trend_vortex_ind_neg']:.2f}
- Ichimoku:
  - Conversion Line (Tenkan-sen): {latest['trend_ichimoku_conv']:.2f}
  - Base Line (Kijun-sen): {latest['trend_ichimoku_base']:.2f}
- KST Oscillator: {latest['trend_kst']:.2f}
  - Signal: {latest['trend_kst_sig']:.2f}
"""

        # ========== MOMENTUM INDICATORS ==========
        rsi_28 = RSIIndicator(close=prices_df["close"], window=28)
        momentum = f"""Momentum Indicators
- RSI (14-day): {latest['momentum_rsi']:.1f}
- RSI (28-day): {round(rsi_28.rsi().iloc[-1], 1)}
- Stoch RSI:
  - Fast K: {latest['momentum_stoch_rsi_k']:.2f}
  - Fast D: {latest['momentum_stoch_rsi_d']:.2f}
- TSI (True Strength Index): {latest['momentum_tsi']:.1f}
- ULTOSC (Ultimate Oscillator): {latest['momentum_uo']:.1f}
- ROC (Rate of Change): {latest['momentum_roc']:.1f}
- KAMA (Kaufman's Adaptive Moving Average): {latest['momentum_kama']:.1f}
"""

        # ========== VOLATILITY INDICATORS ==========
        bb_upper = latest["volatility_bbm"] + latest["volatility_bbh"]
        bb_lower = latest["volatility_bbm"] - latest["volatility_bbl"]
        bb_position = (close_price - bb_lower) / (bb_upper - bb_lower)
        bb_position = np.clip(bb_position, 0, 1)

        volatility = f"""Volatility Indicators
- Bollinger Bands:
  - Middle: {latest['volatility_bbm']:.1f}
  - Upper: {bb_upper:.1f}
  - Lower: {bb_lower:.1f}
  - Position within band: {bb_position:.2f}
- ATR (Average True Range): {latest['volatility_atr']:.1f}
- Donchian Channel:
  - Upper Band: {latest['volatility_dch'] + latest['volatility_dcl']:.1f}
  - Lower Band: {latest['volatility_dch'] - latest['volatility_dcl']:.1f}
"""

        # ========== VOLUME INDICATORS ==========
        obv = OnBalanceVolumeIndicator(
            close=prices_df["close"], volume=prices_df["volume"]
        ).on_balance_volume()
        obv_now = obv.iloc[-1]
        obv_ma10 = obv.rolling(10).mean().iloc[-1]
        obv_slope = np.polyfit(range(10), obv[-10:], 1)[0]
        price_slope = np.polyfit(range(10), prices_df["close"].iloc[-10:], 1)[0]
        obv_trend = "rising" if obv_slope > 0 else "falling"
        price_trend = "rising" if price_slope > 0 else "falling"

        volume = f"""Volume Indicators
- MFI (Money Flow Index): {latest['volume_mfi']:.1f}
- On-Balance Volume: {format_volume(obv_now)}
  - 10-day Trend: OBV is {obv_trend}, while price is {price_trend}.
  - OBV vs 10-day MA: {'above' if obv_now > obv_ma10 else 'below'}
- Chaikin Money Flow (CMF): {latest['volume_cmf']:.2f}
- Ease of Movement (EoM): {latest['volume_em']:.1f}
- Force Index: {format_volume(latest['volume_fi'])}
- Volume Price Trend (VPT): {format_volume(latest['volume_vpt'])}
"""

        # Returns
        return_1month = (
            (prices_df["close"].iloc[-1] / prices_df["close"].iloc[-21] - 1) * 100
            if len(prices_df) >= 21
            else np.nan
        )
        return_3month = (
            prices_df["close"].iloc[-1] / prices_df["close"].iloc[0] - 1
        ) * 100

        return f"""
### Key Statistics
Date: {pd.to_datetime(prices_df.iloc[-1]["time"]).strftime("%Y-%m-%d")}
Previous Close: {prices_df.iloc[-2]['close']}
Open: {prices_df.iloc[-1]['open']}
Close: {prices_df.iloc[-1]['close']}
High: {prices_df.iloc[-1]['high']}
Low: {prices_df.iloc[-1]['low']}
Volume: {format_volume(prices_df.iloc[-1]['volume'])}
Average Volume (3M): {format_volume(prices_df["volume"].mean())}
1-month return: {return_1month:.2f}%
3-month return: {return_3month:.2f}%

### Technical Indicators
{trend}
{momentum}
{volatility}
{volume}
"""


class FinancialMetrics(BaseModel):
    ticker: str
    market_cap: float | None
    enterprise_value: float | None
    price_to_earnings_ratio: float | None
    price_to_book_ratio: float | None
    price_to_sales_ratio: float | None
    enterprise_value_to_ebitda_ratio: float | None
    enterprise_value_to_revenue_ratio: float | None
    free_cash_flow_yield: float | None
    peg_ratio: float | None
    gross_margin: float | None
    operating_margin: float | None
    net_margin: float | None
    return_on_equity: float | None
    return_on_assets: float | None
    return_on_invested_capital: float | None
    asset_turnover: float | None
    inventory_turnover: float | None
    receivables_turnover: float | None
    days_sales_outstanding: float | None
    operating_cycle: float | None
    working_capital_turnover: float | None
    current_ratio: float | None
    quick_ratio: float | None
    cash_ratio: float | None
    operating_cash_flow_ratio: float | None
    debt_to_equity: float | None
    debt_to_assets: float | None
    interest_coverage: float | None
    revenue_growth: float | None
    earnings_growth: float | None
    book_value_growth: float | None
    earnings_per_share_growth: float | None
    free_cash_flow_growth: float | None
    operating_income_growth: float | None
    ebitda_growth: float | None
    payout_ratio: float | None
    earnings_per_share: float | None
    book_value_per_share: float | None
    free_cash_flow_per_share: float | None


class FinancialMetricsResponse(BaseModel):
    snapshot: FinancialMetrics

    def create_prompt(self) -> str:
        if not self.snapshot:
            return "No financial reports available."

        # Use the most recent financial metric entry
        fm = self.snapshot

        def fmt(x):
            return "N/A" if x is None else f"{x:,.2f}"

        def pct(x):
            return "N/A" if x is None else f"{x*100:.1f}%"

        def format_large_number(n):
            if n >= 1_000_000_000_000:
                return f"{n / 1_000_000_000_000:.0f}T"
            elif n >= 1_000_000_000:
                return f"{n / 1_000_000_000:.0f}B"
            elif n >= 1_000_000:
                return f"{n / 1_000_000:.0f}M"
            elif n >= 1_000:
                return f"{n / 1_000:.0f}K"
            else:
                return str(n)

        return f"""
### Financial Metrics
Market Value
- Market Cap: ${format_large_number(fm.market_cap)}
- Enterprise Value: ${format_large_number(fm.enterprise_value)}

Multiples
- P/E Ratio: {fmt(fm.price_to_earnings_ratio)}
- PEG Ratio: {fmt(fm.peg_ratio)}
- Price/Book Ratio: {fmt(fm.price_to_book_ratio)}
- Price/Sales Ratio: {fmt(fm.price_to_sales_ratio)}
- EV/EBITDA: {fmt(fm.enterprise_value_to_ebitda_ratio)}
- EV/Revenue: {fmt(fm.enterprise_value_to_revenue_ratio)}
- Free Cash Flow Yield: {pct(fm.free_cash_flow_yield)}

Profitability
- Gross Margin: {pct(fm.gross_margin)}
- Operating Margin: {pct(fm.operating_margin)}
- Net Margin: {pct(fm.net_margin)}
- ROE (Return on Equity): {pct(fm.return_on_equity)}
- ROA (Return on Assets): {pct(fm.return_on_assets)}
- ROIC (Return on Invested Capital): {pct(fm.return_on_invested_capital)}

Efficiency
- Asset Turnover: {fmt(fm.asset_turnover)}
- Inventory Turnover: {fmt(fm.inventory_turnover)}
- Receivables Turnover: {fmt(fm.receivables_turnover)}
- DSO (Days Sales Outstanding): {fmt(fm.days_sales_outstanding)}
- Operating Cycle: {fmt(fm.operating_cycle)}
- Working Capital Turnover: {fmt(fm.working_capital_turnover)}

Liquidity
- Current Ratio: {fmt(fm.current_ratio)}
- Quick Ratio: {fmt(fm.quick_ratio)}
- Cash Ratio: {fmt(fm.cash_ratio)}
- Operating Cash Flow Ratio: {fmt(fm.operating_cash_flow_ratio)}

Leverage
- Debt/Equity: {fmt(fm.debt_to_equity)}
- Debt/Assets: {fmt(fm.debt_to_assets)}
- Interest Coverage: {fmt(fm.interest_coverage)}

Growth
- Revenue Growth: {pct(fm.revenue_growth)}
- EPS Growth: {pct(fm.earnings_per_share_growth)}
- Book Value Growth: {pct(fm.book_value_growth)}
- Free Cash Flow Growth: {pct(fm.free_cash_flow_growth)}
- EBITDA Growth: {pct(fm.ebitda_growth)}
- Operating Income Growth: {pct(fm.operating_income_growth)}

Per Share Metrics
- EPS: ${fmt(fm.earnings_per_share)}
- Book Value per Share: ${fmt(fm.book_value_per_share)}
- Free Cash Flow per Share: ${fmt(fm.free_cash_flow_per_share)}

"""


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
            return "No insider trades available from past 90 days."

        prompt_lines = ["### Insider Trades from Past 90 days"]
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
            trade_block = "\n".join(line for line in lines if line) + "\n"
            prompt_lines.append(trade_block)

        return "\n".join(prompt_lines)
