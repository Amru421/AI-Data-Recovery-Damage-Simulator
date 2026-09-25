from pydantic import BaseModel
from typing import List


class RecoveryResult(BaseModel):

    artifact_id: str

    recovery_confidence: float = 0.0

    integrity_score: float = 0.0

    missing_fragments: List[str] = []

    corrupted_fragments: List[str] = []

    recovered_file: str = ""