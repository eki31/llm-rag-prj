from fastapi import APIRouter
from app.models.schemas import DocumentQuestionRequest
from app.services.rag_service import ask_document
from app.services.ingest_service import ingest_documents

router = APIRouter()

@router.post("/load-docs")
async def load_docs():
    """
    Load PDF documents from uploads folder, chunk them, 
    create embeddings, and store in vector DB.
    """
    result = await ingest_documents()
    return result

@router.post("/ask-doc")
async def ask_doc(request: DocumentQuestionRequest):
    response = await ask_document(request.question)

    return response