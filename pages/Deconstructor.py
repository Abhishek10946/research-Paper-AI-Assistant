import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from deconstructor.ingestion import ingest_documents
from deconstructor.retriever import ask_question
from deconstructor.memory import build_memory
from deconstructor.database import (
    create_session,
    load_messages,
    save_message,
    list_sessions,
)

st.set_page_config(page_title="Research Paper Deconstructor", layout="wide")
st.title("Research Paper Deconstructor")

# ---- session state bootstrap (must be first) ----
if "session_id" not in st.session_state:
    st.session_state.session_id = create_session()

if "memory" not in st.session_state:
    st.session_state.memory = build_memory([])

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# ---- Sidebar ----
with st.sidebar:
    st.subheader("Chats")

    # single New Chat button
    if st.button("➕ New Chat", key="new_chat", use_container_width=True):
        st.session_state.session_id = create_session()
        st.session_state.memory = build_memory([])
        st.session_state.vectorstore = None
        st.rerun()

    st.divider()

    # existing chats
    for s in list_sessions():
        if st.button(
            s["name"],
            key=f"session_{s['id']}",
            use_container_width=True,
        ):
            st.session_state.session_id = s["id"]
            st.session_state.memory = build_memory(load_messages(s["id"]))
            st.session_state.vectorstore = None
            st.rerun()

# ---- Upload PDFs (once per chat) ----
uploaded_files = st.file_uploader(
    "Upload research papers (PDF)",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploaded_files:
    st.session_state.vectorstore = ingest_documents(
        uploaded_files,
        st.session_state.session_id,
    )
    st.success("Documents processed")

# ---- Chat history ----
for msg in load_messages(st.session_state.session_id):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Chat input ----
question = st.chat_input("Ask a question about the documents")

if question:
    if st.session_state.vectorstore is None:
        st.warning("Please upload and process a PDF first.")
        st.stop()

    save_message(st.session_state.session_id, "user", question)
    with st.chat_message("user"):
        st.markdown(question)

    answer = ask_question(
        st.session_state.vectorstore,
        st.session_state.memory,
        question,
    )

    save_message(st.session_state.session_id, "assistant", answer)
    with st.chat_message("assistant"):
        st.markdown(answer)
