from fastapi import APIRouter
from app.models.schemas import DocumentQuestionRequest
from app.services.rag_service import ask_document

router = APIRouter()

@router.post("/ask-doc")
async def ask_doc(request: DocumentQuestionRequest):
    response = await ask_document(request.question)

    return response