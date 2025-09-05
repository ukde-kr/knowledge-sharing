import chromadb
import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
import pandas as pd

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class NewsScraper:
    def __init__(self):
        self.newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        self.chroma_client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(name="news_collection")

    def fetch_stock_news(self, company, from_date):
        """Fetch news related to a company"""
        response = self.newsapi.get_everything(
            q=company,
            from_param=from_date,
            language='en',
            sort_by='relevancy',
            page=1
        )
        
        raw_articles = response.get("articles", [])
        all_articles = [art.get('title') +  '\n' + art.get('description') + '\n' + art.get('content') for art in raw_articles]
        return all_articles

    def chunk_text(self, text, n=256, overlap=100):
        chunks = []
        for i in range(0, len(text), n - overlap):
            chunks.append(text[i:i + n])
        return chunks

    def process_companies(self, from_date='2025-09-01', chunk_size=512, overlap=100):
        companies = pd.read_csv('holding.csv')['Name']
        for company in companies:
            articles = self.fetch_stock_news(company, from_date)
            for article in articles:
                chunks = self.chunk_text(article, chunk_size, overlap)
                for idx, chunk in enumerate(chunks):
                    self.collection.add(
                        ids=[f"{company}_{idx}"],
                        documents=[chunk],
                        metadatas=[{"company": company}]
                    )

# Usage
if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.process_companies()