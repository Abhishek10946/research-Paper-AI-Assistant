"""SQLite persistence for chat sessions and messages (SQLAlchemy ORM).

init_db() runs an automatic migration on every start: if the sessions table
predates the last_active column, it is added in place without deleting data.
"""
from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy import (
    DateTime, ForeignKey, Integer, String, Text, create_engine, text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from shared.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class ChatSession(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), default="New Chat")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_active: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), index=True)
    role: Mapped[str] = mapped_column(String(16))          # "user" | "assistant"
    content: Mapped[str] = mapped_column(Text)
    sources: Mapped[str] = mapped_column(Text, default="[]")  # JSON list of filenames
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


def _migrate() -> None:
    with engine.connect() as conn:
        cols = [row[1] for row in conn.execute(text("PRAGMA table_info(sessions)"))]
        if cols and "last_active" not in cols:
            conn.execute(text("ALTER TABLE sessions ADD COLUMN last_active DATETIME"))
            conn.execute(text("UPDATE sessions SET last_active = created_at"))
            conn.commit()


def init_db() -> None:
    Base.metadata.create_all(engine)
    _migrate()


# ------------------------------------------------------------------ CRUD ----

def create_session(name: str = "New Chat") -> int:
    with Session(engine) as s:
        row = ChatSession(name=name)
        s.add(row)
        s.commit()
        return row.id


def list_sessions() -> list[ChatSession]:
    with Session(engine) as s:
        return list(
            s.query(ChatSession).order_by(ChatSession.last_active.desc()).all()
        )


def get_session(session_id: int) -> ChatSession | None:
    with Session(engine) as s:
        return s.get(ChatSession, session_id)


def rename_session(session_id: int, name: str) -> None:
    with Session(engine) as s:
        row = s.get(ChatSession, session_id)
        if row:
            row.name = name[:120]
            s.commit()


def touch_session(session_id: int) -> None:
    with Session(engine) as s:
        row = s.get(ChatSession, session_id)
        if row:
            row.last_active = datetime.utcnow()
            s.commit()


def delete_session(session_id: int) -> None:
    """Cascade delete: messages first, then the session row."""
    with Session(engine) as s:
        s.query(Message).filter(Message.session_id == session_id).delete()
        row = s.get(ChatSession, session_id)
        if row:
            s.delete(row)
        s.commit()


def add_message(session_id: int, role: str, content: str, sources: list[str] | None = None) -> None:
    with Session(engine) as s:
        s.add(Message(
            session_id=session_id, role=role, content=content,
            sources=json.dumps(sources or []),
        ))
        s.commit()


def get_messages(session_id: int) -> list[Message]:
    with Session(engine) as s:
        return list(
            s.query(Message)
            .filter(Message.session_id == session_id)
            .order_by(Message.created_at.asc(), Message.id.asc())
            .all()
        )


def get_last_turns(session_id: int, turns: int = 3) -> list[Message]:
    """Last N user/assistant exchange pairs, oldest first."""
    with Session(engine) as s:
        rows = (
            s.query(Message)
            .filter(Message.session_id == session_id)
            .order_by(Message.created_at.desc(), Message.id.desc())
            .limit(turns * 2)
            .all()
        )
    return list(reversed(rows))
