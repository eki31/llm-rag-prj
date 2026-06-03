from langchain_chroma import Chroma

from app.core.logger import logger

from app.rag.retriever import VECTOR_DB_DIR, COLLECTION_NAME

def create_vector_store(chunks, embeddings):
    try:
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=VECTOR_DB_DIR,
            collection_name=COLLECTION_NAME
        )
        logger.info(f"Vector DB created with {len(chunks)} documents")
        return vector_store
    except Exception as e:
        logger.error(f"Failed to create vector store: {str(e)}")
        raise
