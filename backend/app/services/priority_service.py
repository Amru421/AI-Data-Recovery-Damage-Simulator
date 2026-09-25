def calculate_priority(
    recovery_confidence,
    integrity,
    artifact_relevance,
    metadata_strength
):

    score = (
        0.35 * recovery_confidence +
        0.25 * integrity +
        0.20 * artifact_relevance +
        0.20 * metadata_strength
    )

    score = round(
        max(0, min(100, score)),
        2
    )

    if score >= 80:
        level = "High"

    elif score >= 50:
        level = "Medium"

    else:
        level = "Low"

    return {
        "score": score,
        "priority": level,
        "factors": {
            "recovery_confidence": recovery_confidence,
            "integrity": integrity,
            "artifact_relevance": artifact_relevance,
            "metadata_strength": metadata_strength,
        },
    }