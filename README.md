# AI_Trading_Analyst

Customize LLM Models with Ollama's Modelfile
```
ollama create gemma3_trading_analyst_0p1 --file gemma3_trading_analyst_0p1.modelfile
ollama list
ollama run gemma3_trading_analyst_0p1
```

Installation
```
pin install pandas
pip install langchain-ollama langchain-core
pip install langgraph
pip install colorama tabulate
```

Run the code
```
python3 main.py --ticker=TSLA --end-date=2025-04-28
```

Example Output
```
+----------------------------+------+------------------------------------------------------------------------------------------------------+
| llama3.1                   | buy  | TSLA has shown a significant increase in recent trading days with a high volume. The stock is also   |
|                            |      | showing a positive trend with its ADX indicating a moderate price movement and +DI being higher than |
|                            |      | -DI. However, the RSI (14-day) is at 58.48 which suggests that the stock might be due for a          |
|                            |      | correction. Additionally, the company's financials show a high P/E ratio of 144.50 but a low         |
|                            |      | enterprise value to EBITDA ratio of 65.58. The insider trades suggest some sell activity by          |
|                            |      | directors and officers, but this is partially offset by the CFO's buy activity.                      |
+----------------------------+------+------------------------------------------------------------------------------------------------------+
| gemma3_trading_analyst_0p1 | sell | TSLA presents a mixed picture. While the company demonstrates strong liquidity and a healthy cash    |
|                            |      | ratio, growth metrics are concerning with negative revenue and EPS growth. High multiples (P/E,      |
|                            |      | EV/EBITDA) suggest a premium valuation that isn't fully supported by current performance. The recent |
|                            |      | insider selling, particularly by board members like James Murdoch, raises red flags, outweighing the |
|                            |      | positive aspects. The ADX is low, indicating a lack of strong trend. Although free cash flow growth  |
|                            |      | is positive, the overall negative growth trends and significant insider selling warrant a cautious   |
|                            |      | approach.                                                                                            |
+----------------------------+------+------------------------------------------------------------------------------------------------------+
| mistral-nemo:12b           | buy  | TSLA's high P/E ratio (144.50), negative EPS growth (-10.3%), and significant insider selling by     |
|                            |      | James R Murdoch (total -432561 shares) indicate a cautious approach. However, the stock is trading   |
|                            |      | below its 50-day MA and has strong support at $240. Its recent dip might present an attractive       |
|                            |      | buying opportunity for those with a longer-term perspective.                                         |
+----------------------------+------+------------------------------------------------------------------------------------------------------+
| qwen3:14b                  | hold | TSLA shows mixed signals: technical indicators suggest overbought conditions and potential pullback, |
|                            |      | while financial metrics highlight high valuation (P/E=65) and weak revenue growth (5%). Insider      |
|                            |      | selling, particularly by James Murdoch, raises concerns. However, strong ROE (18%) and low debt-to-  |
|                            |      | equity (0.4) provide some support. The combination of overvaluation, lackluster growth, and insider  |
|                            |      | activity leans toward caution.                                                                       |
+----------------------------+------+------------------------------------------------------------------------------------------------------+
```