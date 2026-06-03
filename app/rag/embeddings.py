from langchain_huggingface import HuggingFaceEmbeddings

from app.core.logger import logger

def get_embedding_model():
    logger.info("Loading embedding model")
    
    try:
        # Suppress HuggingFace Hub warnings about missing optional config files
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            # Disable warnings for optional files that don't exist
            cache_folder=".cache",
            encode_kwargs={"normalize_embeddings": True}
        )
        logger.info("Embedding model loaded successfully")
        return embeddings
    except Exception as e:
        logger.error(f"Failed to load embedding model: {str(e)}")
        raise