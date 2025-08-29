from langchain_core.tools import tool
import pandas as pd
import yaml
import yfinance as yf
  
# Load YAML file
with open("prompts.yaml", "r") as f:
    data = yaml.safe_load(f)


@tool
def fetch_holding_price(ticker: str):
   """fetch existing holding price and name for ticker"""
   holding_data = pd.read_csv('holding.csv')
   holding_price = holding_data[holding_data['Ticker']==ticker]['Unit Price'].values[0]
   return holding_price

@tool
def fetch_market_price(ticker: str):
    """fetch market price on last business day with a ticker"""
    ticker = yf.Ticker(ticker)  # Apple
    price = ticker.history(period="1d")["Close"].iloc[-1]
    return price

# Example: fetch one prompt by name
def get_prompt(name, **kwargs):
    for p in data["prompts"]:
        if p["name"] == name:
            return p["prompt"].format(**kwargs)
    raise ValueError(f"Prompt '{name}' not found.")