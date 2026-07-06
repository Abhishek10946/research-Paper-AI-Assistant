"""Singleton Groq client + one-shot chat() helper."""
from __future__ import annotations

import streamlit as st

from shared import config
from shared.config import FAST_MODEL


@st.cache_resource
def get_llm(model: str = FAST_MODEL, temperature: float = 0.3):
    from langchain_groq import ChatGroq

    key = config.GROQ_API_KEY
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY not found. Locally: add it to .env and restart the server. "
            "On Streamlit Cloud: add it in App settings → Secrets."
        )
    return ChatGroq(api_key=key, model=model, temperature=temperature)


def chat(
    prompt: str,
    system: str = "You are a precise, factual research assistant.",
    model: str = FAST_MODEL,
    temperature: float = 0.3,
) -> str:
    llm = get_llm(model, temperature)
    response = llm.invoke([("system", system), ("user", prompt)])
    return response.content.strip()