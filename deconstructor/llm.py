"""Deconstructor LLM calls: grounded ask() + name_session()."""
from __future__ import annotations

from shared.config import FAST_MODEL
from shared.llm import chat

SYSTEM = (
    "You answer questions about research papers strictly from the excerpts "
    "provided. If the excerpts do not contain the answer, say so plainly "
    "instead of guessing. Be concise and technical."
)


def ask(question: str, context: str, history: str = "") -> str:
    history_block = f"Recent conversation:\n{history}\n\n" if history else ""
    prompt = f"""{history_block}Excerpts from the uploaded paper(s):
---
{context}
---

Question: {question}

Answer using only the excerpts above."""
    return chat(prompt, system=SYSTEM, model=FAST_MODEL, temperature=0.2)


def name_session(sample_text: str) -> str:
    try:
        title = chat(
            "Give a 3-5 word title for a chat about this research paper. "
            "Return only the title - no quotes, no punctuation.\n\n"
            f"Paper excerpt:\n{sample_text[:1000]}",
            model=FAST_MODEL,
            temperature=0.2,
        )
        title = title.strip().strip('"').strip("'")
        return title[:60] if title else "Research Paper Chat"
    except Exception:
        return "Research Paper Chat"
