from langchain_community.embeddings import HuggingFaceEmbeddings
from shared.config import EMBEDDING_MODEL_NAME

_embedding = None

def get_embeddings():
    global _embedding
    if _embedding is None:
        _embedding = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embedding
