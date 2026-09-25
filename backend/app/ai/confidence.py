def calculate_recovery_confidence(
    ordering_score,
    integrity_score,
    fragment_coverage
):

    confidence = (
        0.45 * ordering_score +
        0.35 * integrity_score +
        0.20 * fragment_coverage
    )

    return round(
        max(
            0,
            min(
                100,
                confidence
            )
        ),
        2
    )


def explain_confidence(ordering_score, integrity_score, fragment_coverage):
    return {
        "ordering": round(ordering_score * 0.45, 2),
        "integrity": round(integrity_score * 0.35, 2),
        "coverage": round(fragment_coverage * 0.20, 2),
        "explanation": "Confidence combines fragment ordering, observed integrity, and recovered coverage.",
    }