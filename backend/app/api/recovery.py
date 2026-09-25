from fastapi import APIRouter
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[3]

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from app.services.recovery_service import RecoveryService

router = APIRouter()

service = RecoveryService()


@router.post("/scan/{job_id}")
def scan_job(job_id: str):

    result = service.scan(job_id)

    return {
        "job_id": job_id,
        "status": "scan_completed",
        "result": result
    }


@router.get("/scan/{job_id}")
def scan_status(job_id: str):

    return {
        "job_id": job_id,
        "status": "completed"
    }


@router.post("/recover/{job_id}")
def recover_job(job_id: str):

    result = service.recover(job_id)

    return {
        "job_id": job_id,
        "status": "recovery_completed",
        "result": result
    }