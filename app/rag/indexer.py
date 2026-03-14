import os
from pathlib import Path

import chromadb
from openai import OpenAI


DATA_DIR = Path(__file__).parent / "data"
CHROMA_DIR = Path(__file__).parents[2] / "chroma_db"


def get_openai_embedding(text: str, client: OpenAI) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


def load_documents() -> list[dict]:
    docs = []
    for md_file in DATA_DIR.glob("*.md"):
        content = md_file.read_text()
        sections = content.split("\n## ")
        for section in sections[1:]:  # skip the title
            lines = section.strip().split("\n")
            title = lines[0]
            body = "\n".join(lines[1:])
            docs.append({
                "id": f"{md_file.stem}_{title.lower().replace(' ', '_')}",
                "title": title,
                "content": f"{title}\n{body}",
                "source": md_file.name,
            })
    return docs


def index_documents():
    client = OpenAI()
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = chroma_client.get_or_create_collection(
        name="error_docs",
        metadata={"hnsw:space": "cosine"},
    )

    if collection.count() > 0:
        return collection

    docs = load_documents()
    for doc in docs:
        embedding = get_openai_embedding(doc["content"], client)
        collection.add(
            ids=[doc["id"]],
            embeddings=[embedding],
            documents=[doc["content"]],
            metadatas=[{"source": doc["source"], "title": doc["title"]}],
        )

    return collection


if __name__ == "__main__":
    collection = index_documents()
    print(f"Indexed {collection.count()} documents")
