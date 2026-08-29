"""Offline synthetic contract evaluation for optional encoder backends.

This does not execute a model. It measures the framework-neutral envelope and
fails closed for capabilities that need a cleared immutable model artefact.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import platform
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[1]
FIXTURE_PATH = ROOT / "evaluation/multimodal/encoder-contract-fixtures.json"

BACKENDS = {
    "transformers": "transformers",
    "onnxruntime": "onnxruntime",
    "openvino": "openvino",
}
MODEL_TASKS = (
    "dense_embedding",
    "cross_encoder_reranking",
    "classification",
    "similarity",
    "extraction",
)


def _read_fixture(path: Path = FIXTURE_PATH) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("pairs"), list):
        raise ValueError("encoder fixture must be an object containing pairs")
    return value


def _distribution_version(distribution: str) -> str | None:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return None


def _tokens(text: str) -> list[str]:
    return text.casefold().split()


def _contract_vector(text: str, limit: int, dimensions: int = 16) -> tuple[list[float], bool]:
    """Produce a deterministic test oracle, never a model embedding."""
    tokens = _tokens(text)
    kept = tokens[:limit]
    values = [0.0] * dimensions
    for token in kept:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        values[digest[0] % dimensions] += 1.0 if digest[1] & 1 else -1.0
    norm = math.sqrt(sum(value * value for value in values)) or 1.0
    return [value / norm for value in values], len(tokens) > limit


def _cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def evaluate(path: Path = FIXTURE_PATH) -> dict[str, Any]:
    started = time.perf_counter()
    fixture = _read_fixture(path)
    limit = fixture.get("max_tokens")
    if not isinstance(limit, int) or limit < 1:
        raise ValueError("max_tokens must be a positive integer")

    measurements = []
    for pair in fixture["pairs"]:
        left, left_truncated = _contract_vector(pair["left"], limit)
        right, right_truncated = _contract_vector(pair["right"], limit)
        quantised_left = [max(-127, min(127, round(value * 127))) for value in left]
        restored_left = [value / 127 for value in quantised_left]
        measurements.append(
            {
                "id": pair["id"],
                "language": pair["language"],
                "domain": pair["domain"],
                "left_tokens": len(_tokens(pair["left"])),
                "right_tokens": len(_tokens(pair["right"])),
                "truncated": left_truncated or right_truncated,
                "contract_oracle_cosine": round(_cosine(left, right), 6),
                "int8_oracle_max_abs_error": round(
                    max(abs(a - b) for a, b in zip(left, restored_left, strict=True)), 6
                ),
            }
        )

    backends = []
    for backend, distribution in BACKENDS.items():
        version = _distribution_version(distribution)
        backends.append(
            {
                "backend": backend,
                "distribution": distribution,
                "observed_version": version,
                "contract_status": "observed_unadmitted" if version else "unavailable",
                "model_executed": False,
                "remote_code": "prohibited",
                "network": "disabled",
                "tasks": {task: "unsupported_no_cleared_model_asset" for task in MODEL_TASKS},
            }
        )

    result: dict[str, Any] = {
        "schema_version": "1.0",
        "profile_id": "encoders-local",
        "data_class": "generated_synthetic_only",
        "runtime": f"CPython {platform.python_version()} {platform.system()} {platform.machine()}",
        "execution_mode": "offline_contract_oracle_no_model",
        "network": "disabled_no_network_api_used",
        "telemetry": "none",
        "remote_code": "prohibited",
        "external_inference": False,
        "backends": backends,
        "measurements": measurements,
        "effects": {
            "truncation": "measured_on_contract_oracle_only",
            "input_length": "measured_on_contract_oracle_only",
            "language": "described_not_quality_validated",
            "domain": "described_not_quality_validated",
            "calibration": "unsupported_no_probabilistic_model_output",
            "drift": "unsupported_no_baseline_model_revision",
            "quantisation": "int8_numeric_oracle_only_not_backend_or_model",
        },
        "limitations": [
            "No immutable model artefact was locally available or cleared; no model was executed.",
            "Contract-oracle vectors are deterministic test instrumentation, not embeddings.",
            "No backend, task, language, domain, calibration, drift or quantisation support claim is made.",
        ],
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode("utf-8")
    result["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


def verify(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    unsigned = {key: value for key, value in result.items() if key != "receipt_sha256"}
    digest = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if result.get("receipt_sha256") != digest:
        errors.append("receipt hash mismatch")
    if result.get("data_class") != "generated_synthetic_only":
        errors.append("data class is not synthetic")
    for backend in result.get("backends", []):
        if backend.get("model_executed") is not False or backend.get("remote_code") != "prohibited":
            errors.append(f"backend boundary invalid: {backend.get('backend')!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=FIXTURE_PATH)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate(args.fixture)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
