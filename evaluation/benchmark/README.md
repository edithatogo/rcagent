# Canonical benchmark harness

This directory contains synthetic, versioned contract cases, deterministic baseline results, and bounded local comparator receipts. It does not contain private incident material, model weights, clinical gold-standard judgements, approved operational thresholds, promoted models, or published comparative claims.

Validate with `uv run python -m tools.benchmark_harness validate`. Run the local network-disabled baseline with `uv run python -m tools.benchmark_harness run --output evaluation/benchmark/results/deterministic-v1.json`, then render a bounded report with `uv run python -m tools.benchmark_harness report --result evaluation/benchmark/results/deterministic-v1.json --output evaluation/benchmark/results/deterministic-v1.md`.

Comparator admission is declared in `comparators.json`. Validate isolated cached artefacts with `uv run python -m tools.local_model_comparator --model-root /path/to/model-cache --validate-only`. The comparator runner uses only the synthetic fixtures and writes an internal, non-promotion receipt. It does not download or redistribute weights, call external inference, or establish clinical, policy, legal, organisational, or operational approval.
