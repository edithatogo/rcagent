# Option A Execution Control

Version: 2026-08-03
Status: mandatory control plan for full primary evaluation

## Roles and accountability

| Role | Accountable work | Appointment evidence |
|---|---|---|
| Study owner | Approves protocol, exclusions, resources, and escalation decisions | Named approval receipt |
| Phase 4 admission custodian | Controls manifest admission and quarantine | Signed admission receipt |
| H0/H1 remediation custodian | Resolves path anomaly and metadata provenance | Remediation receipt |
| H2 operator | Runs Claude Code/Opus condition | Harness and credential preflight |
| H3 operator | Runs Gemini condition | Trust/authentication preflight |
| H4 operator | Attests joins or reruns Codex condition | Operator attestation |
| H5 operator | Attests joins or reruns Qwen condition | Operator attestation |
| H6 operator | Establishes Kilo harness identity and runs | Harness identity receipt |
| H7 operator | Establishes Copilot harness identity and runs | Harness identity receipt |
| H8 evaluator coordinator | Appoints and briefs Human Expert evaluator(s) | Authority/conflict declaration |
| Scoring custodian | Creates sealed blinding and controls scoring workspace | Blinding receipt |
| IRR analyst | Independently scores subset and calculates kappa | Independence declaration |
| Track 5 reviewer | Reviews admission, blinding, scoring, and IRR | Closure receipt |
| Track 6 analyst/reviewer | Produces reproducible analysis and claims audit | Analysis and review receipts |

No role is treated as appointed until its receipt exists. One person may hold
multiple roles only where independence requirements are not compromised.

## Harness preflight required before every condition

Each H2-H7 operator must record:

- executable and version;
- model/provider identity;
- authentication status without secrets;
- endpoint and workspace trust state;
- read/write and approval mode;
- temperature and retry policy;
- case inventory and prompt hash;
- output paths and available storage;
- token/cost capture or an explicit unavailable reason;
- smoke-run result and operator attestation.

A failed or incomplete preflight blocks production runs for that condition.

## Condition runbooks

1. Create a fresh session for each canonical case/run slot.
2. Use the frozen case and prompt inputs; record hashes before execution.
3. Capture the unedited raw transcript and complete timestamps.
4. Record model, harness, endpoint, parameters, retries, token/cost fields, and
   failures in metadata.
5. Normalize only from the captured raw transcript into the required eight
   sections; record normalizer identity and transformation timestamp.
6. Hash raw, metadata, and normalized files.
7. Complete the operator attestation; submit as one atomic slot package.
8. Never reconstruct, infer, merge, or silently repair missing evidence.

H4/H5 cross-tree evidence may be admitted only when an attestation proves the
raw-to-normalized join by condition, case, run, harness, model, paths, hashes,
and transformation. Otherwise rerun canonically. H6/H7 empty outputs remain
quarantined. H8 requires one raw receipt per approved human case and cannot be
replaced by H8P.

## H0/H1 remediation rules

- Identify the extra H0 path and classify it as canonical, duplicate, failed,
  or out of scope without deleting it.
- Populate metadata only from raw transcripts, filesystem evidence, logs, or
  contemporaneous receipts.
- Record genuinely unavailable fields as unavailable with reason and authority;
  never estimate timestamps, tokens, costs, models, or operators.
- Rehash all admitted artefacts after remediation and retain the before/after
  provenance receipt.

## Submission and automated admission

Every slot package must pass a deterministic validator checking:

- canonical condition/case/run key;
- exactly one raw transcript, metadata record, normalized output, and
  attestation;
- non-empty raw and normalized files;
- required eight-section normalized structure;
- metadata schema and required unavailable reasons;
- matching hashes and path identities;
- no duplicate admitted key;
- no condition leakage into the blind scoring view.

Failed packages remain immutable in quarantine with diagnostics, responsible
owner, and next action. The admission custodian reruns the manifest audit after
each batch and issues a signed admission receipt.

## Schedule and escalation

T0 is the date the study owner appoints the required roles.

- T0+2 business days: all harness and H8 authority preflights submitted.
- T0+5 business days: smoke runs and H0/H1 remediation completed.
- T0+15 business days: first complete H2-H8 evidence batch submitted.
- T0+20 business days: remediation of rejected packages completed.
- T0+22 business days: final manifest audit and Option A viability review.

Escalate immediately for credential/security incidents, unavailable human
authority, evidence-integrity concerns, or protocol deviations. Escalate at
the relevant deadline for missing operator appointment, unavailable harness,
failed preflight, or incomplete evidence.

## Irrecoverability and contingency thresholds

A condition is potentially irrecoverable when any of these persists through
the T0+22 review:

- no authorised operator/evaluator;
- harness or required model cannot be obtained;
- authentication cannot be approved;
- canonical raw evidence cannot be recovered and rerun is impossible;
- required human authority or conflict safeguards cannot be satisfied;
- repeated packages fail integrity/admission checks after two remediation
  cycles.

The study owner must then select: extend Option A with a dated recovery plan,
authorise Option B through a protocol amendment, or authorise Option C. Silence
or missed deadlines do not automatically change the selected option.

## Option A completion gate

Option A is unblocked only when all role receipts exist, all expected slots are
admitted or covered by an authorised protocol decision, the canonical manifest
audit passes, and `tools/track5_preflight.ps1` exits successfully.
