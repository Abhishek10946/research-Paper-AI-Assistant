<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Space+Grotesk&weight=700&size=32&duration=2800&pause=800&color=818CF8&center=true&vCenter=true&width=640&lines=Read+papers.+Write+papers.;GitHub+repo+%E2%86%92+IEEE+paper+in+minutes;Chat+with+any+research+PDF" alt="Research Paper AI Assistant" />

# 📄 Research Paper AI Assistant

**An AI platform that works in both directions** — 🏗️ *generates* full IEEE research papers from GitHub repositories, and 🔍 *deconstructs* existing papers into grounded, source-cited Q&A.

<br>

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain_0.3-1C3C3C?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq_·_LLaMA_70B-F55036?style=for-the-badge)

![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-4F46E5?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-RAG_Store-7C3AED?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-Sessions-003B57?style=flat-square&logo=sqlite)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF_Export-8B0000?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production_Ready-22C55E?style=flat-square)
![License](https://img.shields.io/badge/License-Educational-3B82F6?style=flat-square)

<br>

[✨ Features](#-features) · [🎬 Demo](#-demo) · [🧠 How it works](#-how-it-works) · [⚡ Quick start](#-quick-start) · [🛠️ Tech stack](#%EF%B8%8F-tech-stack) · [🗺️ Roadmap](#%EF%B8%8F-roadmap)

</div>

---

## 🎯 Two modes, one assistant

<table>
<tr>
<td width="50%" valign="top">

### 🏗️ Constructor
**GitHub repo → IEEE paper**

Paste any public repository URL and watch the pipeline run live:

`Fetching → Indexing → Analyzing → Generating`

Up to **40 source files** are pulled via the GitHub API, embedded into **FAISS**, analyzed by **LLaMA 8B**, then **LLaMA 70B** writes all **7 IEEE sections** — exported as a formatted PDF in one click.

</td>
<td width="50%" valign="top">

### 🔍 Deconstructor
**Research PDF → grounded Q&A**

Upload papers, ask anything. Every answer is retrieved from the document itself:

`PDF → chunks → ChromaDB → top-5 → answer`

Sessions are **auto-named from the paper's content**, remember the **last 3 turns**, persist across restarts in **SQLite**, and show **source chips** under every reply — no hallucinated citations.

</td>
</tr>
</table>

<div align="center">

| 📑 7 | 📂 40 | 🎯 top-5 | 🧠 3 | 🌗 2 |
|:---:|:---:|:---:|:---:|:---:|
| IEEE sections generated | repo files indexed | RAG passages per answer | conversation turns remembered | themes — black & white |

</div>

---

## ✨ Features

- 🌗 **Dark / light theme toggle** — Streamlit has no runtime theming, so this app ships its own engine: theme state in `session_state`, injected CSS design-tokens, near-black `#0A0C12` ↔ pure white
- 📡 **Live pipeline pills** — watch each Constructor stage light up: `✓ Fetching → ● Indexing → …`
- 🏷️ **Auto-named chats** — LLaMA titles each session from the paper itself (*"Transformer Attention Mechanism"*, not *"Chat 1"*)
- 📎 **Source attribution chips** — every answer shows exactly which PDFs it came from
- 🗂️ **Section tabs before download** — preview Abstract → References, then export the IEEE PDF
- 📊 **GitHub rate-limit monitor** — remaining API calls + reset time, right in the sidebar
- ⚡ **Snappy navigation** — heavy libraries import lazily, API calls are cached, and the embedding model warms up once per server
- 🔁 **Zero re-ingestion** — PDFs are embedded once per session, survive Streamlit reruns
- 🩹 **Self-healing database** — automatic schema migration on every startup, no data loss

---

## 🎬 Demo

<div align="center">

| 🌙 Dark mode | ☀️ Light mode |
|:---:|:---:|
| <img src="docs/screenshot-dark.png" width="420" alt="Dark theme"/> | <img src="docs/screenshot-light.png" width="420" alt="Light theme"/> |

<sub>*(drop your screenshots into `docs/` — `screenshot-dark.png` & `screenshot-light.png`)*</sub>

</div>

---

## 🧠 How it works

### Constructor pipeline

```mermaid
flowchart LR
    A["🔗 GitHub URL"] --> B["📡 GitHub REST API<br/><sub>metadata · README · 40 files</sub>"]
    B --> C["🧩 FAISS Index<br/><sub>MiniLM-L6-v2 embeddings</sub>"]
    C --> D["🔬 LLaMA 3.1-8B<br/><sub>purpose · domain · stack → JSON</sub>"]
    D --> E["✍️ LLaMA 3.3-70B<br/><sub>7 IEEE sections, RAG-grounded</sub>"]
    E --> F["📄 ReportLab<br/><sub>IEEE PDF export</sub>"]

    style A fill:#4F46E5,color:#fff,stroke:none
    style F fill:#7C3AED,color:#fff,stroke:none
```

### Deconstructor pipeline

```mermaid
flowchart LR
    P["📎 PDF Upload"] --> Q["🔍 PyMuPDF<br/><sub>page parsing</sub>"]
    Q --> R["✂️ Splitter<br/><sub>1000 chars · 150 overlap</sub>"]
    R --> S[("🗃️ ChromaDB<br/><sub>per-session collection</sub>")]
    T["💬 Question"] --> S
    S --> U["🎯 Top-5 passages"]
    U --> V["🤖 LLaMA 8B<br/><sub>grounded answer + memory</sub>"]
    V --> W[("💾 SQLite<br/><sub>persistent history</sub>")]

    style P fill:#4F46E5,color:#fff,stroke:none
    style V fill:#7C3AED,color:#fff,stroke:none
```

---

## ⚡ Quick start

```bash
# 1 · Clone
git clone https://github.com/Abhishek10946/research-paper-assistant.git
cd research-paper-assistant

# 2 · Virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3 · Install
pip install -r requirements.txt

# 4 · Configure
cp .env.example .env            # add your GROQ_API_KEY

# 5 · Launch 🚀
streamlit run home.py
```

Open **http://localhost:8501** — flip the 🌙 toggle, paste a repo, go.

<details>
<summary><b>🔑 Where to get API keys</b></summary>
<br>

| Key | Source | Required |
|---|---|:---:|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) — free tier | ✅ |
| `GITHUB_TOKEN` | [github.com/settings/tokens](https://github.com/settings/tokens) — raises rate limit **60 → 5000 req/hr** | ⭐ recommended |
| `LANGCHAIN_API_KEY` | [smith.langchain.com](https://smith.langchain.com) — tracing | optional |

</details>

---

## 🛠️ Tech stack

| Layer | Technology | Why |
|---|---|---|
| 🖥️ **UI** | Streamlit + custom CSS token engine | Runtime black/white theming Streamlit doesn't offer natively |
| 🧠 **LLMs** | Groq — LLaMA 3.3-70B ✍️ · LLaMA 3.1-8B ⚡ | 70B for prose quality, 8B for fast analysis & Q&A |
| 🔗 **Orchestration** | LangChain 0.3 | Loaders, splitters, vector-store glue |
| 🔢 **Embeddings** | `all-MiniLM-L6-v2` (384-dim, normalized) | Small, fast, CPU-friendly |
| 🧩 **Vector search** | FAISS (Constructor) · ChromaDB (Deconstructor) | In-memory speed vs. persistent per-session collections |
| 📄 **PDF** | ReportLab (write) · PyMuPDF (read) | IEEE-styled export · reliable text extraction |
| 💾 **Persistence** | SQLite + SQLAlchemy ORM | Sessions & messages with auto-migration |

<details>
<summary><b>📁 Project structure</b></summary>

```
research-paper-assistant/
├── home.py                      # Landing — hero, mode cards, workflow
├── requirements.txt
├── .env.example                 # → rename to .env, add keys
├── .streamlit/config.toml       # Base dark theme (no load flicker)
│
├── pages/
│   ├── Constructor.py           # Repo → paper UI (pipeline pills, tabs, PDF)
│   └── Deconstructor.py         # PDF chat UI (sessions, chips, memory)
│
├── constructor/
│   ├── github_loader.py         # REST API — tree, files, rate limit
│   ├── vectorstore.py           # FAISS index builder
│   ├── analysis.py              # LLaMA 8B → structured JSON
│   ├── paper_generator.py       # LLaMA 70B × 7 sections
│   └── pdf_builder.py           # ReportLab IEEE export
│
├── deconstructor/
│   ├── ingestion.py             # PyMuPDF → splitter → ChromaDB
│   ├── retriever.py             # top-5 similarity search
│   ├── memory.py                # last-3-turns context
│   ├── llm.py                   # grounded ask() + name_session()
│   └── database.py              # SQLAlchemy ORM + auto-migration
│
├── shared/
│   ├── ui.py                    # ★ theme engine + components
│   ├── config.py · llm.py · embeddings.py · text_splitter.py
│
└── data/                        # runtime — chroma/ · faiss_cache/ · sessions.db
```

</details>

<details>
<summary><b>🩺 Troubleshooting</b></summary>
<br>

**`GitHub API rate limit exceeded`** → add `GITHUB_TOKEN` to `.env` (60 → 5000 req/hr) or wait for the reset time shown in the sidebar.

**`no such column: sessions.last_active`** → just restart; `_migrate()` in `database.py` adds the column automatically without touching data.

**Slow first load (4–10 s)** → the ~90 MB MiniLM model downloads once, then `@st.cache_resource` makes every later start instant.

**PDF not processing** → the file must contain selectable text (scanned images won't work); keep files under 50 MB.

</details>

---

## 🗺️ Roadmap

- [x] IEEE paper generation from any public repo
- [x] RAG-grounded PDF Q&A with source chips
- [x] 🌗 Runtime dark/light theme engine
- [x] Auto-named, persistent, deletable chat sessions
- [x] Automatic DB migration on startup
- [ ] 🐳 Docker image + `docker-compose.yml`
- [ ] ☁️ One-click Streamlit Cloud deploy
- [ ] 🔐 Private repos via OAuth
- [ ] 📚 APA / MLA / ACM formats
- [ ] 🕸️ Citation graph generation
- [ ] 🆚 Multi-paper comparative analysis

---

## 👨‍💻 Author

<div align="center">

**Abhishek Kale**
B.Tech Electrical Engineering · COEP Technological University, Pune

[![GitHub](https://img.shields.io/badge/GitHub-Abhishek10946-181717?style=for-the-badge&logo=github)](https://github.com/Abhishek10946)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/abhishek-kale-889437205)

</div>

---

<div align="center">

### ⭐ If this project helped you, a star means a lot!

<sub>📜 Educational & research use · respect the licenses of input repositories and the Groq / LangChain terms of service</sub>

<br><br>

<img src="https://img.shields.io/badge/Built_with-🧠_+_☕-4F46E5?style=for-the-badge" alt="Built with brains and coffee"/>

</div>
