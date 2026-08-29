# Decision: Acquire multimodal adapter dependencies

- **Decision ID:** 20260829-003-track06-adapter-acquisition
- **Status:** Approved with conditions
- **Date raised:** 2026-08-29
- **Owner:** Repository owner
- **Track:** multimodal-capability-fabric_20260731
- **GitHub issue:** https://github.com/edithatogo/rcagent/issues/11

## Decision Needed

Track 06 cannot certify adapters or device classes from contract probes alone. Decide whether to install bounded local framework profiles and acquire any required model assets for synthetic measurements.

## Recommendation

**Recommend: Approve bounded local adapter acquisition**

Admit one framework at a time in isolated optional environments, starting with model-free pydicom and WFDB, then Docling/OCR, encoders, and local speech only after each licence, asset, egress, cache, rollback and device preflight passes. Keep pyannote/NeMo, MONAI inference, remote code, external inference, and all clinical interpretation disabled unless separately approved.

## Options

| Option | Benefits | Risks and trade-offs | Reversibility | Cost and dependency impact |
|---|---|---|---|---|
| Approve bounded local adapter acquisition | Enables measured fixtures and honest support matrices | Downloads, storage, transitive licences and device time require review | Optional environments and caches can be removed | Allows Track 06 certification to proceed |
| Approve only model-free pydicom and WFDB | Produces safe ingestion evidence first | Document, encoder and speech phases remain blocked | Fully reversible | Partial progress only |
| Keep contract-only state | No new dependency, download or licence exposure | Acceptance criteria remain unmet and Track 06/08 stay blocked | Fully reversible | No immediate cost |

## Evidence and Assumptions

- `evaluation/multimodal/registry.json` records exact observed candidates and unsupported states.
- Five synthetic contract probes pass without executing upstream frameworks.
- Assumption: all measurements remain local, synthetic, research-only, and unpublished.

## Privacy, Safety, Legal, and Maintenance Impact

No real clinical data is authorised. Every dependency and model asset needs exact licence and provenance review. Network use must be limited to approved acquisition, with telemetry and remote code disabled. Image, ECG, and audio clinical interpretation remain prohibited.

## Safe Default if Deferred

Keep all profiles unsupported, retain contract probes only, and do not claim adapter or device support.

## Execution Impact

- **Paused scope:** Tracks 06 phases 2–7 and completion/archival.
- **Work continuing autonomously:** Contract review, documentation, and negative validation.
- **Dependency effect:** Track 08 remains blocked because Track 06 is incomplete.
- **Wake condition:** Explicit approval of one option.

## Response Requested

Respond exactly: `Approve bounded local adapter acquisition`.

## Owner Decision

- **Decision:** Approve bounded local adapter acquisition.
- **Conditions:** Admit one isolated optional profile at a time, beginning with model-free pydicom and WFDB, then document/OCR, encoders, and local speech; diarisation and MONAI-compatible research assets require exact candidate clearance. Every artefact requires immutable revision, hash, licence/provenance, acquisition-only egress, telemetry-off, remote-code-off, device, cache, uninstall, rollback, and synthetic-fixture receipts. No private clinical or employee data, external inference, redistribution, clinical interpretation, or unsupported support claim.
- **Date:** 2026-08-29
- **Recorded by:** Codex from the repository owner's explicit panel-ratification response

## Follow-up

- [ ] Update plans, metadata, receipts and GitHub state
- [ ] Execute one admitted profile at a time and preserve rollback evidence
