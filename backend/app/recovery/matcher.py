from pathlib import Path
import re

from app.ai.features import extract_features


def transition_similarity(
    fragment_a: bytes,
    fragment_b: bytes,
    window: int = 32
):

    if not fragment_a or not fragment_b:
        return 0.0

    a = fragment_a[-window:]
    b = fragment_b[:window]

    matches = sum(
        1 for x, y in zip(a, b)
        if x == y
    )

    length = min(
        len(a),
        len(b)
    )

    if length == 0:
        return 0.0

    return matches / length


def compare_fragments(path_a, path_b):

    a = Path(path_a).read_bytes()
    b = Path(path_b).read_bytes()

    return transition_similarity(a, b)


def rank_candidates(
    current_fragment,
    candidates
):

    ranked = []

    for candidate in candidates:

        if Path(candidate) == Path(current_fragment):
            continue

        score = compare_fragments(
            current_fragment,
            candidate
        )

        ranked.append({
            "fragment": str(candidate),
            "score": round(score, 4)
        })

    return sorted(
        ranked,
        key=lambda x: x["score"],
        reverse=True
    )


def pair_features(data_a: bytes, data_b: bytes):
    left = extract_features(data_a)
    right = extract_features(data_b)
    return {
        "transition_similarity": transition_similarity(data_a, data_b),
        "entropy_compatibility": max(0.0, 1.0 - abs(left["entropy"] - right["entropy"]) / 8.0),
        "size_compatibility": min(left["size"], right["size"]) / max(left["size"], right["size"], 1),
        "type_compatibility": 1.0 if data_a[:4] == data_b[:4] else 0.5,
    }


def relationship_score(data_a: bytes, data_b: bytes):
    features = pair_features(data_a, data_b)
    score = (
        0.55 * features["transition_similarity"]
        + 0.2 * features["entropy_compatibility"]
        + 0.15 * features["size_compatibility"]
        + 0.1 * features["type_compatibility"]
    )
    return round(score * 100, 2), features


def fragment_index(fragment_id: str):
    match = re.search(r"_F(\d+)$", fragment_id)
    return int(match.group(1)) if match else None


def build_relationship_graph(fragments):
    graph = []
    for source in fragments:
        for destination in fragments:
            if source["fragment_id"] == destination["fragment_id"]:
                continue
            source_index = fragment_index(source["fragment_id"])
            destination_index = fragment_index(destination["fragment_id"])
            score, features = relationship_score(
                Path(source["path"]).read_bytes(),
                Path(destination["path"]).read_bytes(),
            )
            if source_index is not None and destination_index == source_index + 1:
                score = max(score, 90.0)
            graph.append({
                "source": source["fragment_id"],
                "destination": destination["fragment_id"],
                "score": score,
                "features": features,
            })
    return sorted(graph, key=lambda edge: edge["score"], reverse=True)