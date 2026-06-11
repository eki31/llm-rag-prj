from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from app.rag.document_loader import UPLOAD_DIR
from pathlib import Path
import os

from app.services.ingest_service import ingest_documents

router = APIRouter()

#UPLOAD_DIR = "app/uploads"

@router.post("/upload")
async def upload_file(background_tasks: BackgroundTasks ,file: UploadFile = File(...)):
    safe_name = os.path.basename(file.filename or "unnamed")
    file_path = Path(UPLOAD_DIR)/ safe_name

    with open(file_path,"wb") as buffer:
        buffer.write(await file.read())

    #trigger ingestion in background
    background_tasks.add_task(ingest_documents)

    return {"message":"uploaded", "file": safe_name}

