# Track 08 completion receipt

## Repository outcome

Track 08 is repository-complete as a negative-result local runtime/model lab
contract. It provides privacy-safe coarse discovery, strict candidate and model
admission, fail-closed routing, hardened local comparator admission,
operator-owned offline inventory verification and a dated internal matrix. It
downloads and executes no model, supports no runtime/model tuple, and publishes
no comparative claim.

## Acceptance mapping

| Criterion | Direct evidence |
|---|---|
| AC1 reproducible privacy-safe device profiles | `privacy_safe_device_profile`, `validate_device_profile`, durable device observation, sentinel and hash tests. RAM/storage/driver/power gaps are explicit. |
| AC2 runtime adapter coverage where applicable | Registry/schema 1.0 covers interface-only, installed-unmeasured, unavailable and experimental states for llama.cpp, ONNX Runtime, OpenVINO, MLX and MAX/Mojo. Measured/support states require a future exact execution schema. |
| AC3 governed model entries | Strict nested model validation and schema; `models` is empty. Hypotheses are separate, unverified and unroutable. |
| AC4 measured recommendations | No tuple was eligible. The matrix therefore contains only evidence-bound unsupported classifications and makes no parameter-count/vendor inference. |
| AC5 safe routing | Registry/discovery validation, exact receipt hashes, modality/context checks, external/remote-code rejection, governed-private rejection, malformed-input handling and adversarial tests. |
| AC6 offline lifecycle | Exact operator-owned directory inventory, path/hash/size checks, symlink/special/undeclared-entry rejection and documented non-mutating lifecycle for the empty supported set. |

## Exact validation at substantive revision `8000b2c`

- Environment: macOS 26.6.2 arm64; CPython 3.14.5; generated synthetic/public metadata only.
- Network/model boundary: no Track 08 network request, model download, remote code or inference.
- `uv run pytest -q --cov=tools --cov-report=term --cov-fail-under=80`: 343 passed; 91.49% total tools coverage.
- Focused runtime/comparator gate: 59 passed; 96.45% combined module coverage.
- `uv run ruff check tools tests`: passed.
- `uv run ty check tools tests`: passed.
- `uv run basedpyright`: zero errors, warnings or notes.
- `uv run python -m tools.check_gremlins .`: no gremlins found.
- `uv run python -m tools.validate_repository`: passed.
- Benchmark registry validation and seven-case deterministic regression: passed 7/7; no model or external execution.
- `git diff --check`: passed.

## Interpretation and limitations

Runtime registry licence, network and telemetry fields are candidate-policy
requirements, not proof of observed runtime behaviour. Command discovery is
not version/build/driver evidence. The Apple arm64 observation does not support
Intel 32 GiB or larger GPU claims. No quantisation, model quality, context,
latency, memory, storage, power or robustness comparison was run by Track 08.

No private clinical or employee data, credentials, third-party rights claim,
redistribution, paid compute or public release was used. Clinical, policy,
legal, regulatory, employment, cultural-safety, organisational and deployment
validation remain outside repository completion unless separately authorised
by the applicable authority.

## Pending external gates and rollback

- New runtime/model acquisition remains pending per artefact.
- Runtime/model support promotion remains pending exact measured evidence.
- Public comparative claims remain pending a separate publication action.

Revert Track 08 commits to remove the contracts. The offline verifier makes no
filesystem mutation, and external model/runtime artefacts remain outside this
repository.
