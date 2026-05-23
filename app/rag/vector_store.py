from langchain_chroma import Chroma

from app.core.logger import logger

from pathlib import Path

from app.rag.retriever import VECTOR_DB_DIR

#VECTOR_DB_DIR = "app/vector_db"

def create_vector_store(chunks,embeddings):
    vector_path = Path(VECTOR_DB_DIR)
    #Check if DB exists
    if vector_path.exists():
        chroma_files = list(vector_path.glob("*"))
        if chroma_files:
            logger.info("Vector DB already exists. Skipping creation.")
            vector_store=Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
            return vector_store

    logger.info("Creating new vector DB")

    vector_store=Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory=VECTOR_DB_DIR)
    logger.info("Vector DB created")

    return vector_store
