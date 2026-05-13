from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.logger import logger

def chunk_documents(documents):
    logger.info("Chunking documents")

    splitter = (RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100))

    chunks = splitter.split_documents(documents)

    logger.info(f"Created {len(chunks)} chunks")

    return chunks