from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from app.core.logger import logger

UPLOAD_DIR = "app/uploads"

def load_documents():
    logger.info("Loading PDF documents")

    documents = []
    pdf_files = Path(UPLOAD_DIR).glob("*.pdf")

    for pdf_file in pdf_files:
        logger.info(f"Loading {pdf_file}")

        loader = PyPDFLoader(str(pdf_file))
        docs = loader.load()
        documents.extend(docs)

    logger.info(f"Loaded {len(documents)} document pages")

    return documents