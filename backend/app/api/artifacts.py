from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[3]
GROUND_TRUTH = BASE_DIR / "data" / "ground_truth.json"
UPLOAD_INDEX = BASE_DIR / "data" / "uploads.json"


@router.get("/artifacts/{job_id}")
def get_artifacts(job_id: str):

    if not GROUND_TRUTH.exists():
        return {
            "job_id": job_id,
            "artifacts": []
        }

    with open(GROUND_TRUTH, "r", encoding="utf-8") as file:
        data = json.load(file)

    artifacts = data.get("artifacts", [])

    if UPLOAD_INDEX.exists():
        with open(UPLOAD_INDEX, "r", encoding="utf-8") as file:
            uploads = json.load(file)

        for upload in uploads:
            analysis = upload.get("analysis", {})
            artifacts.append({
                "artifact_id": upload.get("file_id"),
                "filename": upload.get("filename"),
                "file_type": analysis.get("classification", "Unknown"),
                "total_fragments": analysis.get("fragment_count", 0),
                "missing_fragments": [],
                "corrupted_fragments": [],
                "integrity_score": analysis.get("integrity_score", 0),
                "recovery_confidence": analysis.get("recovery_confidence", 0),
                "recoverability": analysis.get("recoverability"),
                "uploaded_at": upload.get("uploaded_at"),
                "source": "uploaded",
            })

    return {
        "job_id": job_id,
        "artifacts": artifacts
    }


@router.get("/artifact/{artifact_id}")
def get_artifact(artifact_id: str):

    if not GROUND_TRUTH.exists():
        return {
            "artifact_id": artifact_id,
            "found": False
        }

    with open(GROUND_TRUTH, "r", encoding="utf-8") as file:
        data = json.load(file)

    for artifact in data.get("artifacts", []):

        if artifact.get("artifact_id") == artifact_id:

            return {
                "found": True,
                "artifact": artifact
            }

    return {
        "artifact_id": artifact_id,
        "found": False
    }


@router.get("/fragments/{artifact_id}")
def get_fragments(artifact_id: str):

    if not GROUND_TRUTH.exists():
        return {
            "artifact_id": artifact_id,
            "fragments": []
        }

    with open(GROUND_TRUTH, "r", encoding="utf-8") as file:
        data = json.load(file)

    for artifact in data.get("artifacts", []):

        if artifact.get("artifact_id") == artifact_id:

            return {
                "artifact_id": artifact_id,
                "fragments": artifact.get("fragments", [])
            }

    return {
        "artifact_id": artifact_id,
        "fragments": []
    }