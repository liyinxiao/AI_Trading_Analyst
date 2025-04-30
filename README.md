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
python3 main.py --tickers=TSLA,AAPL,GOOGL,MSFT,NVDA --end-date=2025-04-29
```

Example Output
```
MSFT Stock Analysis
+------------------+-----+------------------------------------------------------------------------------------------------------+
| llama3.1         | buy | The stock price has been increasing over the past month with a 4.81% return in one month and -10.15% |
|                  |     | return in three months. The RSI indicators are not overly bullish, but the ADX is relatively low at  |
|                  |     | 22.73, indicating a possible trend reversal. Insider trades show some buying activity from           |
|                  |     | directors, which could be a positive sign for the stock.                                             |
+------------------+-----+------------------------------------------------------------------------------------------------------+
| gemma3:12b       | buy | MSFT is showing mixed signals. The price is trending upwards, supported by the moving averages, and  |
|                  |     | the stock is within the upper half of its Bollinger Bands, suggesting potential for further short-   |
|                  |     | term gains. However, the recent 3-month return is negative, and volume is below average. Insider     |
|                  |     | activity is minimal and mostly related to restricted stock unit grants, which aren't necessarily     |
|                  |     | indicative of sentiment. The ADX is moderate, suggesting a lack of strong directional movement.      |
|                  |     | Overall, the positive momentum indicators and upward trend outweigh the negative returns, but        |
|                  |     | caution is warranted.                                                                                |
+------------------+-----+------------------------------------------------------------------------------------------------------+
| mistral-nemo:12b | buy | MSFT has shown positive momentum with a 1-month return of 4.81% and a closing price above its 20-day |
|                  |     | and 50-day moving averages. However, the 3-month return is negative (-10.15%), indicating some       |
|                  |     | recent weakness. The RSI is in the neutral range (56.97), and there's no significant insider selling |
|                  |     | activity within the last 90 days. Overall, while there are signs of short-term strength, the longer- |
|                  |     | term trend is uncertain.                                                                             |
+------------------+-----+------------------------------------------------------------------------------------------------------+
| qwen3:14b        | buy | MSFT is trading above its 20-day and 50-day moving averages, with positive short-term momentum       |
|                  |     | (14-day RSI at 56.97). Insider buying by board members (e.g., restricted stock purchases) suggests   |
|                  |     | confidence, though mixed insider activity (e.g., small sell by Amy Coleman at ~$387.81) introduces   |
|                  |     | caution. Lower-than-average volume may indicate reduced near-term interest, but the stock is not     |
|                  |     | overbought (RSI <70) or near the upper Bollinger Band (402.35). The 3-month negative return          |
|                  |     | (-10.15%) contrasts with recent strength, but overall technicals and insider buying lean slightly    |
|                  |     | positive for short-term performance.                                                                 |
+------------------+-----+------------------------------------------------------------------------------------------------------+
```