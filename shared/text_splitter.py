"""Default text splitter used by both Constructor and Deconstructor."""
from __future__ import annotations

from langchain_text_splitters import RecursiveCharacterTextSplitter

from shared.config import CHUNK_OVERLAP, CHUNK_SIZE


def get_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
