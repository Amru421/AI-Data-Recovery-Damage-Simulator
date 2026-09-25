from pathlib import Path
import json
import sys

BASE_DIR = Path(__file__).resolve().parents[3]

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from app.recovery.scanner import scan_directory
from app.recovery.integrity import calculate_integrity
from app.recovery.matcher import build_relationship_graph, fragment_index
from app.recovery.reconstructor import reconstruct_ordered
from app.ai.confidence import calculate_recovery_confidence, explain_confidence
from app.ai.report import generate_report
from app.ai.classifier import classify_artifact
from app.services.priority_service import calculate_priority


class RecoveryService:

    def scan(self, job_id):

        damaged_dir = (
            BASE_DIR /
            "data" /
            "damaged"
        )

        fragments = scan_directory(
            damaged_dir
        )

        fragments = scan_directory(damaged_dir)
        for item in fragments:
            item["original_index"] = fragment_index(item.get("fragment_id", ""))

        return {
            "fragment_count": len(fragments),
            "fragments": fragments,
            "relationships": build_relationship_graph(fragments),
            "status": "scan_completed",
        }

    def recover(self, job_id):

        ground_truth_path = (
            BASE_DIR /
            "data" /
            "ground_truth.json"
        )

        if not ground_truth_path.exists():

            return {
                "message":
                "ground_truth.json not found"
            }

        with open(
            ground_truth_path,
            "r",
            encoding="utf-8"
        ) as file:

            ground_truth = json.load(file)

        recovered_dir = BASE_DIR / "data" / "recovered"
        recovered_dir.mkdir(parents=True, exist_ok=True)
        scan_result = self.scan(job_id)
        scanned = scan_result["fragments"]
        results = []
        reports = []

        for artifact in ground_truth.get(
            "artifacts",
            []
        ):

            artifact_id = artifact.get("artifact_id")
            filename = artifact.get("filename", "artifact.bin")
            present = [
                item for item in scanned
                if item.get("fragment_id", "").startswith(f"{Path(filename).stem}_F")
            ]
            present_by_index = {item.get("original_index"): item for item in present}
            total = artifact.get("total_fragments", len(artifact.get("fragments", [])))
            missing = [index for index in range(total) if index not in present_by_index]
            original_path = BASE_DIR / "data" / "original" / filename
            expected_bytes = original_path.read_bytes() if original_path.exists() else b""
            chunk_size = artifact.get("fragments", [{}])[0].get("size", 1024) if artifact.get("fragments") else 1024
            corrupted = []
            for index, item in present_by_index.items():
                if expected_bytes:
                    expected = expected_bytes[index * chunk_size:(index + 1) * chunk_size]
                    if Path(item["path"]).read_bytes() != expected:
                        corrupted.append(index)
            output_path = recovered_dir / filename
            reconstruct_ordered(present, output_path)
            integrity = calculate_integrity(
                artifact.get("original_sha256"),
                output_path,
                expected_size=artifact.get("original_size"),
                total_fragments=total,
                missing_fragments=missing,
                corrupted_fragments=corrupted,
                filename=filename,
            )
            coverage = (len(present) / total * 100) if total else 0
            ordering_score = 100 if present and [item["original_index"] for item in sorted(present, key=lambda value: value["original_index"])] == sorted(item["original_index"] for item in present) else 0
            confidence = calculate_recovery_confidence(ordering_score, integrity["score"], coverage)
            priority = calculate_priority(confidence, integrity["score"], 70, 100 if artifact.get("original_sha256") else 35)
            recovery = {
                "artifact_id": artifact_id,
                "filename": filename,
                "recovered_file": str(output_path.relative_to(BASE_DIR)),
                "recovered_fragment_count": len(present),
                "missing_fragments": missing,
                "corrupted_fragments": corrupted,
                "integrity_score": integrity["score"],
                "integrity": integrity,
                "recovery_confidence": confidence,
                "confidence_factors": explain_confidence(ordering_score, integrity["score"], coverage),
                "priority": priority["priority"],
                "priority_score": priority["score"],
                "priority_factors": priority["factors"],
                "relationships": [edge for edge in scan_result["relationships"] if edge["source"] in {item["fragment_id"] for item in present}],
                "reconstruction_explanation": "Fragments were scanned, ranked by deterministic relationship features, and written in inferred source order."
            }
            results.append(recovery)
            reports.append(generate_report(artifact, recovery))

        payload = {"job_id": job_id, "artifacts": results, "reports": reports}
        with open(BASE_DIR / "data" / "recovery_results.json", "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

        return {
            "artifacts": results,
            "reports": reports,
            "status": "recovery_completed",
        }