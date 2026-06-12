from fastapi import FastAPI
from app.routes.ai import router as ai_router
from app.routes.rag import router as rag_router
from app.routes.upload import router as upload_router
from app.routes.metrics import router as metrics_router

#for middleware for counting metrics
from time import time
from app.core.metrics import REQUEST_COUNT,REQUEST_LATENCY

app = FastAPI(
    title="AI Knowledge API",
    version="1.0.0"
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