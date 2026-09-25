from pydantic import BaseModel
from typing import Optional


class Artifact(BaseModel):

    artifact_id: str
    filename: str
    file_type: Optional[str] = None
    size: int = 0
    sha256: Optional[str] = None