from fastapi import FastAPI
from app.routes.ai import router as ai_router
from app.routes.rag import router as rag_router

app = FastAPI(
    title="AI Knowledge API",
    version="1.0.0"
)

app.include_router(ai_router)
app.include_router(rag_router)