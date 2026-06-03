from langchain_chroma import Chroma

from app.rag.embeddings import get_embedding_model
from app.core.logger import logger

VECTOR_DB_DIR = "app/vector_db"
COLLECTION_NAME = "documents"

retriever_instance = None

def get_retriever():

    global retriever_instance
    if retriever_instance:
        return retriever_instance

    try:
        embeddings = get_embedding_model()

        vector_store = Chroma(
            persist_directory=VECTOR_DB_DIR,
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings
        )
        
        # Check if vector store has any documents
        doc_count = vector_store._collection.count()
        if doc_count == 0:
            logger.warning("Vector store is empty - no documents loaded")
        else:
            logger.info(f"Vector store loaded with {doc_count} documents")

        retriever_instance = vector_store.as_retriever(search_kwargs={"k": 5})
        logger.info("Retriever initialized successfully")
        
        return retriever_instance
    except Exception as e:
        logger.error(f"Failed to initialize retriever: {str(e)}")
        raise