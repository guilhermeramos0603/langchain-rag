import chromadb
from openai import OpenAI

from app.rag.indexer import CHROMA_DIR, get_openai_embedding, index_documents


def retrieve(query: str, n_results: int = 3) -> list[str]:
    collection = index_documents()
    client = OpenAI()

    query_embedding = get_openai_embedding(query, client)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    return results["documents"][0] if results["documents"] else []
