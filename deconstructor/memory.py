"""Conversation memory: format the last N turns for the LLM prompt."""
from __future__ import annotations

from deconstructor.database import get_last_turns
from shared.config import MEMORY_TURNS


def format_history(session_id: int, turns: int = MEMORY_TURNS) -> str:
    rows = get_last_turns(session_id, turns)
    if not rows:
        return ""
    return "\n".join(f"{r.role.capitalize()}: {r.content}" for r in rows)
