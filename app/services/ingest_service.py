from app.rag.document_loader import load_documents
from app.rag.chunker import chunk_documents
from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import create_vector_store
from app.rag.retriever import retriever_instance
from app.core.logger import logger

async def ingest_documents():
    """
    Load documents, chunk them, embed them, and store in vector DB.
    Returns a status dict with result information.
    """
    try:
        logger.info("Starting document ingestion pipeline")
        
        # Load documents
        documents = load_documents()
        
        if not documents:
            logger.warning("No PDF documents found in uploads folder")
            return {
                "status": "warning",
                "message": "No PDF documents found in uploads folder",
                "documents_loaded": 0,
                "chunks_created": 0
            }
        
        # Chunk documents
        chunks = chunk_documents(documents)
        
        if not chunks:
            logger.warning("No chunks created from documents")
            return {
                "status": "warning",
                "message": "No chunks created from documents",
                "documents_loaded": len(documents),
                "chunks_created": 0
            }
        
        # Get embedding model
        embeddings = get_embedding_model()
        
        # Create and populate vector store
        vector_store = create_vector_store(chunks, embeddings)
        
        # Reset retriever instance to force reload
        global retriever_instance
        retriever_instance = None
        
        logger.info("Document ingestion completed successfully")
        
        return {
            "status": "success",
            "message": "Documents ingested successfully",
            "documents_loaded": len(documents),
            "chunks_created": len(chunks)
        }
        
    except Exception as e:
        logger.error(f"Document ingestion failed: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"Document ingestion failed: {str(e)}",
            "documents_loaded": 0,
            "chunks_created": 0
        }
