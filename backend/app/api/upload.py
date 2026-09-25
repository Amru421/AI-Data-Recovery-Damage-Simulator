from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import json
import uuid
from datetime import datetime, timezone

from app.ai.analyzer import analyze_uploaded_file

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[3]
UPLOAD_DIR = BASE_DIR / "data" / "original"
UPLOAD_INDEX = BASE_DIR / "data" / "uploads.json"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A filename is required"
        )

    file_id = str(uuid.uuid4())
    safe_name = f"{file_id}_{Path(file.filename).name}"

    destination = UPLOAD_DIR / safe_name

    contents = await file.read()

    analysis = analyze_uploaded_file(
        file.filename,
        contents,
    )

    with open(destination, "wb") as output:
        output.write(contents)

    record = {
        "file_id": file_id,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "filename": file.filename,
        "stored_as": safe_name,
        "content_type": file.content_type or "application/octet-stream",
        "size": len(contents),
        "analysis": analysis,
    }

    records = []
    if UPLOAD_INDEX.exists():
        with open(UPLOAD_INDEX, "r", encoding="utf-8") as index_file:
            records = json.load(index_file)

    records.append(record)
    with open(UPLOAD_INDEX, "w", encoding="utf-8") as index_file:
        json.dump(records, index_file, indent=2)

    return {
        "status": "uploaded",
        **record
    }


@router.get("/uploads")
def get_uploads():

    if not UPLOAD_INDEX.exists():
        return {"uploads": []}

    with open(UPLOAD_INDEX, "r", encoding="utf-8") as index_file:
        return {"uploads": json.load(index_file)}