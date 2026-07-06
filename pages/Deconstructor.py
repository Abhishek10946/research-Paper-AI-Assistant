"""Deconstructor — upload research PDFs, chat with them via RAG."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

st.set_page_config(page_title="Deconstructor · RP Assistant", page_icon="🔍", layout="wide")

from deconstructor import database as db
from deconstructor.ingestion import delete_session_data, has_documents, ingest_pdfs
from deconstructor.llm import ask, name_session
from deconstructor.memory import format_history
from deconstructor.retriever import retrieve
from shared.ui import apply_theme, chips, feature_card, hero, sidebar_header

sidebar_header()
apply_theme()
db.init_db()

sid = st.session_state.get("current_session")

# ----------------------------------------------------------------- sidebar --
with st.sidebar:
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_session = db.create_session()
        st.rerun()

    st.caption("SESSIONS")
    sessions = db.list_sessions()
    if not sessions:
        st.caption("No chats yet.")
    for s in sessions:
        col_name, col_del = st.columns([5, 1])
        label = ("▸ " if s.id == sid else "") + s.name
        if col_name.button(label, key=f"sel_{s.id}", use_container_width=True, type="secondary"):
            st.session_state.current_session = s.id
            st.rerun()
        if col_del.button("🗑️", key=f"del_{s.id}", type="secondary", help="Delete session"):
            db.delete_session(s.id)
            delete_session_data(s.id)
            st.session_state.pop(f"ingested_{s.id}", None)
            if sid == s.id:
                st.session_state.pop("current_session", None)
            st.rerun()

    st.divider()
    if st.button("← Home", use_container_width=True, type="secondary"):
        st.switch_page("home.py")

# --------------------------------------------------------------- empty state
if sid is None:
    hero(
        "DECONSTRUCTOR",
        'Chat with your <span class="grad">research papers</span>',
        "Every answer is retrieved from the PDF itself — top-5 passages from "
        "ChromaDB, with source chips under each reply.",
    )
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        feature_card("➕", "1 · Create a chat", "Click New Chat in the sidebar to open a session.")
    with c2:
        feature_card("📂", "2 · Upload PDFs", "Text-based PDFs work best. Multiple papers per session are fine.")
    with c3:
        feature_card("💬", "3 · Ask anything", "Cross-paper questions welcome — history persists across restarts.")
    st.stop()

# ------------------------------------------------------------------- header --
session_row = db.get_session(sid)
if session_row is None:
    st.session_state.pop("current_session", None)
    st.rerun()

st.markdown(f"### 🔍 {session_row.name}")

# ------------------------------------------------------------------ upload --
ingested_key = f"ingested_{sid}"
ingested: set[str] = st.session_state.setdefault(ingested_key, set())

with st.expander("📂 Upload research papers", expanded=not has_documents(sid)):
    files = st.file_uploader(
        "Drop PDFs here",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"uploader_{sid}",
        label_visibility="collapsed",
    )
    new_files = [f for f in (files or []) if f.name not in ingested]
    if new_files:
        with st.spinner(f"Ingesting {len(new_files)} file(s)…"):
            n_chunks, sample = ingest_pdfs(new_files, sid)
        ingested.update(f.name for f in new_files)
        if n_chunks == 0:
            st.warning("No text found — is the PDF a scanned image?")
        else:
            st.toast(f"Ingested {n_chunks} chunks", icon="📚")
            if session_row.name == "New Chat" and sample:
                db.rename_session(sid, name_session(sample))
                st.rerun()

# -------------------------------------------------------------------- chat --
for m in db.get_messages(sid):
    with st.chat_message(m.role):
        st.markdown(m.content)
        try:
            src = json.loads(m.sources or "[]")
        except json.JSONDecodeError:
            src = []
        if src:
            st.markdown(chips(src), unsafe_allow_html=True)

question = st.chat_input("Ask about the papers…")
if question:
    if not has_documents(sid):
        st.warning("Upload at least one PDF before asking questions.")
        st.stop()

    db.add_message(sid, "user", question)
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Reading the paper…"):
            docs = retrieve(sid, question)
            context = "\n\n---\n\n".join(d.page_content for d in docs)[:6000]
            history = format_history(sid)
            answer = ask(question, context, history)
        st.markdown(answer)
        sources = list(dict.fromkeys(d.metadata.get("source", "document") for d in docs))
        if sources:
            st.markdown(chips(sources), unsafe_allow_html=True)

    db.add_message(sid, "assistant", answer, sources)
    db.touch_session(sid)
