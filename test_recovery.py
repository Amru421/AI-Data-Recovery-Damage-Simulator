import json

from python import calculate_recovery_metrics, prioritize_recovery


def test_calculate_recovery_metrics_recovers_missing_fields():
    ground_truth = [
        {
            "transaction_id": "TXN-9901",
            "timestamp": "2026-09-25T14:32:00Z",
            "user_id": 1042,
            "amount_usd": 249.50,
            "action": "PURCHASE",
            "status": "SUCCESS"
        }
    ]
    recovered = [
        {
            "transaction_id": "TXN-9901",
            "timestamp": "2026-09-25T14:32:00Z",
            "user_id": 1042,
            "amount_usd": 249.50,
            "action": "PURCHASE",
            "status": "SUCCESS"
        }
    ]

    result = calculate_recovery_metrics(recovered, ground_truth)

    assert result["valid"] is True
    assert result["accuracy"] >= 95
    assert result["integrity_score"] >= 90


def test_prioritize_recovery_selects_high_priority():
    score = {
        "accuracy": 96,
        "integrity_score": 88,
        "recovery_confidence": 92,
        "missing_records": 0,
        "corruption_ratio": 5,
    }

    priority = prioritize_recovery(score)

    assert priority["level"] == "HIGH"
    assert priority["reason"].startswith("High-priority")


def test_generate_fragment_dataset_and_report():
    from python import generate_fragment_dataset, build_forensic_report

    dataset = generate_fragment_dataset([
        {"transaction_id": "TXN-9901", "status": "SUCCESS"},
        {"transaction_id": "TXN-9902", "status": "SUCCESS"},
        {"transaction_id": "TXN-9903", "status": "FAILED"}
    ], "Field Obliteration (Delete)", 33)

    assert "fragments" in dataset
    assert len(dataset["fragments"]) >= 3
    assert dataset["missing_fragments"] >= 0

    report = build_forensic_report({
        "accuracy": 87.5,
        "integrity_score": 82.0,
        "recovery_confidence": 90.0,
        "missing_records": 1,
        "corruption_ratio": 18.0,
    }, "financial_report.json")

    assert "Integrity" in report
    assert "87.5%" in report
    assert "financial_report.json" in report
