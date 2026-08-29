import json
from pathlib import Path

from tools.multimodal_fabric import load_registry, validate_registry

ROOT = Path(__file__).parents[1]
MATRIX = ROOT / "evaluation/multimodal/support-matrix-20260829.json"


def test_support_matrix_is_fail_closed_and_evidence_exists() -> None:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    assert matrix["certification_scope"] == "repository contract evidence only"
    assert len(matrix["profiles"]) == 5
    assert {item["profile_id"] for item in matrix["profiles"]} == {
        "documents-ocr",
        "encoders-local",
        "speech-local",
        "medical-imaging-research",
        "ecg-research",
    }
    for profile in matrix["profiles"]:
        assert profile["supported_claims"]
        assert profile["unsupported_claims"]
        assert "operational use" in profile["unsupported_claims"]
        for evidence in profile["evidence"]:
            assert (ROOT / evidence).is_file(), evidence
    boundaries = matrix["global_boundaries"]
    assert boundaries["remote_code"] == "prohibited"
    assert boundaries["private_data"].startswith("prohibited")
    assert boundaries["clinical_interpretation"] == "disabled"
    assert (ROOT / matrix["ci_contract_benchmark"]["evidence"]).is_file()
    assert validate_registry(load_registry()) == []
