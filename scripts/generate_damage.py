from pathlib import Path
import hashlib
import json
import random
import argparse
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parents[1]

ORIGINAL_DIR = BASE_DIR / "data" / "original"
DAMAGED_DIR = BASE_DIR / "data" / "damaged"
GROUND_TRUTH = BASE_DIR / "data" / "ground_truth.json"


def sha256(data):

    return hashlib.sha256(data).hexdigest()


def corrupt_bytes(data):

    if not data:
        return data

    data = bytearray(data)

    number_of_changes = max(
        1,
        len(data) // 100
    )

    for _ in range(number_of_changes):

        index = random.randint(
            0,
            len(data) - 1
        )

        original = data[index]
        replacement = random.randint(0, 255)
        data[index] = replacement if replacement != original else (original + 1) % 256

    return bytes(data)


def process_file(
    file_path,
    chunk_size,
    delete_probability,
    corruption_probability
):

    data = file_path.read_bytes()

    original_hash = sha256(data)

    chunks = []

    for index in range(
        0,
        len(data),
        chunk_size
    ):

        chunk = data[
            index:index + chunk_size
        ]

        chunks.append({
            "index": len(chunks),
            "data": chunk
        })

    random.shuffle(chunks)

    missing = []
    corrupted = []
    fragment_records = []

    for chunk in chunks:

        original_index = chunk["index"]

        # Random deletion
        if (
            len(chunks) > 3 and
            random.random() < delete_probability
        ):

            missing.append(
                original_index
            )

            continue

        fragment_data = chunk["data"]

        is_corrupted = False

        if (
            random.random() <
            corruption_probability
        ):

            fragment_data = corrupt_bytes(
                fragment_data
            )

            corrupted.append(
                original_index
            )

            is_corrupted = True

        fragment_name = (
            f"{file_path.stem}"
            f"_F{original_index:04d}.bin"
        )

        fragment_path = (
            DAMAGED_DIR /
            fragment_name
        )

        fragment_path.write_bytes(
            fragment_data
        )

        fragment_records.append({
            "fragment_id":
                fragment_path.stem,

            "original_index":
                original_index,

            "filename":
                fragment_name,

            "size":
                len(fragment_data),

            "corrupted": is_corrupted,
            "sha256": sha256(fragment_data),
        })

    return {
        "artifact_id": file_path.stem,
        "filename": file_path.name,
        "file_type": file_path.suffix.lower(),
        "original_size": len(data),
        "original_sha256": original_hash,
        "total_fragments": len(chunks),
        "fragments": fragment_records,
        "missing_fragments": missing,
        "corrupted_fragments": corrupted
    }


def main():

    parser = argparse.ArgumentParser(
        description=
        "AI-RecoverX Damage Simulator"
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1024
    )

    parser.add_argument(
        "--fragment-size",
        type=int,
        dest="chunk_size_alias",
        help="Alias for --chunk-size"
    )

    parser.add_argument(
        "--delete-probability",
        type=float,
        default=0.15
    )

    parser.add_argument(
        "--corruption-probability",
        type=float,
        default=0.15
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed used to make damage generation reproducible"
    )

    args = parser.parse_args()

    if args.chunk_size_alias is not None:
        args.chunk_size = args.chunk_size_alias

    if args.chunk_size <= 0:
        parser.error("chunk size must be greater than zero")

    if not 0 <= args.delete_probability <= 1:
        parser.error("delete probability must be between 0 and 1")

    if not 0 <= args.corruption_probability <= 1:
        parser.error("corruption probability must be between 0 and 1")

    random.seed(args.seed)

    ORIGINAL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    DAMAGED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Remove old damaged fragments
    for file in DAMAGED_DIR.glob("*"):

        if file.is_file():
            file.unlink()

    artifacts = []

    files = [
        file
        for file in ORIGINAL_DIR.iterdir()
        if file.is_file()
    ]

    if not files:

        sample = (
            "AI-RecoverX sample evidence file.\n"
            "This file is used to demonstrate "
            "fragmentation, damage simulation, "
            "reconstruction and integrity analysis."
        )

        sample_path = (
            ORIGINAL_DIR /
            "sample_evidence.txt"
        )

        sample_path.write_text(
            sample,
            encoding="utf-8"
        )

        files = [sample_path]

    for file_path in files:

        artifact = process_file(
            file_path,
            args.chunk_size,
            args.delete_probability,
            args.corruption_probability
        )

        artifacts.append(
            artifact
        )

    result = {
        "project": "AI-RecoverX",
        "generated_with": {
            "chunk_size":
                args.chunk_size,

            "delete_probability":
                args.delete_probability,

            "corruption_probability":
                args.corruption_probability,
            "seed": args.seed,
            "generated_at": datetime.now(timezone.utc).isoformat()
        },
        "artifacts": artifacts
    }

    with open(
        GROUND_TRUTH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4
        )

    print(
        "\nAI-RecoverX damage simulation completed."
    )

    print(
        f"Artifacts processed: {len(artifacts)}"
    )

    print(
        f"Ground truth: {GROUND_TRUTH}"
    )


if __name__ == "__main__":
    main()