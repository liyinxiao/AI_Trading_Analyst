from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import requests
from datetime import date, timedelta
import os
from data.models import InsiderTradeResponse, Price, PriceResponse
import argparse


def get_prices(ticker: str, start_date: str, end_date: str) -> PriceResponse:
    """
    Fetch price data from API.
    """
    # If not in cache or no data in range, fetch from API
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    url = f"https://api.financialdatasets.ai/prices/?ticker={ticker}&interval=day&interval_multiplier=1&start_date={start_date}&end_date={end_date}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data: {ticker} - {response.status_code} - {response.text}"
        )

    # Parse response with Pydantic model
    return PriceResponse(**response.json())


def get_insider_trades(
    ticker: str, start_date: str, end_date: str
) -> InsiderTradeResponse:
    """
    Fetch insider trade data from API.
    """
    # If not in cache or no data in range, fetch from API
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    url = f"https://api.financialdatasets.ai/insider-trades/?ticker={ticker}&filing_date_gte={start_date}&filing_date_lte={end_date}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data: {ticker} - {response.status_code} - {response.text}"
        )

    # Parse response with Pydantic model
    return InsiderTradeResponse(**response.json())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the AI trading analyst system")
    parser.add_argument("--tickers", type=str, required=True, help="stock ticker symbol to analyze")
    args = parser.parse_args()
    ticker =  args.tickers.strip()

    start_date = (date.today() - timedelta(days=60)).strftime("%Y-%m-%d")
    end_date = date.today().strftime("%Y-%m-%d")
    prompt = ""

    # Get the historical price data
    prices = get_prices(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
    )
    prompt += prices.create_prompt()

    # Get insider trades
    insider_trades = get_insider_trades(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
    )
    prompt += insider_trades.create_prompt()

    prompt += f"""
### Instructions: Review `Key Stock Statistics`, `Technical Indicators` and `Insider Trades`, and provide a rating to stock ticker={ticker}. \
The rating should be strong buy, buy, hold, sell, or strong sell. 
Your answer should only contain a JSON object with the following two keywords:
'rating': Strong buy, buy, hold, sell, or strong sell
'reasoning': A short description of your reasoning for the rating
Please DO NOT output anything outside the JSON.
"""
    print(prompt)

    # Ollama Settings
    model_names = ["qwen2.5:7b", "llama3.1", "gemma3", "gemma3_trading_analyst_0p1"]
    base_url = "http://localhost:11434"  # Default for local Ollama

    for model_name in model_names:
        # Initialize ChatOllama
        chat = ChatOllama(
            model=model_name,
            base_url=base_url,
        )

        # Send a message
        response = chat.invoke(
            [
                SystemMessage(
                    content="You are a helpful trading analyst. Your job is to rate wheather a stock is a strong buy, buy, hold, sell, or strong sell."
                ),
                HumanMessage(content=prompt),
            ]
        )

        # Print the response
        print("------------------------------------------------------------")
        print("model name: ", model_name)
        print("response: ", response.content)
        print("------------------------------------------------------------")
