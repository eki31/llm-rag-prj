from fastapi import APIRouter

from app.core.logger import logger

from app.models.schemas import (
    QuestionRequest,
    SummarizeRequest
)

from app.services.openrouter_service import (
    ask_llm,
    summarize_text
)

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.post("/ask")
def ask_question(request: QuestionRequest):

    logger.info(f"Question received: {request.question}")

    response = ask_llm(request.question)

    return response

@router.post("/summarize")
def summarize(request: SummarizeRequest):

    logger.info(f"Text received: {request.text}")

    response = summarize_text(request.text)

    return response