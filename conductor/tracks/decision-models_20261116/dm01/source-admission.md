# DM01.2 — Candidate source and rights admission

Date: **17 November 2026, Australia/Brisbane**. The primary-source queries ran
on 16 November 2026 UTC; their exact timestamps are retained in
[candidate-admission.json](./candidate-admission.json). The track identifier
remains `decision-models_20261116`. Each UTC timestamp with a fractional second
uses a whole-second string and an adjacent integer microsecond component. This
preserves its instant while avoiding the privacy scanner's known false
identification of decimal timestamps as phone numbers; raw response hashes are
unchanged.

**Result:** one concrete local decision-model candidate has an immutable
source identity for the first synthetic text study. Execution remains
unadmitted. The generative comparator is explicitly deferred to DM03 before
the model manifest is frozen. No weights were downloaded, no model was run,
and no runtime dependency or support-registry entry was changed.

## Question and admission boundary

The canonical [study protocol](./study-protocol.json),
`dm01-synthetic-intake-v1`, owns the question wording, references and analysis.
It calls for six separate usable-field/completeness Noul predicates and one
synthetic escalation-required Noul predicate on the same source-bound text
packet. It does not require ontology coding, statutory adjudication, an
operational severity scale, images, audio, video, Choice, Score or extraction.

DM01.2 distinguishes three evidence levels:

1. **Documentation evidence** describes an available interface or intended
   capability. The earlier [source register](../sources.md) remains discovery
   material; mutable documentation is not an executable model manifest.
2. **Immutable source identification** binds full commits and file identities.
   The machine-readable record supplies the exact reference model, selected
   GGUF, tokenizer/configuration, processor, licence and runtime/API provenance.
3. **Execution admission and empirical qualification** require actual assets,
   rights applicability, build/device/isolation receipts, accepted contracts
   and measured behaviour. None is inferred from the first two levels.

This finite disposition satisfies the source-inventory part of DM01. It does
not complete DM02, DM03, calibration or the comparison study.

## Selected immutable identities

| Component | Identity | Evidence and present status |
|---|---|---|
| Current d1 source reference | `LiquidAI/d1-2B` at `a6bce774e6dde338dcc3036ceb5d91f78bf4c19e` | [Pinned Hub metadata](https://huggingface.co/api/models/LiquidAI/d1-2B/revision/a6bce774e6dde338dcc3036ceb5d91f78bf4c19e?blobs=true). Source/configuration/licence reference only; not an admitted Transformers route or a proven source revision for the older GGUF. |
| Selected D artefact | `LiquidAI/d1-2B-GGUF` at `4a181094d1b6addfaa3a0956f78e7ab2aa406a0c`, `d1-2B-Q8_0.gguf` | [Pinned Hub metadata](https://huggingface.co/api/models/LiquidAI/d1-2B-GGUF/revision/4a181094d1b6addfaa3a0956f78e7ab2aa406a0c?blobs=true). Publisher reports 1,846,240,576 bytes and LFS SHA-256 `073313d92b53b0ac8193db6e906cb3c78a98183d244b15b7b8f5426115c6738c`. Weight bytes were not retrieved or independently verified. |
| Runtime source | `ggml-org/llama.cpp`, tag `b11960`, commit `8642541b255bfb5dc39cd351a178be09013a55d6` | [Commit metadata](https://api.github.com/repos/ggml-org/llama.cpp/git/commits/8642541b255bfb5dc39cd351a178be09013a55d6) identifies version 0.8.0 and tree `10602a4338fd3d7eafb4144463f78ed35fe2a8f0`. The full tree listing was not truncated. This pins source, not an executable or a working installation. |
| Selected API | Local `POST /v1/systemone` in that runtime commit | [Pinned server documentation](https://github.com/ggml-org/llama.cpp/blob/8642541b255bfb5dc39cd351a178be09013a55d6/tools/server/README.md) and [implementation](https://github.com/ggml-org/llama.cpp/blob/8642541b255bfb5dc39cd351a178be09013a55d6/tools/server/server-decision.cpp) identify a Noul path. No server was started and no endpoint was called. |
| Generative comparator G | **Deferred to DM03 before model manifest freeze** | No model ID, revision, weight digest or rights entitlement is invented. G and H, and the planned G/D/H comparison, remain blocked until one independently admitted local G is fixed. |

Q8_0 is a specific candidate, not permission to fall back to another
quantisation. The official GGUF model card and the pinned upstream Noul branch
make this a feasible route to investigate without executing repository-supplied
Python code. They do not establish local compatibility, latency, calibration
or incident-investigation usefulness.

## What was actually verified

Primary public metadata was read from the Hugging Face Hub and GitHub APIs.
Twenty-two small text files were fetched at the selected commits: twelve from
the current d1 source reference, the GGUF README and licence, and eight runtime
source/documentation/licence files. For each, SHA-256 was calculated over the
received bytes, and its Git blob SHA-1 was independently calculated and matched
to the primary publisher metadata. The JSON record contains per-file URLs,
sizes, identities, timestamps and verification flags.

The 35-file reference inventory also records metadata identities for source
files, templates and large assets that were not fetched. In particular,
`model.safetensors`, `tokenizer.json` and the selected GGUF have **publisher
digests**, not local content-verification receipts. No downloaded source was
imported or executed. Selected interface passages were inspected; this was not
a comprehensive code or security audit.

| Small-file evidence | Locally calculated SHA-256 |
|---|---|
| d1 reference `api.py` | `d57845b414b6766cd0410f0437080244320adebd4f9f031a03777acbec243d2a` |
| d1 reference `tokenizer_config.json` | `594a96e4caedd07536a595b48f5dc84655bd672b715b6ac891ca3d503d439f76` |
| d1 reference `processor_config.json` | `37396ef3370083a04381ef25f9e1b50dec184b8cdcf08cf718feb8944ad8f3bc` |
| d1 reference `calibration.json` | `e534464458f485d800fe6cc896ac241590bbc8cd54f5af08f7b3064b0d884d69` |
| LFM licence, independently fetched from both model repositories | `4d28ca14dedc0b3d0fcc2b3339f0e79931faa33874f3d24f522183a8fc70068c` |
| llama.cpp `tools/server/server-decision.cpp` | `86379ffbf753cbe4ae90cebd60d5df62cda44cf37459e4e1de2db081fec8652b` |
| llama.cpp `tools/server/README.md` | `8fd5abde2fb52de3b30f30a170631d4c0d92febecc8da44d0541e48b132b35c6` |
| llama.cpp `LICENSE` | `94f29bbed6a22c35b992c5c6ebf0e7c92f13b836b90f36f461c9cf2f0f1d010d` |

The reference tokenizer's publisher LFS SHA-256 is
`a39eed58008cbcbc09e5b629b81338a654269c64cd13348aaa6090f4db75c7e7`.
The selected GGUF's embedded tokenizer, template and calibration data have not
been inspected. The current source snapshot must not be asserted to be the
input to an older conversion. Exact converter input/build and reference parity
remain unverified. A later study can describe the selected artefact as its own
measured tuple; it cannot present an unverified conversion relationship as fact.

The JSON API response hashes are observation receipts. Future responses can
change counters or formatting even when the selected repository revision does
not change. GitHub reported a valid commit signature; independent signature
verification was not performed.

## Runtime semantics and conflicts retained

**Noul:** the pinned server returns the probability associated with `true`.
The protocol must keep missing, malformed, timeout and unavailable outcomes
separate from that numeric probability. Seven named questions may share one
HTTP request, but the documentation describes independently evaluated questions.
The seven-question procedure is not a demonstrated single physical forward
pass. Later cost and latency measurements cover the full procedure.

The pinned endpoint documentation reports zero output tokens and explicitly
warns that its probability scaling does not guarantee calibration on new data.
These are interface statements. They establish neither sub-100–200 ms latency
nor a cost, calibration, absence-of-error or safe-auto-resolution guarantee.
No such measurement was made in DM01.

**Score discrepancy:** the generic server README describes a
probability-weighted expected index, whereas its pinned LFM3 d1 implementation
returns the first ordinal level whose cumulative probability reaches 0.5. The
current [reference API](https://huggingface.co/LiquidAI/d1-2B/blob/a6bce774e6dde338dcc3036ceb5d91f78bf4c19e/api.py)
also defaults to a median readout. Score is outside this study. A later Score
adapter must retain the distribution and verify its specific native semantics;
the generic README cannot justify silently replacing the readout.

**Typed Answers:** the reference Python API applies its `found` gate at 0.5;
values below that threshold are missing. That reference implementation is not
evidence of a Typed Answers endpoint in this GGUF route. Extraction, multi-label
Choice and media are excluded from the selected experiment.

**Transformers conflict:** the current model configuration maps to
repository-specific `D1Model`/`Lfm3VlConfig` classes, and the documented route
uses `trust_remote_code=True`. The recorded configuration version field is
`5.19.0`; it is not a pinned compatible environment. The repository's runtime
policy has `remote_code=false`. A code hash does not remove this conflict, and
DM01 neither changes that policy nor vendors custom code as a bypass.

**Existing runtime registry:**
[`evaluation/runtime-lab/registry.json`](../../../../evaluation/runtime-lab/registry.json)
contains no admitted models. Its llama.cpp entry is `installed_unmeasured` and
has a generation interface. It is not a qualified System One service. The
observed registry digest and all five false policy flags are recorded in the
JSON; this work does not mutate them.

## Rights disposition

The exact [LFM Open License v1.0 text](https://huggingface.co/LiquidAI/d1-2B-GGUF/blob/4a181094d1b6addfaa3a0956f78e7ab2aa406a0c/LICENSE)
was retrieved and matched across both model repositories. Its commercial-use
and revenue conditions, qualified-non-profit/research provisions, and
attribution/retention/redistribution requirements need an actual entity/use
applicability decision. Public access and an open-weight description do not
make that decision. No organisational entitlement, unrestricted research
entitlement or redistribution entitlement is asserted here.

The selected runtime's [MIT licence](https://github.com/ggml-org/llama.cpp/blob/8642541b255bfb5dc39cd351a178be09013a55d6/LICENSE)
was separately pinned and hash verified. It does not grant rights in the model,
data or a future terminology package. No private/clinical corpus or terminology
content was accessed in this increment.

## Explicit exclusions and deferrals

These are dispositions for the first study, not unsupported claims that the
named technologies do not exist. The JSON retains the discovery links and
specific missing admission evidence. None is an automatic substitute for D
or G.

| Requested candidate or material | First-study disposition |
|---|---|
| d1-Omni-2B and d1-omni-600M | Excluded: no audio/media question. Their exact model, processor, rights and runtime tuples are not admitted. |
| Hosted d1.1/d1-ultra; Liquid API, OpenRouter, Vercel AI Gateway | Excluded: local-only study; no immutable served-model identity, data terms or egress admission. No hosted fallback. |
| TypeSafe Jev; Cloudflare Clef | Deferred: no exact alternative variant, weight/tokenizer/licence/build tuple selected. Hosted and open-weight offerings are not interchangeable. |
| GLiNER, ModernBERT, DeBERTa, SapBERT, KRISSBERT, BioClinicalBERT and MedCAT | Excluded: no NER/linking condition. Checkpoint, code, tokenizer, modelpack, corpus and terminology rights are separate unresolved admissions. |
| FAISS and Qdrant | Excluded: this procedure needs no vector index. No dependency, container or index was selected or installed. |
| SNOMED CT, SNOMED CT-AU, UMLS, ICD-10 and ICD-10-AM/ACHI/ACS | Excluded: no edition, mapping, access or redistribution entitlement is selected. These are distinct systems, not substitutes. |
| ICPS and HFACS | Excluded: no local versioned taxonomy or healthcare adaptation is selected. A framework description is not an admitted universal code profile or a validated causal attribution system. |
| HDC and MedMentions | Excluded from this corpus. Earlier HDC authority is not extended; no external release, split, terminology entitlement or new data access is claimed. |
| When2Call, Artificial Analysis Decision Index and AA-Symmetry | Methodological discovery only. No dataset is imported, no controller installed and no private AA-Symmetry reproduction or access entitlement claimed. |
| Transformers execution, mlx-vlm, Ollama, ONNX, FastAPI and Power Automate | No alternative runtime/conversion, deployment service or connector is admitted. Shared API naming does not establish parity with the pinned upstream route. |

The corpus is to be authored as original synthetic incident families under the
protocol. At DM01 completion there are no generated study cases, reference
labels, partitions or model outputs to hash. Future packages bind those actual
artefacts before the relevant freeze; this source inventory does not invent
their existence.

## Remaining blockers and exact closure scope

| Blocker | What it blocks | Required evidence |
|---|---|---|
| DM01-SB01 | D/H execution | Lawful acquisition and local verification of selected bytes; executable/compiler/dependency/device identity; measured Noul capability and actual isolation. |
| DM01-SB02 | Model use or redistribution | Actual entity/use rights applicability, with the selected licence text retained. |
| DM01-SB03 | Conversion-equivalence and calibration claims | Inspect embedded tokenizer/template/calibration identities; document converter/reference limitations and create task-specific calibration lineage. |
| DM01-SB04 | G, H and planned three-arm comparison | One exact independently admitted local G before model/holdout freeze. H reuses the same G and D. |
| DM01-SB05 | Integrated or thresholded use | Accepted contracts and seven-question adapter; discriminating missing/timeout/probability controls; later calibration and threshold receipts. |
| DM01-SB06 | Empirical conclusions | Actual corpus/reference/partition/analysis manifests and complete attempt/resource observations under the frozen protocol. |

If either G or D cannot be admitted, the planned comparison remains blocked.
A D-only pilot must not be relabelled as its completed comparison, and model selection or replacement may not use calibration, threshold-selection
or holdout outcomes. The bounded training-only selection procedure is allowed
exactly as prespecified; its chosen model/prompt is fixed before those later
partitions are accessed. Revision, quantisation, runtime,
tokenizer/template or procedure changes require a new exact tuple and the
associated calibration/threshold validity review. DM01.2 closes with this
concrete inventory and explicit unadmitted scopes; it makes no performance or
deployment claim.
