"""Public protocol consistency only; never local eligibility or study admission."""

import hashlib
import json
from pathlib import Path

import pytest

from tools import darwin_server_v030 as profile
from tools import prospective_execution_gate as gate
from tools import prospective_native_protocol as native
from tools import prospective_protocol as legacy
from tools.prospective_model import MODEL_ID, REGISTRY_PIN

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "evaluation/prospective/prospective-agent-text-20260830/protocol.json"


def test_actual_protocol_references_and_declared_condition_remain_consistent():
    raw = PROTOCOL.read_bytes()
    value = json.loads(raw)
    result = native.validate_protocol(PROTOCOL, hashlib.sha256(raw).hexdigest())
    assert result["status"] == "native_protocol_candidate_valid"
    assert result["admitted"] is result["study_unlocked"] is False
    assert result["execution_observed"] is False
    assert result["expected_slots"] == 2
    assert list(result["requests"]) == value["expected_slots"]
    assert value["study_id"] == "prospective-agent-text-20260830"
    condition = value["condition"]
    assert condition["model_id"] == MODEL_ID
    assert condition["registry_sha256"] == REGISTRY_PIN
    assert condition["profile_sha256"] == profile.profile_digest()
    assert condition["runtime_sha256"] == profile.PINNED_FILES[profile.EXECUTABLE]
    assert condition["adapter_sha256"] == hashlib.sha256((ROOT / gate.ADAPTER).read_bytes()).hexdigest()
    manifest = json.loads((ROOT / gate.REGISTRY).read_bytes())
    selected = next(row for row in manifest["models"] if row["id"] == MODEL_ID)
    assert condition["model_revision"] == selected["revision"]
    assert condition["model_sha256"] == selected["files"][0]["sha256"]
    assert value["generation"] == legacy.GENERATION
    # Declared file hashes do not inspect the actual installed model/runtime.
    assert value["held_out"] is False
    assert value["case_exposure"] == "public"


@pytest.mark.parametrize("reference", ["rubric", "scoring_instructions", "prompt_template"])
def test_changed_operative_reference_is_rejected(tmp_path, reference):
    value = json.loads(PROTOCOL.read_bytes())
    refs = [case["input"] for case in value["cases"]]
    refs.extend(value[key] for key in ("rubric", "scoring_instructions", "prompt_template"))
    for ref in refs:
        (tmp_path / ref["path"]).write_bytes((PROTOCOL.parent / ref["path"]).read_bytes())
    changed = tmp_path / value[reference]["path"]
    changed.write_bytes(changed.read_bytes() + b"changed")
    copied = tmp_path / "protocol.json"
    copied.write_bytes(PROTOCOL.read_bytes())
    with pytest.raises(ValueError):
        native.validate_protocol(copied, hashlib.sha256(copied.read_bytes()).hexdigest())
