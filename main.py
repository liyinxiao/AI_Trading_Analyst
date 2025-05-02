import re
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import requests
from datetime import timedelta, datetime
import os
from data.models import FinancialMetricsResponse, InsiderTradeResponse, PriceResponse
import argparse
import json
from colorama import Fore, Style
from tabulate import tabulate
import textwrap


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


def get_financial_metrics(
    ticker: str, start_date: str, end_date: str
) -> FinancialMetricsResponse:
    """
    Fetch financial metrics data from API.
    """
    # If not in cache or no data in range, fetch from API
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    url = f"https://api.financialdatasets.ai/financial-metrics/snapshot?ticker={ticker}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data: {ticker} - {response.status_code} - {response.text}"
        )

    # Parse response with Pydantic model
    return FinancialMetricsResponse(**response.json())


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
    parser.add_argument(
        "--tickers",
        type=str,
        required=True,
        help="stock ticker symbol to analyze. Without an API key, only the following are available: AAPL, BRK.B, GOOGL, MSFT, NVDA, TSLA",
    )
    parser.add_argument(
        "--end-date", type=str, help="End date (YYYY-MM-DD). Defaults to today"
    )

    args = parser.parse_args()
    tickers = [ticker.strip() for ticker in args.tickers.split(",")]

    # Set the start and end dates
    if args.end_date:
        try:
            datetime.strptime(args.end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("End date must be in YYYY-MM-DD format")
    end_date = args.end_date or datetime.now().strftime("%Y-%m-%d")
    start_date = (
        datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=90)
    ).strftime("%Y-%m-%d")

    for ticker in tickers:
        prompt = f"{ticker} Stock Analysis"

        # Get price signals
        prices = get_prices(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )
        prompt += prices.create_prompt()

        # Get financial metrics signals
        # financial_metrics = get_financial_metrics(
        #     ticker=ticker,
        #     start_date=start_date,
        #     end_date=end_date,
        # )
        # prompt += financial_metrics.create_prompt()

        # Get insider trade signals
        insider_trades = get_insider_trades(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )
        prompt += insider_trades.create_prompt()

        prompt += f"""
### Instructions: for stock {ticker}, review `Key Statistics`, `Technical Indicators`, and `Insider Trades`, \
and provide a rating to predict its stock performance within the next 5 trading days. The rating should be strong buy \
(+5% or better), buy (+1% to +5%), hold (-1% to +1%), sell (-5% to -1%), or strong sell (-5% or worse). 

Your answer should only contain a JSON object with the following two keywords:
'reasoning': a detailed description of your thought process for the rating
'rating': strong buy, buy, hold, sell, or strong sell
Please DO NOT output anything outside the JSON.
"""

        # print(prompt)

        # Ollama Settings
        model_names = [
            "llama3.1",
            "gemma3:12b",
            "mistral-nemo:12b",
            "qwen3:14b",
            "deepseek-r1:14b",
        ]
        base_url = "http://localhost:11434"  # Default for local Ollama
        summary = []

        for model_name in model_names:
            # Initialize ChatOllama
            chat = ChatOllama(
                model=model_name,
                base_url=base_url,
                temperature=0.6,
            )

            # Send a message
            response = chat.invoke(
                [
                    SystemMessage(
                        content="You are a helpful trading analyst. Your job is to predict how a stock performs in the next 5 trading days."
                    ),
                    HumanMessage(content=prompt),
                ]
            )
            # Print the response
            # print("------------------------------------------------------------")
            # print("model name: ", model_name)
            # print("response: ", response.content)
            # print("------------------------------------------------------------")

            json_str = (
                re.sub(r"<think>.*?</think>", "", response.content, flags=re.DOTALL)
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            try:
                data = json.loads(json_str)
                rating = data.get("rating", "unavailable").lower()
                reasoning = data.get("reasoning", "unavailable")
            except:
                rating = "unavailable"
                reasoning = json_str

            rating_color = {
                "strong buy": Fore.GREEN,
                "buy": Fore.GREEN,
                "hold": Fore.YELLOW,
                "sell": Fore.RED,
                "strong sell": Fore.RED,
            }.get(rating, Fore.WHITE)

            summary.append(
                [
                    model_name,
                    f"{rating_color}{rating}{Style.RESET_ALL}",
                    "\n".join(textwrap.wrap(reasoning, width=100)),
                ]
            )

        print(f"{ticker} Stock Analysis")
        print(tabulate(summary, tablefmt="grid", colalign=("left", "center", "left")))
