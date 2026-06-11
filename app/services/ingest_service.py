from typing import Optional
from app.rag.document_loader import load_documents, load_single_document, UPLOAD_DIR
from app.rag.chunker import chunk_documents
from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import (
    create_vector_store, 
    append_to_vector_store,
    document_exists_in_vector_store,
    remove_document_from_vector_store
)
from app.rag.retriever import reset_retriever
from app.core.logger import logger

async def ingest_single_document(filename: str):
    """
    Load a single document, chunk it, embed it, and append to existing vector DB.
    This is called when a new file is uploaded.
    Returns a status dict with result information.
    """
    try:
        logger.info(f"Starting ingestion for single document: {filename}")
        
        # Check if document already exists in vector store
        doc_exists = document_exists_in_vector_store(filename)
        if doc_exists:
            logger.info(f"Document {filename} already exists in vector store. Removing old version...")
            remove_document_from_vector_store(filename)
        
        # Load single document
        documents = load_single_document(f"{UPLOAD_DIR}/{filename}")
        
        if not documents:
            logger.warning(f"No documents loaded for file: {filename}")
            return {
                "status": "warning",
                "message": f"No documents loaded for file: {filename}",
                "filename": filename,
                "documents_loaded": 0,
                "chunks_created": 0
            }
        
        # Chunk documents
        chunks = chunk_documents(documents)
        
        if not chunks:
            logger.warning(f"No chunks created from {filename}")
            return {
                "status": "warning",
                "message": f"No chunks created from {filename}",
                "filename": filename,
                "documents_loaded": len(documents),
                "chunks_created": 0
            }
        
        # Get embedding model
        embeddings = get_embedding_model()
        
        # Append to existing vector store
        append_to_vector_store(chunks, embeddings)
        
        # Reset retriever instance to force reload
        reset_retriever()
        
        logger.info(f"Single document ingestion completed for {filename}")
        
        return {
            "status": "success",
            "message": f"Document {filename} ingested successfully",
            "filename": filename,
            "documents_loaded": len(documents),
            "chunks_created": len(chunks)
        }
        
    except Exception as e:
        logger.error(f"Single document ingestion failed for {filename}: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"Document ingestion failed: {str(e)}",
            "filename": filename,
            "documents_loaded": 0,
            "chunks_created": 0
        }

async def ingest_documents(filename: Optional[str] = None):
    """
    Ingest documents into vector DB.
    
    If filename is provided: Load and ingest only that specific document (called on upload).
    If filename is None: Load all documents from uploads folder (batch operation).
    
    Returns a status dict with result information.
    """
    # If a specific filename is provided, use single document ingestion
    if filename:
        return await ingest_single_document(filename)
    
    # Otherwise, perform batch ingestion of all documents
    try:
        logger.info("Starting batch document ingestion pipeline")
        
        # Load all documents
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
        
        # Create vector store (for batch operation, we recreate from scratch)
        create_vector_store(chunks, embeddings)
        
        # Reset retriever instance to force reload
        reset_retriever()
        
        logger.info("Batch document ingestion completed successfully")
        
        return {
            "status": "success",
            "message": "Documents ingested successfully",
            "documents_loaded": len(documents),
            "chunks_created": len(chunks)
        }
        
    except Exception as e:
        logger.error(f"Batch document ingestion failed: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"Document ingestion failed: {str(e)}",
            "documents_loaded": 0,
            "chunks_created": 0
        }