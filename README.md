# Research-Paper-AI-Assistant

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

# Architecture Diagrams
## High Level Architecture Diagram
![System Architecture](docs/high_level_architecture.png)
## Low Level Architecture Diagram
![System Architecture](docs/low_level_architecture.png)

## Project Structure & Additionally Architecture diagrams high level and low level both are in docs\
```bash

research-paper-assistant/
│
├── app.py
├── Home.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── pages/
│   ├── Constructor.py
│   └── Deconstructor.py
│
├── constructor/
│   ├── __init__.py
│   ├── app.py
│   ├── analysis.py
│   ├── github_loader.py
│   ├── paper_generator.py
│   ├── pdf_builder.py
│   ├── vectorstore.py
│   └── utils.py
│
├── deconstructor/
│   ├── __init__.py
│   ├── app.py
│   ├── ingestion.py
│   ├── retriever.py
│   ├── memory.py
│   ├── llm.py
│   └── database.py
│
├── shared/
│   ├── __init__.py
│   ├── embeddings.py
│   ├── text_splitter.py
│   └── config.py
│
└── data/
    ├── chroma/
    ├── faiss_cache/
    └── sessions.db

```
---

### First of all we need to fix our API KEYs into .env file

---


1. Environment Setup

- Before running the application, configure environment variables using a .env file.

- Create a .env file using .env.example and add the following:

- GROQ_API_KEY=your_groq_api_key
- LANGCHAIN_PROJECT=researchpaper-assistant

- Get your Groq API key from:
- https://console.groq.com

- Do not commit real API keys to the repository.


2. Installation

2.1 Clone the Repository

- git clone <repository-url>
- cd research-paper-assistant

2.2 Create a Virtual Environment

```bash
python -m venv venv

Activate the environment (Windows):

venv\Scripts\activate

Activate the environment (Linux / macOS):

source venv/bin/activate
```

2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

3. Run the Application
```bash
streamlit run home.py
```
- Open the application in your browser:

- http://localhost:8501


## 4. Usage Guide

# 4.1 Constructor Verification

- Step 1: Open Constructor
- Step 2: Paste a small public GitHub repository URL
- Step 3: Enter Author Name and Institution
- Step 4: Click Generate
- Step 5: Verify the PDF download

- Successful PDF generation confirms Constructor functionality.

## 4.2 Deconstructor Usage

- Step 1: Open Deconstructor
- Step 2: Click New Chat
- Step 3: Upload one or more research paper PDFs
- Step 4: Ask questions using the chat interface
- Step 5: Start a new chat for independent document sessions

- Each chat session is persistent and isolated.


## 5. Design Principles

- 1. Modular and maintainable architecture
- 2. Stateless UI with persistent backend memory
- 3. Transparent logic without hard-coded assumptions
- 4. Scalable for both local and cloud deployments

------------------------------------------------------------

## 6. Notes

- 1. Large repositories may take longer to process
- 2. GitHub API rate limits apply for unauthenticated requests
- 3. First embedding run may be slower due to model initialization


## 7. License

- This project is intended for educational and research use.

- Users must ensure compliance with individual GitHub repository licenses when generating research papers from source code.

 
## 8. Future Enhancements

- 1. Citation graph generation
- 2. Multi-paper comparative analysis
- 3. Docker and cloud-native deployment
- 4. Support for additional academic templates beyond IEEE
