"""PDF ingestion: PyMuPDF → splitter → per-session ChromaDB collection."""
from __future__ import annotations

import tempfile
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyMuPDFLoader

from shared.config import CHROMA_DIR
from shared.embeddings import get_embeddings
from shared.text_splitter import get_splitter


def get_store(session_id: int) -> Chroma:
    return Chroma(
        collection_name=f"session_{session_id}",
        embedding_function=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
    )


def has_documents(session_id: int) -> bool:
    try:
        return get_store(session_id)._collection.count() > 0
    except Exception:
        return False


def ingest_pdfs(uploaded_files, session_id: int) -> tuple[int, str]:
    """Ingest Streamlit UploadedFile objects. Returns (chunk_count, sample_text)."""
    docs = []
    for uf in uploaded_files:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(uf.getbuffer())
            tmp_path = tmp.name
        try:
            pages = PyMuPDFLoader(tmp_path).load()
            for p in pages:
                p.metadata["source"] = uf.name
            docs.extend(pages)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    if not docs:
        return 0, ""

    chunks = get_splitter().split_documents(docs)
    if chunks:
        get_store(session_id).add_documents(chunks)

    sample = docs[0].page_content[:1200]
    return len(chunks), sample


def delete_session_data(session_id: int) -> None:
    try:
        get_store(session_id).delete_collection()
    except Exception:
        pass
