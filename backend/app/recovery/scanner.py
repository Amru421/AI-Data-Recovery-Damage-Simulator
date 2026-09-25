from pathlib import Path
import hashlib
import math

from app.recovery.signatures import detect_file_type_with_filename


def calculate_entropy(data: bytes):

    if not data:
        return 0.0

    frequency = [0] * 256

    for byte in data:
        frequency[byte] += 1

    entropy = 0.0
    length = len(data)

    for count in frequency:

        if count == 0:
            continue

        probability = count / length

        entropy -= probability * math.log2(probability)

    return entropy


def scan_fragment(path: Path):

    data = path.read_bytes()

    sha256 = hashlib.sha256(data).hexdigest()

    return {
        "fragment_id": path.stem,
        "filename": path.name,
        "size": len(data),
        "sha256": sha256,
        "entropy": round(
            calculate_entropy(data),
            4
        ),
        "first_bytes": data[:16].hex(),
        "last_bytes": data[-16:].hex(),
        "possible_type": detect_file_type_with_filename(data, path.name),
        "path": str(path),
        "corruption_indicators": {
            "empty": not data,
            "short_fragment": len(data) < 16,
        },
    }


def scan_directory(directory):

    directory = Path(directory)

    results = []

    for file in sorted(directory.glob("*")):

        if file.is_file():

            try:
                results.append(
                    scan_fragment(file)
                )
            except Exception as error:
                results.append({
                    "filename": file.name,
                    "error": str(error)
                })

    return results