import math


def byte_entropy(data):

    if not data:
        return 0.0

    counts = [0] * 256

    for byte in data:
        counts[byte] += 1

    result = 0.0

    for count in counts:

        if count == 0:
            continue

        probability = count / len(data)

        result -= (
            probability *
            math.log2(probability)
        )

    return result


def extract_features(data):

    if not data:
        return {
            "size": 0,
            "entropy": 0,
            "first_byte": 0,
            "last_byte": 0,
            "first_bytes": [],
            "last_bytes": [],
            "byte_frequency": [0] * 16,
            "transition_mean": 0.0,
        }

    transitions = [abs(left - right) for left, right in zip(data, data[1:])]

    return {
        "size": len(data),
        "entropy": byte_entropy(data),
        "first_byte": data[0],
        "last_byte": data[-1],
        "first_bytes": list(data[:8]),
        "last_bytes": list(data[-8:]),
        "byte_frequency": [data.count(value) / len(data) for value in range(16)],
        "transition_mean": sum(transitions) / len(transitions) if transitions else 0.0,
    }