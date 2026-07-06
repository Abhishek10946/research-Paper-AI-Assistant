"""Build an in-memory FAISS index from fetched repository content."""
from __future__ import annotations

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from shared.embeddings import get_embeddings
from shared.text_splitter import get_splitter


def build_index(fetched: dict) -> FAISS:
    meta = fetched["meta"]
    docs: list[Document] = [
        Document(
            page_content=(
                f"Repository: {meta['full_name']}\n"
                f"Description: {meta['description']}\n"
                f"Primary language: {meta['language']}\n"
                f"Topics: {', '.join(meta['topics'])}"
            ),
            metadata={"source": "repository-metadata"},
        )
    ]

    if fetched.get("readme"):
        docs.append(Document(page_content=fetched["readme"][:20_000], metadata={"source": "README"}))

    for f in fetched["files"]:
        docs.append(Document(page_content=f["content"][:12_000], metadata={"source": f["path"]}))

    chunks = get_splitter().split_documents(docs)
    return FAISS.from_documents(chunks, get_embeddings())
