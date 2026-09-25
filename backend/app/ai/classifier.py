from pathlib import Path


EXTENSION_MAP = {
    ".pdf": "Document",
    ".txt": "Document",
    ".docx": "Document",
    ".jpg": "Image",
    ".jpeg": "Image",
    ".png": "Image",
    ".gif": "Image",
    ".zip": "Archive",
    ".mp4": "Video",
    ".mp3": "Audio",
    ".db": "Database",
    ".log": "Log",
    ".csv": "Structured Data",
    ".json": "Structured Data",
    ".xml": "Structured Data",
    ".xlsx": "Structured Data"
}


def classify_artifact(filename):

    extension = Path(
        filename
    ).suffix.lower()

    return EXTENSION_MAP.get(
        extension,
        "Unknown"
    )