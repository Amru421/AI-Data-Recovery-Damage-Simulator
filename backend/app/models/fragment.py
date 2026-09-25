from pydantic import BaseModel
from typing import Optional


class Fragment(BaseModel):

    fragment_id: str
    artifact_id: str

    original_index: Optional[int] = None

    size: int = 0

    sha256: Optional[str] = None

    entropy: float = 0.0

    possible_type: Optional[str] = None

    corrupted: bool = False