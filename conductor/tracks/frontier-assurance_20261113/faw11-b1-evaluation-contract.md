# FAW11 / Checkpoint B — frozen synthetic comparison development lane

The case-family reference manifest was committed separately **before** the
implementation and contains exactly 48 fixed synthetic text observations across
24 root families: 24 train, 8 development, 16 test. Each of the four classes
has 4 test observations, grouped in 2 distinct test families. The manifest
contains source text and human-authored synthetic class labels, not predictions
from the producer and not independent clinical adjudication or patient records.
Do not substitute it for an external clinical holdout.

## Bounded comparison contract

- Construct actual D3 source/version/byte-span witnesses and recipient/cutoff
  packets from each synthetic record. All D4 arm inputs are the same
  label-excluding D3-projected evidence. The untrusted source content remains
  distinct from label and authority metadata.
- Freeze all family splits and labels before developing an algorithm. Only
  train-family labels fit the conventional classifier; development/test labels
  are evaluation-only. Reject root-family leakage, duplicate IDs and mismatched
  partition counts. The reference manifest must be hashed and version-pinned.
- Compare (1) the existing D4 fixed regex baseline, (2) bounded deterministic
  token/negation/experiencer and section-style rules (a **ConText-style** software
  analogue, **not** a claim to have run spaCy or medspaCy), and (3) a
  conventional four-way sparse linear perceptron trained solely on the
  predeclared synthetic training cases. These use the portable Python standard
  library, deterministic fixed algorithms, and no network, model download,
  private data or extra dependency.
- (4) Structured local LLM generation must remain explicitly **unavailable**
  without a pinned offline runtime, licensed model/tokenizer and actual
  observed inference. A deterministic template or injected prediction file
  must not masquerade as an LLM result. Implement a thin optional adapter only
  after compatible model/runtime admission.
- Emit complete eligible/test denominators, correct/incorrect/abstentions,
  conditional accuracy, macro-F1, class-wise precision/recall and false
  positives/omissions. Retain nullable precision for no positive predictions;
  abstentions count as false negatives for recall.
- Metamorphic/integrity tests require unchanged actor/cutoff/method input under
  changes confined to frozen reference labels, correct original UTF-8 spans
  and hashes, permuted source order, missing/withdrawn records, and negative
  cases for duplicated families and forbidden future access.

## Acceptance boundary

Completing this synthetic development lane is **not** completing Checkpoint B
for D0–D3 or a clinical holdout. The full Checkpoint B requires independent
component-specific heldout references, adverse and metamorphic tests and honest
precision/recall/abstention for each accepted component. A fitted linear
classifier is an executed *conventional baseline*, not a generative LLM or
clinical qualification. A software-only comparator improvement must not be
called frontier or evidence of patient benefit.

A durable local/hosted receipt must name the exact manifest hash, code revision,
locked dependencies, method status and output. Preserved failed/negative runs
remain in the PR record. Nothing here weakens the CI quality gates.
