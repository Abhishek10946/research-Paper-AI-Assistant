"""Constructor — GitHub repository → IEEE paper."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

st.set_page_config(page_title="Constructor · RP Assistant", page_icon="🏗️", layout="wide")

from constructor.analysis import analyze_repository
from constructor.github_loader import fetch_repository, get_rate_limit
from constructor.paper_generator import SECTIONS, generate_paper
from constructor.pdf_builder import build_pdf
from constructor.vectorstore import build_index
from shared.ui import apply_theme, hero, sidebar_header, step_pills

sidebar_header()
apply_theme()

STEPS = ["Fetching", "Indexing", "Analyzing", "Generating"]

# ----------------------------------------------------------------- sidebar --
with st.sidebar:
    st.caption("GITHUB API")
    try:
        rl = get_rate_limit()
        st.metric("Requests remaining", f"{rl['remaining']} / {rl['limit']}")
        st.caption(f"Resets {rl['reset']:%H:%M:%S}")
        if rl["limit"] <= 60:
            st.caption("Add a GITHUB_TOKEN in .env for 5000 req/hour.")
    except Exception:
        st.caption("Rate limit unavailable (offline?)")
    st.divider()
    if st.button("← Home", use_container_width=True, type="secondary"):
        st.switch_page("home.py")

# -------------------------------------------------------------------- hero --
hero(
    "CONSTRUCTOR",
    'GitHub repo → <span class="grad">IEEE paper</span>',
    "Paste a public repository. The pipeline fetches up to 40 files, indexes them "
    "in FAISS, analyzes the codebase with LLaMA 8B, and writes all seven sections "
    "with LLaMA 70B.",
)

# ------------------------------------------------------------------ inputs --
repo_url = st.text_input(
    "GitHub repository URL",
    placeholder="https://github.com/owner/repository",
)
c1, c2 = st.columns(2)
author = c1.text_input("Author name", placeholder="Abhishek Kale")
institution = c2.text_input("Institution", placeholder="COEP Technological University, Pune")

generate = st.button("🚀 Generate IEEE paper", type="primary")

pills_slot = st.empty()
status_slot = st.empty()


def _show_steps(i: int, error: bool = False) -> None:
    pills_slot.markdown(step_pills(STEPS, i, error), unsafe_allow_html=True)


if generate:
    if not repo_url.strip():
        st.warning("Paste a GitHub repository URL first.")
    else:
        st.session_state.pop("paper", None)
        st.session_state.pop("pdf_bytes", None)
        step = 0
        try:
            _show_steps(step)
            with status_slot, st.spinner("Fetching repository files…"):
                fetched = fetch_repository(repo_url)

            step = 1
            _show_steps(step)
            with status_slot, st.spinner("Building FAISS index…"):
                vs = build_index(fetched)

            step = 2
            _show_steps(step)
            with status_slot, st.spinner("Analyzing codebase with LLaMA 8B…"):
                analysis = analyze_repository(fetched)

            step = 3
            _show_steps(step)
            section_names = [s[0] for s in SECTIONS]
            with status_slot, st.spinner("Writing sections with LLaMA 70B…"):
                sections = generate_paper(
                    vs, analysis, fetched["meta"],
                    progress=lambda name: status_slot.caption(
                        f"Writing {name}… ({section_names.index(name) + 1}/{len(section_names)})"
                    ),
                )

            _show_steps(len(STEPS))  # all done
            status_slot.empty()
            st.session_state.paper = {
                "meta": fetched["meta"],
                "analysis": analysis,
                "sections": sections,
            }
            st.toast("Paper generated", icon="✅")
        except Exception as e:
            _show_steps(step, error=True)
            status_slot.empty()
            st.error(str(e))

# ----------------------------------------------------------------- results --
paper = st.session_state.get("paper")
if paper:
    meta, sections = paper["meta"], paper["sections"]
    st.write("")
    st.markdown(
        f"#### 📄 {meta['full_name']} "
        f"<span class='rp-chip'>⭐ {meta['stars']}</span> "
        f"<span class='rp-chip'>{meta['language'] or 'code'}</span>",
        unsafe_allow_html=True,
    )

    tabs = st.tabs(list(sections.keys()))
    for tab, (name, text) in zip(tabs, sections.items()):
        with tab:
            st.markdown(text)

    if "pdf_bytes" not in st.session_state:
        title = f"{meta['full_name'].split('/')[-1].replace('-', ' ').title()}: Design and Implementation"
        st.session_state.pdf_bytes = build_pdf(
            title,
            author or "Anonymous",
            institution or "Independent Researcher",
            sections,
        )

    st.write("")
    st.download_button(
        "⬇️ Download IEEE PDF",
        data=st.session_state.pdf_bytes,
        file_name=f"{meta['full_name'].split('/')[-1]}_ieee_paper.pdf",
        mime="application/pdf",
    )
else:
    st.write("")
    st.caption(
        "Tips: repos with a good README produce better papers · start with repos "
        "under 50 files · the sidebar shows your GitHub API budget."
    )
