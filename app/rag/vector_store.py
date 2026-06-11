from langchain_chroma import Chroma

from app.core.logger import logger

from app.rag.retriever import VECTOR_DB_DIR, COLLECTION_NAME

def create_vector_store(chunks, embeddings):
    """
    Create a new vector store from scratch with the given chunks.
    WARNING: This will overwrite the existing collection. Use append_to_vector_store for incremental updates.
    """
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

def get_vector_store(embeddings):
    """
    Get an existing vector store instance.
    This loads the existing collection without modifying it.
    """
    try:
        vector_store = Chroma(
            persist_directory=VECTOR_DB_DIR,
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings
        )
        logger.info("Connected to existing vector store")
        return vector_store
    except Exception as e:
        logger.error(f"Failed to get vector store: {str(e)}")
        raise

def append_to_vector_store(chunks, embeddings):
    """
    Append new chunks to an existing vector store.
    This incremental approach is efficient for adding new documents without reprocessing old ones.
    """
    try:
        # Get existing vector store
        vector_store = get_vector_store(embeddings)
        
        # Add new documents to the collection
        vector_store.add_documents(chunks)
        logger.info(f"Appended {len(chunks)} new documents to vector store")
        return vector_store
    except Exception as e:
        logger.error(f"Failed to append to vector store: {str(e)}")
        raise

def document_exists_in_vector_store(filename: str) -> bool:
    """
    Check if a document with the given filename already exists in the vector store.
    Searches the metadata of all documents for matching source filename.
    
    Args:
        filename: The filename to search for in metadata
        
    Returns:
        True if document exists, False otherwise
    """
    try:
        from app.rag.embeddings import get_embedding_model
        embeddings = get_embedding_model()
        vector_store = get_vector_store(embeddings)
        
        # Get all documents from the collection
        collection = vector_store._collection
        
        # Query with no filters to get all documents and check their metadata
        if collection.count() == 0:
            logger.info(f"Vector store is empty, document {filename} does not exist")
            return False
        
        # Get all items and check metadata
        all_items = collection.get()
        
        if all_items and all_items.get('metadatas'):
            for metadata in all_items['metadatas']:
                # Check if the source filename matches
                source = metadata.get('source', '')
                # Extract just the filename from the full path
                if source.endswith(filename) or source.endswith(f"/app/uploads/{filename}"):
                    logger.info(f"Document {filename} found in vector store")
                    return True
        
        logger.info(f"Document {filename} not found in vector store")
        return False
        
    except Exception as e:
        logger.warning(f"Error checking if document exists: {str(e)}", exc_info=True)
        # On error, assume document doesn't exist to allow processing to continue
        return False

def remove_document_from_vector_store(filename: str) -> bool:
    """
    Remove all chunks belonging to a specific document from the vector store.
    Searches by filename in the metadata.
    
    Args:
        filename: The filename of the document to remove
        
    Returns:
        True if document was removed, False if not found
    """
    try:
        from app.rag.embeddings import get_embedding_model
        embeddings = get_embedding_model()
        vector_store = get_vector_store(embeddings)
        
        collection = vector_store._collection
        all_items = collection.get()
        
        if not all_items or not all_items.get('ids'):
            logger.info(f"Vector store is empty, cannot remove {filename}")
            return False
        
        # Find IDs of documents with matching filename
        ids_to_delete = []
        if all_items.get('metadatas'):
            for idx, metadata in enumerate(all_items['metadatas']):
                source = metadata.get('source', '')
                # Check if this chunk belongs to the file we're removing
                if source.endswith(filename) or source.endswith(f"/app/uploads/{filename}"):
                    ids_to_delete.append(all_items['ids'][idx])
        
        if ids_to_delete:
            # Delete the documents by ID
            collection.delete(ids=ids_to_delete)
            logger.info(f"Removed {len(ids_to_delete)} chunks for document {filename}")
            return True
        else:
            logger.info(f"No chunks found for document {filename} to remove")
            return False
            
    except Exception as e:
        logger.error(f"Failed to remove document from vector store: {str(e)}", exc_info=True)
        # On error, log but don't fail - the ingestion should continue
        return False
