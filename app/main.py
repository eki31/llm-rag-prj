from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core.logger import logger
from app.rag.retriever import get_retriever
from app.routes.ai import router as ai_router
from app.routes.rag import router as rag_router
from app.routes.upload import router as upload_router
from app.routes.metrics import router as metrics_router

#for middleware for counting metrics
from time import time
from app.core.metrics import REQUEST_COUNT,REQUEST_LATENCY

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the embedding model and vector store before accepting requests,
    # so the first user doesn't wait for the cold load (~14s on a slow CPU).
    # Uvicorn only starts serving (including /health) once this finishes.
    try:
        get_retriever().invoke("warm up")
        logger.info("Retriever warmed up at startup")
    except Exception as e:
        # Don't block startup; the retriever loads lazily on the first request instead
        logger.error(f"Retriever warm-up failed, will retry on first request: {str(e)}")
    yield


app = FastAPI(
    title="AI Knowledge API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ai_router)
app.include_router(rag_router)
app.include_router(upload_router)
app.include_router(metrics_router)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time()
    REQUEST_COUNT.inc()
    response = await call_next(request)
    duration = (time()-start_time)
    REQUEST_LATENCY.observe(duration)

    return response