SIGNATURES = {
    "PDF": b"%PDF",
    "PNG": b"\x89PNG\r\n\x1a\n",
    "JPEG": b"\xff\xd8\xff",
    "ZIP": b"PK\x03\x04",
    "GIF": b"GIF8"
}


def detect_file_type(data: bytes):

    for file_type, signature in SIGNATURES.items():

        if data.startswith(signature):
            return file_type

    return "UNKNOWN"


def detect_file_type_with_filename(data: bytes, filename: str = ""):
    detected = detect_file_type(data)
    return detected if detected != "UNKNOWN" else detect_from_filename(filename)


def detect_from_filename(filename: str):

    filename = filename.lower()

    if filename.endswith(".pdf"):
        return "PDF"

    if filename.endswith((".jpg", ".jpeg")):
        return "JPEG"

    if filename.endswith(".png"):
        return "PNG"

    if filename.endswith(".zip"):
        return "ZIP"

    if filename.endswith(".gif"):
        return "GIF"

    if filename.endswith(".txt"):
        return "TXT"

    if filename.endswith(".docx"):
        return "DOCX"

    return "UNKNOWN"