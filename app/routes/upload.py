from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from app.rag.document_loader import UPLOAD_DIR
from pathlib import Path
import os

from app.services.ingest_service import ingest_documents

router = APIRouter()

#UPLOAD_DIR = "app/uploads"

@router.post("/upload")
async def upload_file(background_tasks: BackgroundTasks ,file: UploadFile = File(...)):
    """
    Upload single PDF documents, load additional file, chunk them,
    create embeddings, and append it to vector DB.
    """
    safe_name = os.path.basename(file.filename or "unnamed")
    file_path = Path(UPLOAD_DIR)/ safe_name

    with open(file_path,"wb") as buffer:
        buffer.write(await file.read())

    #trigger ingestion in background for this specific file
    background_tasks.add_task(ingest_documents, safe_name)

    return {"message":"uploaded", "file": safe_name}

