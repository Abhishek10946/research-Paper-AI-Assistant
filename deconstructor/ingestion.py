import os
import tempfile
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from shared.embeddings import get_embeddings

CHROMA_DIR = "./data/chroma"


def ingest_documents(files, session_id: str):
    embeddings = get_embeddings()
    vectorstore = Chroma(
        collection_name=session_id,
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    docs = []

    for f in files:
        tmp_path = os.path.join(tempfile.gettempdir(), f.name)
        with open(tmp_path, "wb") as out:
            out.write(f.getvalue())

        loader = PyMuPDFLoader(tmp_path)
        loaded_docs = loader.load()
        docs.extend(splitter.split_documents(loaded_docs))

    if docs:
        vectorstore.add_documents(docs)
        vectorstore.persist()

        
    return vectorstore    
