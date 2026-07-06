"""Landing page — hero, mode cards, workflow overview."""
from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="Research Paper AI Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

from shared.ui import apply_theme, badges, feature_card, hero, sidebar_header

sidebar_header()
apply_theme()

with st.sidebar:
    st.caption("MODES")
    if st.button("🏗️ Constructor", use_container_width=True, type="secondary"):
        st.switch_page("pages/Constructor.py")
    if st.button("🔍 Deconstructor", use_container_width=True, type="secondary"):
        st.switch_page("pages/Deconstructor.py")

# ------------------------------------------------------------------ hero ----
hero(
    "AI RESEARCH TOOLKIT",
    'Read <em>papers</em>. Write <span class="grad">papers</span>.',
    "One assistant, two directions: turn any GitHub repository into a full "
    "IEEE-style paper, or upload existing papers and interrogate them with "
    "retrieval-grounded Q&A.",
)

# ------------------------------------------------------------ mode cards ----
c1, c2 = st.columns(2, gap="medium")

with c1:
    feature_card(
        "🏗️",
        "Constructor — repo → IEEE paper",
        "Fetches up to 40 source files from a public GitHub repository, indexes "
        "them in FAISS, analyzes the codebase with LLaMA 8B, then writes all "
        "seven IEEE sections with LLaMA 70B and exports a formatted PDF.",
    )
    st.write("")
    if st.button("Open Constructor →", use_container_width=True, key="go_con"):
        st.switch_page("pages/Constructor.py")

with c2:
    feature_card(
        "🔍",
        "Deconstructor — PDF → grounded Q&A",
        "Ingests your research PDFs into ChromaDB, auto-names each chat from the "
        "paper's content, remembers the last three turns, and answers strictly "
        "from the retrieved passages — with source chips under every reply.",
    )
    st.write("")
    if st.button("Open Deconstructor →", use_container_width=True, key="go_dec"):
        st.switch_page("pages/Deconstructor.py")

st.write("")
st.write("")

# -------------------------------------------------------------- workflow ----
st.markdown("#### How Constructor works")
w1, w2, w3, w4 = st.columns(4, gap="small")
for col, num, label, desc in (
    (w1, "1", "Fetch", "Repo tree, README and code via the GitHub REST API"),
    (w2, "2", "Index", "Chunks embedded with MiniLM into a FAISS store"),
    (w3, "3", "Analyze", "LLaMA 8B extracts purpose, domain and stack as JSON"),
    (w4, "4", "Generate", "LLaMA 70B writes 7 sections from retrieved context"),
):
    with col:
        st.markdown(
            f'<div class="rp-card"><span class="rp-step-num">{num}</span>'
            f"<b>{label}</b><p>{desc}</p></div>",
            unsafe_allow_html=True,
        )

st.write("")
st.markdown("#### Under the hood")
badges(
    [
        "Groq · LLaMA 3.3-70B",
        "LLaMA 3.1-8B",
        "LangChain 0.3",
        "FAISS",
        "ChromaDB",
        "all-MiniLM-L6-v2",
        "ReportLab",
        "PyMuPDF",
        "SQLite",
        "Streamlit",
    ]
)

st.write("")
st.caption("Built by Abhishek Kale · Educational and research use")
