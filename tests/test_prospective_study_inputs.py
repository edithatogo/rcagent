"""Public protocol consistency only; never local eligibility or study admission."""

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tools import darwin_server_v030 as profile
from tools import prospective_execution_gate as gate
from tools import prospective_native_protocol as native
from tools import prospective_protocol as legacy
from tools.json_shapes import is_array, require_object
from tools.prospective_model import MODEL_ID, REGISTRY_PIN

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "evaluation/prospective/prospective-agent-text-20260830/protocol.json"


def test_actual_protocol_references_and_declared_condition_remain_consistent(
    tmp_path: Path,
) -> None:
    raw = PROTOCOL.read_bytes()
    value = require_object(json.loads(raw), context="historical protocol")
    raw_result: object = native.validate_protocol(PROTOCOL, hashlib.sha256(raw).hexdigest())
    result = require_object(raw_result, context="protocol validation")
    assert result["status"] == "native_protocol_candidate_valid"
    assert result["admitted"] is result["study_unlocked"] is False
    assert result["execution_observed"] is False
    assert result["expected_slots"] == 2
    assert list(require_object(result["requests"], context="requests")) == value["expected_slots"]
    assert value["study_id"] == "prospective-agent-text-20260830"
    condition = require_object(value["condition"], context="condition")
    assert condition["model_id"] == MODEL_ID
    assert condition["registry_sha256"] == REGISTRY_PIN
    review = require_object(
        json.loads((ROOT / gate.REVIEW_PATH).read_bytes()), context="historical review"
    )
    source_commit = review["source_commit"]
    assert isinstance(source_commit, str)
    assert re.fullmatch(r"[0-9a-f]{40}", source_commit)
    assert review["protocol_sha256"] == hashlib.sha256(raw).hexdigest()
    # Evaluate the trusted repository's historical declarations in an isolated
    # interpreter with no site packages. No verification, subprocess runtime or
    # model execution is requested. The current engineering identity is separate.
    package = tmp_path / "tools"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    for name in (
        "darwin_runtime_profile.py",
        "darwin_runtime_v030.py",
        "darwin_server_v030.py",
        "local_model_comparator.py",
    ):
        historical_source = subprocess.run(
            ["git", "show", f"{source_commit}:tools/{name}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        (package / name).write_bytes(historical_source)
    declaration = subprocess.run(
        [
            sys.executable,
            "-I",
            "-S",
            "-c",
            (
                "import sys, json; sys.path.insert(0, sys.argv[1]); "
                "from tools import darwin_server_v030 as p; "
                "print(json.dumps({'profile_sha256': p.profile_digest(), "
                "'runtime_sha256': p.PINNED_FILES[p.EXECUTABLE]}))"
            ),
            str(tmp_path),
        ],
        capture_output=True,
        check=True,
    ).stdout
    historical_profile = require_object(json.loads(declaration), context="historical profile")
    assert condition["profile_sha256"] == historical_profile["profile_sha256"]
    assert condition["runtime_sha256"] == historical_profile["runtime_sha256"]
    assert profile.PROFILE_ID == "darwin-llama-server-0.3.0-typing-20261114"
    assert profile.profile_digest() != historical_profile["profile_sha256"]
    # A consumed protocol binds its reviewed source revision. Current engineering
    # changes require fresh execution review; they do not rewrite this old pin.
    historical_adapter = subprocess.run(
        ["git", "show", f"{source_commit}:{gate.ADAPTER}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    assert condition["adapter_sha256"] == hashlib.sha256(historical_adapter).hexdigest()
    assert review["adapter_sha256"] == condition["adapter_sha256"]
    manifest = require_object(json.loads((ROOT / gate.REGISTRY).read_bytes()), context="registry")
    raw_models = manifest["models"]
    assert is_array(raw_models)
    models = [require_object(row, context="model") for row in raw_models]
    selected = next(row for row in models if row["id"] == MODEL_ID)
    assert condition["model_revision"] == selected["revision"]
    files = selected["files"]
    assert is_array(files)
    assert condition["model_sha256"] == require_object(files[0], context="model file")["sha256"]
    assert value["generation"] == legacy.GENERATION
    # Declared file hashes do not inspect the actual installed model/runtime.
    assert value["held_out"] is False
    assert value["case_exposure"] == "public"


@pytest.mark.parametrize("reference", ["rubric", "scoring_instructions", "prompt_template"])
def test_changed_operative_reference_is_rejected(tmp_path: Path, reference: str) -> None:
    value = require_object(json.loads(PROTOCOL.read_bytes()), context="protocol")
    cases = value["cases"]
    assert is_array(cases)
    refs = [
        require_object(require_object(case, context="case")["input"], context="case input")
        for case in cases
    ]
    refs.extend(
        require_object(value[key], context=key)
        for key in ("rubric", "scoring_instructions", "prompt_template")
    )
    for ref in refs:
        path = ref["path"]
        assert isinstance(path, str)
        (tmp_path / path).write_bytes((PROTOCOL.parent / path).read_bytes())
    changed_reference = require_object(value[reference], context="changed reference")
    path = changed_reference["path"]
    assert isinstance(path, str)
    changed = tmp_path / path
    changed.write_bytes(changed.read_bytes() + b"changed")
    copied = tmp_path / "protocol.json"
    copied.write_bytes(PROTOCOL.read_bytes())
    with pytest.raises(ValueError):
        native.validate_protocol(copied, hashlib.sha256(copied.read_bytes()).hexdigest())
