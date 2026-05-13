from langchain_huggingface import HuggingFaceEmbeddings

from app.core.logger import logger

def get_embedding_model():
    logger.info("Loading embedding model")

    embeddings = (HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))

    return embeddings