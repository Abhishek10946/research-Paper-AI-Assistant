"""Top-K similarity search against the session's ChromaDB collection."""
from __future__ import annotations

from langchain_core.documents import Document

from deconstructor.ingestion import get_store
from shared.config import TOP_K


def retrieve(session_id: int, query: str, k: int = TOP_K) -> list[Document]:
    return get_store(session_id).similarity_search(query, k=k)
