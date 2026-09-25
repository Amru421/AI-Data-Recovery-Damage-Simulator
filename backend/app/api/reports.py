from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[3]
GROUND_TRUTH = BASE_DIR / "data" / "ground_truth.json"


@router.get("/report/{artifact_id}")
def get_report(artifact_id: str):

    if not GROUND_TRUTH.exists():
        return {
            "artifact_id": artifact_id,
            "report": "No recovery report available."
        }

    with open(GROUND_TRUTH, "r", encoding="utf-8") as file:
        data = json.load(file)

    for artifact in data.get("artifacts", []):

        if artifact.get("artifact_id") == artifact_id:

            return {
                "artifact_id": artifact_id,
                "report": {
                    "filename": artifact.get("filename"),
                    "file_type": artifact.get("file_type"),
                    "original_sha256": artifact.get("original_sha256"),
                    "missing_fragments": artifact.get("missing_fragments", []),
                    "corrupted_fragments": artifact.get(
                        "corrupted_fragments", []
                    )
                }
            }

    return {
        "artifact_id": artifact_id,
        "report": "Artifact not found."
    }