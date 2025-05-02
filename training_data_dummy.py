# training_data.py

TSLA_Prompt = """
TSLA Stock Analysis
### Key Statistics
Date: 2025-04-24
Previous Close: 250.74
Open: 250.5
Close: 259.51
High: 259.54
Low: 249.2
Volume: 94M
Average Volume (3M): 112.0M
1-month return: -4.61%
3-month return: -36.17%

### Technical Indicators
Trend Indicators
- SMA (20-day): 246.99
- SMA (50-day): 254.24
- EMA (20-day): 248.42
- EMA (50-day): 255.81
- MACD: -7.40, Signal: -9.50, Diff: 2.10
- ADX (Average Directional Index): 21.22
  - +DI: 21.49
  - -DI: 23.65
- CCI (Commodity Channel Index): 24.89
- DPO (Detrended Price Oscillator): -30.69
- Vortex Indicator:
  - VI+ : 0.88
  - VI- : 0.94
- Ichimoku:
  - Conversion Line (Tenkan-sen): 242.30
  - Base Line (Kijun-sen): 253.05
- KST Oscillator: -68.00
  - Signal: -71.70

Momentum Indicators
- RSI (14-day): 51.0
- RSI (28-day): 46.0
- Stoch RSI:
  - Fast K: 0.76
  - Fast D: 0.56
- TSI (True Strength Index): -9.8
- ULTOSC (Ultimate Oscillator): 53.1
- ROC (Rate of Change): 11.2
- KAMA (Kaufman's Adaptive Moving Average): 253.0

Volatility Indicators
- Bollinger Bands:
  - Middle: 252.5
  - Upper: 536.7
  - Lower: 31.6
  - Position within band: 0.45
- ATR (Average True Range): 19.9
- Donchian Channel:
  - Upper Band: 506.1
  - Lower Band: 77.6

Volume Indicators
- MFI (Money Flow Index): 41.3
- On-Balance Volume: -748M
  - 10-day Trend: OBV is rising, while price is falling.
  - OBV vs 10-day MA: above
- Chaikin Money Flow (CMF): 0.05
- Ease of Movement (EoM): 26.6
- Force Index: 335.0M
- Volume Price Trend (VPT): -21.0M

### Instructions: for stock TSLA, review `Key Statistics` and `Technical Indicators`, and provide a rating to predict its stock performance within the next 5 trading days. The rating should be strong buy (+5% or better), buy (+1% to +5%), hold (-1% to +1%), sell (-5% to -1%), or strong sell (-5% or worse). 

Your answer should only contain a JSON object with the following two keywords:
'reasoning': a detailed description of your thought process for the rating
'rating': strong buy, buy, hold, sell, or strong sell
Please DO NOT output anything outside the JSON.
"""

AAPL_Prompt = """
AAPL Stock Analysis
### Key Statistics
Date: 2025-04-24
Previous Close: 204.6
Open: 204.89
Close: 208.37
High: 208.83
Low: 202.94
Volume: 47M
Average Volume (3M): 61.0M
1-month return: -5.94%
3-month return: -6.47%

### Technical Indicators
Trend Indicators
- SMA (20-day): 196.80
- SMA (50-day): 206.12
- EMA (20-day): 200.96
- EMA (50-day): 205.75
- MACD: -4.79, Signal: -6.82, Diff: 2.04
- ADX (Average Directional Index): 23.59
  - +DI: 25.08
  - -DI: 25.73
- CCI (Commodity Channel Index): 27.15
- DPO (Detrended Price Oscillator): -29.86
- Vortex Indicator:
  - VI+ : 0.91
  - VI- : 0.93
- Ichimoku:
  - Conversion Line (Tenkan-sen): 199.50
  - Base Line (Kijun-sen): 197.42
- KST Oscillator: -114.96
  - Signal: -125.22

Momentum Indicators
- RSI (14-day): 51.5
- RSI (28-day): 47.9
- Stoch RSI:
  - Fast K: 0.96
  - Fast D: 0.88
- TSI (True Strength Index): -10.0
- ULTOSC (Ultimate Oscillator): 53.9
- ROC (Rate of Change): 14.8
- KAMA (Kaufman's Adaptive Moving Average): 199.3

Volatility Indicators
- Bollinger Bands:
  - Middle: 202.3
  - Upper: 432.6
  - Lower: 28.0
  - Position within band: 0.45
- ATR (Average True Range): 9.8
- Donchian Channel:
  - Upper Band: 394.8
  - Lower Band: 56.4

Volume Indicators
- MFI (Money Flow Index): 47.0
- On-Balance Volume: -88M
  - 10-day Trend: OBV is rising, while price is rising.
  - OBV vs 10-day MA: above
- Chaikin Money Flow (CMF): 0.01
- Ease of Movement (EoM): 6.0
- Force Index: 95.0M
- Volume Price Trend (VPT): 587.0K

### Instructions: for stock AAPL, review `Key Statistics` and `Technical Indicators`, and provide a rating to predict its stock performance within the next 5 trading days. The rating should be strong buy (+5% or better), buy (+1% to +5%), hold (-1% to +1%), sell (-5% to -1%), or strong sell (-5% or worse). 

Your answer should only contain a JSON object with the following two keywords:
'reasoning': a detailed description of your thought process for the rating
'rating': strong buy, buy, hold, sell, or strong sell
Please DO NOT output anything outside the JSON.
"""

GOOGL_Prompt = """
GOOGL Stock Analysis
### Key Statistics
Date: 2025-04-24
Previous Close: 155.35
Open: 156.15
Close: 159.28
High: 159.59
Low: 155.79
Volume: 45M
Average Volume (3M): 35.0M
1-month return: -3.50%
3-month return: -20.44%

### Technical Indicators
Trend Indicators
- SMA (20-day): 153.92
- SMA (50-day): 156.51
- EMA (20-day): 154.45
- EMA (50-day): 157.44
- MACD: -3.00, Signal: -4.21, Diff: 1.21
- ADX (Average Directional Index): 37.50
  - +DI: 23.09
  - -DI: 26.88
- CCI (Commodity Channel Index): 84.02
- DPO (Detrended Price Oscillator): -9.07
- Vortex Indicator:
  - VI+ : 0.98
  - VI- : 0.88
- Ichimoku:
  - Conversion Line (Tenkan-sen): 153.91
  - Base Line (Kijun-sen): 155.58
- KST Oscillator: -71.70
  - Signal: -90.27

Momentum Indicators
- RSI (14-day): 51.6
- RSI (28-day): 46.0
- Stoch RSI:
  - Fast K: 0.90
  - Fast D: 0.76
- TSI (True Strength Index): -15.1
- ULTOSC (Ultimate Oscillator): 52.5
- ROC (Rate of Change): 8.5
- KAMA (Kaufman's Adaptive Moving Average): 155.6

Volatility Indicators
- Bollinger Bands:
  - Middle: 153.8
  - Upper: 317.1
  - Lower: 9.5
  - Position within band: 0.49
- ATR (Average True Range): 5.9
- Donchian Channel:
  - Upper Band: 305.9
  - Lower Band: 24.9

Volume Indicators
- MFI (Money Flow Index): 41.2
- On-Balance Volume: -224M
  - 10-day Trend: OBV is falling, while price is falling.
  - OBV vs 10-day MA: above
- Chaikin Money Flow (CMF): -0.04
- Ease of Movement (EoM): 16.7
- Force Index: 41.0M
- Volume Price Trend (VPT): -11.0M


### Instructions: for stock GOOGL, review `Key Statistics` and `Technical Indicators`, and provide a rating to predict its stock performance within the next 5 trading days. The rating should be strong buy (+5% or better), buy (+1% to +5%), hold (-1% to +1%), sell (-5% to -1%), or strong sell (-5% or worse). 

Your answer should only contain a JSON object with the following two keywords:
'reasoning': a detailed description of your thought process for the rating
'rating': strong buy, buy, hold, sell, or strong sell
Please DO NOT output anything outside the JSON.
"""

MSFT_Prompt = """
MSFT Stock Analysis
### Key Statistics
Date: 2025-04-24
Previous Close: 374.39
Open: 375.69
Close: 387.3
High: 388.45
Low: 375.19
Volume: 22M
Average Volume (3M): 25.0M
1-month return: -0.68%
3-month return: -12.78%

### Technical Indicators
Trend Indicators
- SMA (20-day): 376.28
- SMA (50-day): 379.21
- EMA (20-day): 375.75
- EMA (50-day): 379.57
- MACD: -3.82, Signal: -5.03, Diff: 1.21
- ADX (Average Directional Index): 24.95
  - +DI: 25.38
  - -DI: 25.18
- CCI (Commodity Channel Index): 67.71
- DPO (Detrended Price Oscillator): -21.21
- Vortex Indicator:
  - VI+ : 0.97
  - VI- : 0.90
- Ichimoku:
  - Conversion Line (Tenkan-sen): 375.16
  - Base Line (Kijun-sen): 370.58
- KST Oscillator: -34.24
  - Signal: -41.55

Momentum Indicators
- RSI (14-day): 53.8
- RSI (28-day): 48.9
- Stoch RSI:
  - Fast K: 0.79
  - Fast D: 0.63
- TSI (True Strength Index): -10.1
- ULTOSC (Ultimate Oscillator): 48.8
- ROC (Rate of Change): 8.2
- KAMA (Kaufman's Adaptive Moving Average): 374.7

Volatility Indicators
- Bollinger Bands:
  - Middle: 375.8
  - Upper: 774.2
  - Lower: 22.7
  - Position within band: 0.49
- ATR (Average True Range): 13.4
- Donchian Channel:
  - Upper Band: 739.4
  - Lower Band: 49.9

Volume Indicators
- MFI (Money Flow Index): 47.1
- On-Balance Volume: -173M
  - 10-day Trend: OBV is falling, while price is falling.
  - OBV vs 10-day MA: above
- Chaikin Money Flow (CMF): 0.04
- Ease of Movement (EoM): 305.1
- Force Index: 55.0M
- Volume Price Trend (VPT): -5.0M

### Instructions: for stock MSFT, review `Key Statistics` and `Technical Indicators`, and provide a rating to predict its stock performance within the next 5 trading days. The rating should be strong buy (+5% or better), buy (+1% to +5%), hold (-1% to +1%), sell (-5% to -1%), or strong sell (-5% or worse). 

Your answer should only contain a JSON object with the following two keywords:
'reasoning': a detailed description of your thought process for the rating
'rating': strong buy, buy, hold, sell, or strong sell
Please DO NOT output anything outside the JSON.
"""


NVDA_Prompt = """
NVDA Stock Analysis
### Key Statistics
Date: 2025-04-24
Previous Close: 102.71
Open: 103.47
Close: 106.43
High: 106.54
Low: 103.11
Volume: 220M
Average Volume (3M): 313.0M
1-month return: -6.44%
3-month return: -25.38%

### Technical Indicators
Trend Indicators
- SMA (20-day): 105.25
- SMA (50-day): 108.32
- EMA (20-day): 104.55
- EMA (50-day): 108.04
- MACD: -3.50, Signal: -3.82, Diff: 0.32
- ADX (Average Directional Index): 29.22
  - +DI: 19.55
  - -DI: 28.09
- CCI (Commodity Channel Index): 4.83
- DPO (Detrended Price Oscillator): -9.04
- Vortex Indicator:
  - VI+ : 0.96
  - VI- : 0.88
- Ichimoku:
  - Conversion Line (Tenkan-sen): 104.67
  - Base Line (Kijun-sen): 104.42
- KST Oscillator: -102.12
  - Signal: -115.76

Momentum Indicators
- RSI (14-day): 48.2
- RSI (28-day): 45.5
- Stoch RSI:
  - Fast K: 0.69
  - Fast D: 0.59
- TSI (True Strength Index): -19.2
- ULTOSC (Ultimate Oscillator): 50.6
- ROC (Rate of Change): 9.0
- KAMA (Kaufman's Adaptive Moving Average): 104.8

Volatility Indicators
- Bollinger Bands:
  - Middle: 105.3
  - Upper: 222.7
  - Lower: 12.0
  - Position within band: 0.45
- ATR (Average True Range): 6.8
- Donchian Channel:
  - Upper Band: 201.7
  - Lower Band: 28.5

Volume Indicators
- MFI (Money Flow Index): 52.0
- On-Balance Volume: -686M
  - 10-day Trend: OBV is falling, while price is falling.
  - OBV vs 10-day MA: above
- Chaikin Money Flow (CMF): 0.08
- Ease of Movement (EoM): 2.2
- Force Index: 71.0M
- Volume Price Trend (VPT): -138.0M


### Instructions: for stock NVDA, review `Key Statistics` and `Technical Indicators`, and provide a rating to predict its stock performance within the next 5 trading days. The rating should be strong buy (+5% or better), buy (+1% to +5%), hold (-1% to +1%), sell (-5% to -1%), or strong sell (-5% or worse). 

Your answer should only contain a JSON object with the following two keywords:
'reasoning': a detailed description of your thought process for the rating
'rating': strong buy, buy, hold, sell, or strong sell
Please DO NOT output anything outside the JSON.
"""

training_data = [
    (TSLA_Prompt, "sell"),
    (AAPL_Prompt, "sell"),
    (GOOGL_Prompt, "hold"),
    (MSFT_Prompt, "strong buy"),
    (NVDA_Prompt, "buy"),
]
