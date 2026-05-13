from langchain_community.vectorstores import Chroma

from app.core.logger import logger

VECTOR_DB_DIR = "app/vector_db"

def create_vector_store(chunks,embeddings):
    logger.info("Creating vector DB")

    vector_store=Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory=VECTOR_DB_DIR)
    logger.info("Vector DB created")

    return vector_store
