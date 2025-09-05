from langchain_core.tools import tool
import pandas as pd
import yaml
import requests
import yfinance as yf

import chromadb

# Load YAML file
with open("prompts.yaml", "r") as f:
    data = yaml.safe_load(f)

@tool
def fetch_holding_price(ticker: str):
   """search client investment inventory to find holding value and number of units information with ticker name"""
   holding_data = pd.read_csv('investment_inventory.csv')
   holding_price = holding_data[holding_data['Ticker']==ticker]['Unit Price'].values[0]
   holding_units = holding_data[holding_data['Ticker']==ticker]['Unit'].values[0]
   return f"price: {holding_price}, units: {holding_units}"

@tool
def fetch_market_price(ticker: str):
    """fetch market price on last business day with a ticker"""
    ticker = yf.Ticker(ticker)  # Apple
    price = ticker.history(period="1d")["Close"].iloc[-1]
    return price


@tool
def search_news(company: str):
    """fetch public news related to the company"""
    chroma_client = chromadb.PersistentClient(path="chroma_db")
    collection = chroma_client.get_or_create_collection(name="news_collection")

    results = collection.query(
        query_texts=[f"recent news about {company}"],
        n_results=3
    )
    return results["documents"][0] if results and results["documents"] else []


# Example: fetch one prompt by name
def get_prompt(name, **kwargs):
    for p in data["prompts"]:
        if p["name"] == name:
            return p["prompt"].format(**kwargs)
    raise ValueError(f"Prompt '{name}' not found.")