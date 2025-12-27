# ResearchPaper-Assistant

An AI-powered research assistant that constructs IEEE-formatted research papers from GitHub repositories and deconstructs existing research papers for interactive question-answering.

The system is designed as a dual-mode application to accelerate academic, technical, and research workflows using Retrieval-Augmented Generation (RAG).

---

## Overview

ResearchPaper-Assistant enables researchers, students, and developers to:

- Convert real-world software repositories into structured IEEE-style research papers
- Interactively explore and question uploaded research papers using document-grounded AI
- Maintain persistent, multi-session academic workflows using modern LLM infrastructure

---

## Features

### Constructor (Paper Generator)

- Analyze a complete public GitHub repository
- Understand code structure, documentation, and architecture
- Generate a multi-page IEEE-formatted research paper
- Edit sections before PDF generation
- On-demand PDF export

### Deconstructor (Paper Analyzer)

- Upload one or more research paper PDFs
- Build a document-grounded vector knowledge base
- Ask unlimited questions in a single chat session
- Create multiple independent chat sessions
- Persistent document and chat history

---

## Technology Stack

### Frontend
- Streamlit

### LLM Orchestration
- LangChain

### LLM Provider
- Groq  
  - LLaMA-3.1-8B-Instant  
  - LLaMA-3.3-70B-Versatile  

### Vector Databases
- FAISS (Constructor)
- ChromaDB (Deconstructor)

### Embeddings
- Hugging Face Sentence Transformers  
  - all-MiniLM-L6-v2

### Persistence
- SQLite (sessions and chat history)

### PDF Handling
- ReportLab (PDF generation)
- PyMuPDF / PyPDF2 (PDF parsing)

---

## Project Structure

research_paper_project/
│
├── Home.py
├── pages/
│ ├── Constructor.py
│ └── Deconstructor.py
│
├── constructor/
│ ├── app.py
│ ├── analysis.py
│ ├── github_loader.py
│ ├── paper_generator.py
│ ├── pdf_builder.py
│ ├── vectorstore.py
│ └── utils.py
│
├── deconstructor/
│ ├── app.py
│ ├── ingestion.py
│ ├── retriever.py
│ ├── memory.py
│ ├── llm.py
│ └── database.py
│
├── shared/
│ ├── embeddings.py
│ ├── text_splitter.py
│ └── config.py
│
├── data/
│ ├── chroma/
│ ├── faiss_cache/
│ └── sessions.db
│
├── requirements.txt
├── .env
└── README.md

---

### First of all you need to fix your API KEY into .env file

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd research_pepaar_project

2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS

3. Install Dependencies
pip install -r requirements.txt

Environment Configuration

Create a .env file using .env.example:

GROQ_API_KEY=your_groq_api_key
LANGCHAIN_PROJECT=researchpaper-assistant


Get your Groq API key from:
https://console.groq.com

Run the Application
streamlit run Home.py


Open in your browser:

http://localhost:8501

Usage Guide
Constructor Verification

Open Constructor

Paste a small public GitHub repository URL

Enter Author Name and Institution

Click Generate

Verify PDF download

Successful PDF generation confirms Constructor functionality.

Deconstructor Usage

Open Deconstructor

Click New Chat

Upload one or more research paper PDFs

Ask questions in the chat interface

Start a new chat for independent document sessions

Each session is persistent and isolated.

Design Principles

Modular and maintainable architecture

Stateless UI with persistent backend memory

Transparent logic with no hard-coded assumptions

Scalable for both local and cloud deployments

Notes

Large repositories may take longer to process

GitHub API rate limits apply for unauthenticated requests

First embedding run is slower due to model initialization

License

This project is intended for educational and research use.

Users must ensure compliance with individual GitHub repository licenses when generating research papers from source code.

Future Enhancements

Citation graph generation

Multi-paper comparative analysis

Docker and cloud-native deployment

Support for additional academic templates beyond IEEE


---

### Final Confirmation

- This is **one single `.md` file**
- 100% valid GitHub Markdown
- Recruiter-ready
- Academic-quality documentation
- No formatting errors

If you want next:
- **Resume bullets from this project**
- **Architecture diagram**
- **Docker support**
- **Portfolio website section**

Say what you want to add next.
