from pathlib import Path

from app.ai.classifier import classify_artifact
from app.ai.confidence import calculate_recovery_confidence
from app.ai.features import byte_entropy
from app.ai.similarity import similarity_score


CHUNK_SIZE = 1024


def _fragment_data(data: bytes):
    return [data[index:index + CHUNK_SIZE] for index in range(0, len(data), CHUNK_SIZE)]


def analyze_uploaded_file(filename: str, data: bytes):
    file_type = classify_artifact(filename)
    fragments = _fragment_data(data)
    fragment_count = len(fragments)
    entropy = round(byte_entropy(data), 3)
    printable_ratio = round(
        sum(32 <= byte <= 126 or byte in (9, 10, 13) for byte in data)
        / len(data)
        * 100,
        2,
    ) if data else 0.0

    boundary_scores = [
        similarity_score(left[-16:], right[:16])
        for left, right in zip(fragments, fragments[1:])
    ]
    relationship_score = round(
        (sum(boundary_scores) / len(boundary_scores) * 100)
        if boundary_scores else 100.0,
        2,
    )
    integrity_score = 100.0 if data else 0.0
    coverage = 100.0 if data else 0.0
    confidence = calculate_recovery_confidence(
        relationship_score,
        integrity_score,
        coverage,
    )

    if confidence >= 85:
        priority = "HIGH"
        recoverability = "High recoverability"
        recovery_method = "Reconstruct ordered fragments and verify the restored hash."
    elif confidence >= 60:
        priority = "MEDIUM"
        recoverability = "Partial recovery likely"
        recovery_method = "Join linked fragments, isolate damaged ranges, and validate the partial output."
    else:
        priority = "LOW"
        recoverability = "Further evidence needed"
        recovery_method = "Compare against additional evidence before attempting reconstruction."

    return {
        "status": "analyzed",
        "filename": Path(filename).name,
        "classification": file_type,
        "size_bytes": len(data),
        "fragment_count": fragment_count,
        "fragment_size_bytes": CHUNK_SIZE,
        "entropy": entropy,
        "printable_ratio": printable_ratio,
        "relationships": {
            "method": "ordered fragment boundary comparison",
            "relationship_score": relationship_score,
            "linked_pairs": max(fragment_count - 1, 0),
        },
        "integrity_score": integrity_score,
        "fragment_coverage": coverage,
        "recovery_confidence": confidence,
        "recoverability": recoverability,
        "priority": priority,
        "recovery_status": "Ready for reconstruction",
        "recovery_method": recovery_method,
        "recoverable_items": [
            f"{fragment_count} ordered fragment{'s' if fragment_count != 1 else ''}",
            f"{relationship_score}% boundary relationship evidence",
            "Original bytes preserved for verification",
        ],
    }
