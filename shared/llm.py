"""Singleton Groq client + one-shot chat() helper."""
from __future__ import annotations

import streamlit as st

from shared.config import FAST_MODEL, GROQ_API_KEY


@st.cache_resource
def get_llm(model: str = FAST_MODEL, temperature: float = 0.3):
    from langchain_groq import ChatGroq

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY missing. Add it to your .env file.")
    return ChatGroq(api_key=GROQ_API_KEY, model=model, temperature=temperature)


def chat(
    prompt: str,
    system: str = "You are a precise, factual research assistant.",
    model: str = FAST_MODEL,
    temperature: float = 0.3,
) -> str:
    llm = get_llm(model, temperature)
    response = llm.invoke([("system", system), ("user", prompt)])
    return response.content.strip()
