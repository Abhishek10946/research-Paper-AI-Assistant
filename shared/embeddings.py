"""Shared HuggingFace embeddings, cached once per Streamlit session."""
from __future__ import annotations

import streamlit as st

from shared.config import EMBEDDING_MODEL_NAME


@st.cache_resource(show_spinner="Loading embedding model…")
def get_embeddings():
    from langchain_huggingface import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        encode_kwargs={"normalize_embeddings": True},
    )
