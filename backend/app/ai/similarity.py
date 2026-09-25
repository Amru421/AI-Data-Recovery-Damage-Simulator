def byte_similarity(a: bytes, b: bytes):

    if not a or not b:
        return 0.0

    length = min(
        len(a),
        len(b)
    )

    matches = sum(
        1
        for i in range(length)
        if a[i] == b[i]
    )

    return matches / length


def similarity_score(
    end_a: bytes,
    start_b: bytes
):

    if not end_a or not start_b:
        return 0.0

    length = min(
        len(end_a),
        len(start_b)
    )

    if length == 0:
        return 0.0

    matches = sum(
        1
        for i in range(length)
        if end_a[-length + i] ==
           start_b[i]
    )

    return round(
        matches / length,
        4
    )