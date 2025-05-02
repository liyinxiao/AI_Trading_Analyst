# AI_Trading_Analyst

Installation
```
pin install pandas
pip install langchain-ollama langchain-core
pip install langgraph
pip install colorama tabulate
```

Run the code
```
python3 main.py --tickers=TSLA,AAPL,GOOGL,MSFT,NVDA --end-date=2025-05-01
```

Example Output
```
MSFT Stock Analysis
+------------------+------------+------------------------------------------------------------------------------------------------------+
| llama3.1         | strong buy | Based on the analysis of Key Statistics and Technical Indicators, MSFT stock is showing signs of a   |
|                  |            | potential breakout. The stock has been rising steadily over the past month with a 1-month return of  |
|                  |            | 11.32%, indicating a strong upward trend. The RSI (14-day) is at 69.5, which is above the neutral    |
|                  |            | zone but not yet in overbought territory. The MACD is also positive, with a signal line that has     |
|                  |            | crossed above the histogram, indicating a potential bullish crossover. Additionally, the ADX is at   |
|                  |            | 19.39, which suggests that the stock's price movement is becoming more consistent and less volatile. |
|                  |            | Considering these indicators, it appears that MSFT stock is poised for further growth in the next 5  |
|                  |            | trading days. Furthermore, there are no significant red flags or warning signs from the Insider      |
|                  |            | Trades section, which suggests that the company's leadership is confident in its future prospects.   |
+------------------+------------+------------------------------------------------------------------------------------------------------+
| gemma3:12b       |    buy     | MSFT presents a mixed but ultimately bullish picture for the next 5 trading days. Let's break down   |
|                  |            | the factors.   **Positive Indicators:** *   **Strong Price Action:** The stock opened significantly  |
|                  |            | higher than the previous close and closed near its high, indicating strong buying pressure. The gap  |
|                  |            | up suggests positive sentiment and momentum. *   **Technical Indicators:** The RSI (69.5) is         |
|                  |            | approaching overbought territory but isn't yet a significant concern. The MACD shows a positive      |
|                  |            | divergence, suggesting upward momentum. The CCI is very high, which can be a warning sign of a       |
|                  |            | potential pullback, but the current price action supports continued upward movement. The ADX is      |
|                  |            | below 25, indicating a lack of strong trend, but the +DI is significantly higher than the -DI,       |
|                  |            | suggesting an upward bias. *   **Volume:** The volume today was significantly higher than the        |
|                  |            | 3-month average, confirming the buying pressure. The OBV is rising in tandem with the price, further |
|                  |            | supporting the bullish trend. *   **Insider Activity:** While there's a small number of sales, the   |
|                  |            | overall insider activity isn't a significant red flag. Amy Coleman's purchase is a positive signal,  |
|                  |            | even if the price per share is listed as $0. The other insider transactions are mostly related to    |
|                  |            | restricted stock units, which are typical and don't necessarily indicate a change in sentiment.      |
|                  |            | **Negative/Neutral Indicators:** *   **CCI:** The extremely high CCI reading (266.36) suggests the   |
|                  |            | stock may be overbought and vulnerable to a correction. However, the current price action is         |
|                  |            | overriding this signal. *   **Bollinger Bands:** The stock is positioned near the upper band, which  |
|                  |            | could indicate a potential pullback. However, the strong price action suggests the band is expanding |
|                  |            | to accommodate the upward movement.  **Overall Assessment:** The combination of strong price action, |
|                  |            | high volume, and generally positive technical indicators outweigh the potential risks. While the CCI |
|                  |            | and Bollinger Bands suggest caution, the current momentum is too strong to ignore. The insider       |
|                  |            | activity is not a significant concern. Therefore, I anticipate a continued upward trend over the     |
|                  |            | next 5 trading days.                                                                                 |
+------------------+------------+------------------------------------------------------------------------------------------------------+
| mistral-nemo:12b |    buy     | MSFT has shown significant price increase in the past month (1-month return: 11.32%), indicating a   |
|                  |            | strong uptrend. Technical indicators such as MACD and RSI are bullish, with MACD at 4.55 and RSI at  |
|                  |            | 69.5. Additionally, insider trading activity shows board directors acquiring shares, which is a      |
|                  |            | positive sign for the company's future prospects. However, the stock is overbought according to the  |
|                  |            | RSI indicator, suggesting a potential pullback in the short term.                                    |
+------------------+------------+------------------------------------------------------------------------------------------------------+
| qwen3:14b        |    hold    | The stock is currently above both the 20-day and 50-day SMAs, indicating a positive trend. The MACD  |
|                  |            | is positive, and the ADX suggests a moderate uptrend. However, the RSI and Stoch RSI are in          |
|                  |            | overbought territory, which may signal a potential pullback. Insider buying activity, though limited |
|                  |            | in scale, shows some confidence. The high trading volume could indicate strong buying pressure, but  |
|                  |            | the overbought conditions and mixed technical indicators suggest caution. The stock may hold its     |
|                  |            | value but lacks strong upward momentum for a 'buy' rating.                                           |
+------------------+------------+------------------------------------------------------------------------------------------------------+
| deepseek-r1:14b  |    hold    | MSFT has shown positive performance with an 11.32% return in the past month and a 2.49% return over  |
|                  |            | three months. However, technical indicators like CCI (266.36) and RSI (69.5) suggest overbought      |
|                  |            | conditions, which may lead to short-term corrections. The MACD shows bullish signals but with a      |
|                  |            | negative signal line, indicating potential divergence. Insider trades are mostly small transactions  |
|                  |            | involving RSUs, showing some confidence but limited impact. Overall, the stock is likely to face     |
|                  |            | minor corrections due to overbought conditions and mixed technical indicators.                       |
+------------------+------------+------------------------------------------------------------------------------------------------------+
```