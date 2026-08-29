# Mode assurance cases and runbooks

## Mode contracts

| Mode | Permitted content and processing | Required controls | Fail-closed condition |
|---|---|---|---|
| public remote | reviewed public or content-redacted material | known endpoint, provenance, telemetry, storage, egress, limits, and human review | any private classification or unknown disclosure field |
| governed hybrid | explicitly approved split processing; sensitive material only after approved de-identification | separate stores/keys/logs, transfer receipt, approved adapter and authority | missing de-identification, authority, or transfer evidence |
| fully local | authorised local material on an approved device | destination local, telemetry known, local keys/access/audit inherited | any remote destination or unknown egress |
| air-gapped | authorised local material and pre-positioned verified dependencies | no network path, local time/update provenance, offline rollback assets | unavailable dependency or attempted egress; never substitute network access |

## AI and clinical-safety gate

Before any model or external tool, record task, tool/model and exact revision,
mode, classification, network, telemetry, storage, limitations, and accountable
human review. Evidence insufficiency, conflicting evidence, uncertain
jurisdiction, unavailable capability, or unknown provenance requires
abstention or escalation. Assistance and systems analysis remain distinct from
clinical interpretation, policy/legal decisions, or regulated use. Unsafe
output is quarantined with a hash-linked reason receipt and cannot be promoted
without authorised review.

## Legal, records, cultural, and participation safeguards

The core never infers legal privilege or confidentiality protection from a
label. Records, access, disclosure, open disclosure, consultation, retention,
and deletion remain versioned jurisdiction or organisation rules. Unresolved
interpretation stays an explicit decision. Workflows must provide for
Aboriginal cultural-safety consultation, consumer/family participation, staff
support, procedural fairness, accessibility, and Just Culture without
automated culpability classification.

## Deployment checklist

1. Verify accountable owner, jurisdiction, system of record, mode, data class,
   and authority.
2. Verify identity, least privilege, device posture, encryption, keys, secrets,
   audit, backup, restore, and approved retention/deletion controls.
3. Verify network and telemetry state, dependency/model provenance, sandbox,
   remote-code policy, caches/logs/indexes, and rollback.
4. Run sentinel, routing, adversarial, recovery, quarantine, and assurance
   fixtures in the target environment.
5. Record limitations, residual risks, review due date, and owner decision.
6. Do not deploy while any required control is unknown, unavailable, stale, or
   awaiting risk acceptance.

## Incident and recovery

1. Deny the affected route and quarantine outputs; preserve bounded receipts.
2. Isolate affected adapters, credentials, stores, indexes, caches, queues, and
   logs using organisational incident-response controls.
3. Notify the accountable security/privacy/clinical owner through the approved
   process; this repository sends no message automatically.
4. Determine exposure, affected provenance, unsafe outputs, and downstream
   decisions. Do not infer breach status or notification duties.
5. Restore from a verified backup or clean dependency only after integrity,
   compartment, and authority checks pass.
6. Re-run fixtures and invalidate assurance until evidence and review are
   current.

## Key compromise

1. Stop use of the affected compartment and key; do not copy material to an
   alternate unapproved location.
2. Invoke the organisation's key-revocation, credential-rotation, access-log,
   incident, records, and notification procedures.
3. Re-encrypt or restore only under approved key custody and document affected
   versions and receipts.
4. Treat every previous assurance case depending on the key as invalid until
   an accountable owner reviews new evidence.

These runbooks are portable prompts and validation boundaries, not production
incident-response authority or residual-risk acceptance.
