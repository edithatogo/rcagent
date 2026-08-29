# Canonical benchmark harness

This directory contains synthetic, versioned contract cases and deterministic baseline results. It does not contain private incident material, clinical gold-standard judgements, approved operational thresholds, or published comparative claims.

Validate with `uv run python -m tools.benchmark_harness validate`. Run the local network-disabled baseline with `uv run python -m tools.benchmark_harness run --output evaluation/benchmark/results/deterministic-v1.json`, then render a bounded report with `uv run python -m tools.benchmark_harness report --result evaluation/benchmark/results/deterministic-v1.json --output evaluation/benchmark/results/deterministic-v1.md`.
