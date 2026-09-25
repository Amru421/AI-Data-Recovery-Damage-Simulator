from pathlib import Path


def split_file(
    file_path,
    output_dir,
    chunk_size=1024
):

    file_path = Path(file_path)
    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    fragments = []

    with open(file_path, "rb") as source:

        index = 0

        while True:

            data = source.read(chunk_size)

            if not data:
                break

            fragment_name = (
                f"{file_path.stem}_F{index:04d}.bin"
            )

            fragment_path = (
                output_dir / fragment_name
            )

            fragment_path.write_bytes(data)

            fragments.append({
                "fragment_id": fragment_path.stem,
                "index": index,
                "filename": fragment_name,
                "size": len(data)
            })

            index += 1

    return fragments