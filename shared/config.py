"""Central configuration: env vars, paths, model names, tuning constants."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", str(DATA_DIR / "chroma")))
FAISS_CACHE_DIR = Path(os.getenv("FAISS_CACHE_DIR", str(DATA_DIR / "faiss_cache")))

for _p in (DATA_DIR, CHROMA_DIR, FAISS_CACHE_DIR):
    _p.mkdir(parents=True, exist_ok=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'sessions.db'}")

# Groq model ids
FAST_MODEL = "llama-3.1-8b-instant"      # analysis + Q&A
SMART_MODEL = "llama-3.3-70b-versatile"  # IEEE section writing

# Tuning
MAX_REPO_FILES = 40
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 5
MEMORY_TURNS = 3
