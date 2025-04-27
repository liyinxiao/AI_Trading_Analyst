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
```

Run the code
```
python3 main.py --ticker TSLA
```

Example Prompt
```
### Key Stock Statistics
Date: 2025-04-25
Ticker: TSLA
Previous Close: 259.51
Open: 261.69
Close: 284.95
High: 286.85
Low: 259.63
Volume: 167521263

### Technical Indicators
8-day EMA: 255.99
21-day EMA: 254.11
55-day EMA: 262.53
ADX: 20.51 
+DI: 38.02
-DI: 16.66
Bollinger Bands: upper band = 287.48, lower band = 218.8
14-day RSI: 63.11
28-day RSI: 56.76

### Insider Trades from Past 60 days
Insider Trade #1 of TSLA
- Issuer: Tesla Inc
- Name: Vaibhav Taneja
- Title: Chief Financial Officer
- Board Director: False
- Transaction Date: 2025-04-07
- Shares Traded: -4000.0
- Price per Share: $18.22
- Transaction Value: $72880.0
- Shares Before: 741920.0
- Shares After: 737920.0
- Security Title: Non-Qualified Stock Option right to buy
- Filing Date: 2025-04-09
Insider Trade #2 of TSLA
- Issuer: Tesla Inc
- Name: Vaibhav Taneja
- Title: Chief Financial Officer
- Board Director: False
- Transaction Date: 2025-04-07
- Shares Traded: -4000.0
- Price per Share: $250.0
- Transaction Value: $1000000.0
- Shares Before: 30949.0
- Shares After: 26949.0
- Security Title: Common Stock
- Filing Date: 2025-04-09
Insider Trade #3 of TSLA
- Issuer: Tesla Inc
- Name: Vaibhav Taneja
- Title: Chief Financial Officer
- Board Director: False
- Transaction Date: 2025-04-07
- Shares Traded: 4000.0
- Price per Share: $18.22
- Transaction Value: $72880.0
- Shares Before: 26949.0
- Shares After: 30949.0
- Security Title: Common Stock
- Filing Date: 2025-04-09

### Instructions: Review `Key Stock Statistics`, `Technical Indicators` and `Insider Trades`, and provide a rating to stock ticker=TSLA. The rating should be strong buy, buy, hold, sell, or strong sell. 
Your answer should only contain a JSON object with the following two keywords:
'rating': Strong buy, buy, hold, sell, or strong sell
'reasoning': A short description of your reasoning for the rating
Please DO NOT output anything outside the JSON.
```