# Cognitive autopsy evaluation workspace

This is the planning namespace for a new prospective study. No evaluation has been run by adding these files, and no model is qualified.

- [Study design manifest](./study-design.json)
- [Conductor track](../../conductor/tracks/cognitive-autopsy_20261107/index.md)
- [Evaluation design](../../conductor/research/cognitive-autopsy/evaluation-design.md)
- [Component contracts](../../conductor/research/cognitive-autopsy/component-matrix.md)

The manifest is not an executable run manifest. Implementation must resolve and hash sources, partitions, prompts, runtimes, hardware and metrics before a run can be admitted. Keep case payloads, identifiers, sensitive outputs and approval documents in the governed local study store. Only non-sensitive receipts belong in this repository.

Historical benchmark and H0–H8/H8P results remain unchanged. Do not fill this namespace with copied historical results or synthetic outputs labelled as HDC observations.

## Component experiments

[Experiment catalogue](./experiment-catalogue.json) contains eight planned questions and 25 bounded work packages. It is non-executable and carries empty run/qualification arrays. [Candidate dataset metadata](../../conductor/research/cognitive-autopsy/component-datasets.json) is an inventory, not dataset admission. Conventional NLP/encoder baselines, controlled variants, process reconstruction and verifier experiments are specified in the linked research documents.
