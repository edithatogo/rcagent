# Optional cloud orchestration with a local data boundary

## Architecture decision

The default is a fully local pipeline. An optional cloud model may assist with public code, schemas, experiment planning and scheduling of preapproved task templates. All sensitive case content, inference, retrieval, evaluation and reports remain inside a locally governed environment. This is a new profile to implement and test, not a claim that the current governed_hybrid mode already enforces this stronger boundary.

A cloud agent that cannot inspect the case cannot make case-informed clinical judgements. Its value is generic workflow preparation; local deterministic logic and local models choose case-dependent actions. Evaluate whether the cloud layer adds enough operational value to justify its additional attack surface.

## Trust boundaries and allowed messages

| Boundary | Permitted | Prohibited |
| --- | --- | --- |
| Cloud planner → local broker | Signed/versioned allowlisted template ID, public schema version, opaque random job token, bounded resource class | Free-form case prompts, shell commands, arbitrary code/URLs, model downloads, policy changes, new tools, secrets |
| Local broker → isolated worker | Locally resolved source handles, admitted configuration, least-privilege task capability and budget | Access outside the assigned case compartment; unadmitted tools or unrestricted network |
| Worker → local result store/UI | Sensitive output, citations, traces and evaluation artefacts under local access control | Automatic forwarding to cloud chat, hosted CI, tracing services, error reporting, analytics or shared indexes |
| Broker → cloud scheduler | Prefer acknowledgement of template receipt only; optional coarse status independent of case content under explicit metadata policy | Patient text, summaries, embeddings, scores, labels, findings, filenames, stack traces, token counts, detailed timing or data-derived errors |

Opaque identifiers must be freshly random, not hashes of public or sensitive case IDs. Mapping stays local. Detailed progress can disclose cohort composition or encode data; the strongest profile has no data-dependent return channel. If fixed/coarse status is used, test and document its residual metadata leakage instead of claiming perfect non-interference.

## Enforcement

Use a deterministic broker outside the model's authority. It validates signatures, template hashes, schema, nonce/expiry, quotas and capabilities, then resolves local input handles. It refuses instructions that alter firewall, credentials, audit, retention, source access or output policy. A local model's tool request is untrusted and independently checked.

Workers run in separate processes/containers or stronger host isolation as appropriate, with read-only source mounts, scoped output directories, no cloud credentials, no host control socket, no shell tool and denied network egress including DNS. Bind inference servers to loopback or the approved isolated local network with authentication. Prevent other local users/processes from reading the inference endpoint or store.

Prepare model weights and dependencies in a separate update environment; pin and verify artefacts before transfer. Disable remote-code execution, hub downloads, telemetry, crash uploads, cloud fallbacks and remote experiment tracking. Cache misses, licence uncertainty, timeouts and insufficient capability fail locally. Offline environment flags are defence in depth, not a firewall.

Keep logs, prompts, generations, reasoning traces, embeddings, vector stores, caches, backups and temporary files inside the same governed boundary. Encrypt and apply organisational identity/retention controls. Build code with synthetic fixtures in cloud tooling; run sensitive integration tests only locally. Do not copy an actual failure payload into a GitHub issue.

Treat report text, retrieved passages and model responses as untrusted data. Validate structured output; never execute embedded instructions. Separate the case-data workflow from software updates so a compromised cloud planner cannot ship new code that opens an egress path.

## Required adversarial evidence

Before sensitive hybrid execution, test actual network behaviour, not only mocked routing:

1. Put unique synthetic canaries in source text, names, metadata, OCR, attachments, tool results and errors. Capture traffic at worker and gateway boundaries during success and failure.
2. Attempt direct HTTP/DNS, redirects, fallback providers, model-hub fetches, telemetry, crash reports, log exporters and cloud tracing. Test library updates and cold caches.
3. Attempt prompt injection, cross-case retrieval, malicious filenames, output parser abuse, job replay, path traversal, unsigned templates and arbitrary task parameters.
4. Attempt covert return via job IDs, status codes, progress counts, size, timing and repeated jobs. Bound or remove each channel; rate-limit the broker.
5. Kill the worker, corrupt inputs, exhaust memory and fill storage. Confirm no remote rescue path and no private diagnostic payload.
6. Verify local access control, encrypted storage/backups, deletion/retention behaviour and audit completeness. Retain signed receipts without case content in the public repository.

A passed canary suite supports a bounded assurance claim; it is not a mathematical proof that no possible disclosure can occur. DLP/string matching cannot establish this architecture alone. Any unaccounted egress blocks hybrid admission and leaves the fully local path available.

## Deployment trade-offs

Fully local operation is simpler and makes a stronger data-boundary claim. Cloud scheduling can reduce planning friction but adds credentials, metadata exposure, supply-chain paths and maintenance. A secure hospital network or remote on-premise GPU can still be locally governed; a vendor-hosted endpoint is not local merely because it is private.

Adopt the hybrid option only after a measurable benefit and the exact boundary evidence exist. The approved next step here is design and non-sensitive implementation planning; no cloud connection to clinical data is created.
