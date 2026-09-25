from pathlib import Path
import hashlib
from app.recovery.signatures import detect_file_type, detect_from_filename


def sha256_file(path):

    path = Path(path)

    sha256 = hashlib.sha256()

    with open(path, "rb") as file:

        while True:

            chunk = file.read(8192)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def calculate_integrity(
    original_hash,
    recovered_path,
    expected_size=None,
    total_fragments=0,
    missing_fragments=None,
    corrupted_fragments=None,
    filename="",
):

    recovered_hash = sha256_file(
        recovered_path
    )

    missing = missing_fragments or []
    corrupted = corrupted_fragments or []
    size = Path(recovered_path).stat().st_size
    size_score = 100.0 if expected_size in (None, size) else min(size / max(expected_size, 1) * 100, 100)
    damage_score = basic_integrity_score(total_fragments, missing, corrupted) if total_fragments else size_score
    header_type = detect_file_type(Path(recovered_path).read_bytes()[:32])
    expected_type = detect_from_filename(filename) if filename else "UNKNOWN"
    header_valid = header_type != "UNKNOWN" or expected_type in {"TXT", "DOCX", "UNKNOWN"}
    score = round(max(0.0, min(100.0, 0.5 * damage_score + 0.25 * size_score + 0.25 * (100 if header_valid else 0))), 2)
    return {
        "score": 100.0 if original_hash == recovered_hash else score,
        "hash_match": original_hash == recovered_hash,
        "recovered_sha256": recovered_hash,
        "size": size,
        "expected_size": expected_size,
        "size_consistent": expected_size in (None, size),
        "header_valid": header_valid,
        "missing_count": len(missing),
        "corrupted_count": len(corrupted),
    }


def basic_integrity_score(
    total_fragments,
    missing_fragments,
    corrupted_fragments
):

    if total_fragments == 0:
        return 0.0

    damaged = (
        len(missing_fragments)
        + len(corrupted_fragments)
    )

    score = (
        1 -
        damaged / total_fragments
    ) * 100

    return round(
        max(0.0, score),
        2
    )