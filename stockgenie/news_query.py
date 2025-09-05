import chromadb

class NewsQuery:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(name="news_collection")

    def search_news(self, company: str, k: int = 5):
        results = self.collection.query(
            query_texts=[company],
            n_results=k,
            where={"company": company}  # only match company’s stored news
        )
        return results["documents"][0] if results and results["documents"] else []