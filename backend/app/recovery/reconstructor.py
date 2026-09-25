from pathlib import Path
import re


def reconstruct(
    fragment_paths,
    output_path
):

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output_path, "wb") as output:

        for fragment in fragment_paths:

            fragment = Path(fragment)

            with open(fragment, "rb") as source:

                output.write(
                    source.read()
                )

    return str(output_path)


def greedy_reconstruct(
    fragments,
    output_path
):

    fragments = sorted(fragments, key=lambda item: item.get("index", _index_from_id(item.get("fragment_id", ""))))

    paths = [
        x["path"]
        for x in fragments
        if x.get("path")
    ]

    return reconstruct(
        paths,
        output_path
    )


def _index_from_id(fragment_id):
    match = re.search(r"_F(\d+)$", fragment_id or "")
    return int(match.group(1)) if match else 0


def reconstruct_ordered(fragments, output_path):
    """Reconstruct using the scanner's inferred fragment order metadata."""
    ordered = sorted(
        fragments,
        key=lambda item: item.get("original_index", _index_from_id(item.get("fragment_id", ""))),
    )
    return reconstruct([item["path"] for item in ordered if item.get("path")], output_path)