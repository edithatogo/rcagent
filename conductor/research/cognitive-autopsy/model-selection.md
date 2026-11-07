# Local model experiment shortlist

## Selection policy

These are priorities for experiments, not qualified models or supported hardware recommendations. No candidate was executed by this planning update. The best model is the one that passes a specified task/context evaluation with acceptable resource use, not the one with the strongest unrelated leaderboard result.

Use a short development tournament, then freeze finalists. Do not benchmark every available model on the final test set. Exact Hub commit, weight hashes, tokenizer/template, licence, runtime/build, quantisation, hardware, reasoning budget and context envelope are required before execution.

## Candidates and roles

| Candidate | Role and rationale | Trade-off and admission facts |
| --- | --- | --- |
| [Qwen/Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | First general local baseline for structured claims, temporal reconstruction and source-grounded decision context | Apache-2.0 on the publisher card. Start with text; native multimodality does not qualify clinical image interpretation. Verify current runtime support and quantify context/truncation effects. |
| [google/medgemma-1.5-4b-it](https://huggingface.co/google/medgemma-1.5-4b-it) | Medical-specialised comparator for clinically material detail | HAI-DEF terms and gated access. Compare with a general model; medical adaptation is not evidence of better RCA or calibrated uncertainty. Publisher limitations include lack of optimisation/evaluation for multi-turn applications. |
| [google/gemma-3-4b-it](https://huggingface.co/google/gemma-3-4b-it) | Parent-family control alongside MedGemma to examine the value of medical adaptation | Gemma terms, not Apache-2.0. This is a useful architectural/size control, not a claim that every pre/post-training difference is isolated. |
| [openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) | Local reasoning/verification challenger; test low/medium reasoning budget and a bounded critic role | Apache-2.0, native Harmony format and MXFP4. Publisher states a 16 GB memory fit; actual context, KV cache, concurrency and runtime overhead need measurement. Do not show reasoning traces as evidence of a clinician's cognition. |
| [LiquidAI/LFM2.5-1.2B-Instruct](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct) | Optional fast local extractor/router for short, tightly specified source-grounded tasks | Hybrid convolution/attention architecture; LFM Open License v1.0. The publisher discourages knowledge-intensive tasks. Do not appoint it the final clinical reasoner. Its value must survive comparison with rules and the general baseline. |
| [Qwen/Qwen3.5-27B](https://huggingface.co/Qwen/Qwen3.5-27B) | Optional scale challenger if smaller models miss important context and sufficient hardware is available | Apache-2.0; greater weight and runtime cost. Add only to answer a specific capacity question. |

An alternative efficiency experiment is [LiquidAI/LFM2-24B-A2B](https://huggingface.co/LiquidAI/LFM2-24B-A2B), whose publisher describes a hybrid mixture-of-experts model under LFM Open License v1.0. Use it instead of an additional large-scale arm when CPU/RAM efficiency is the research question. Active parameters affect compute; total weights still need storage/memory. Neither it nor a larger Qwen model is required for the first paper.

The model-selection evidence consists of the linked primary cards, reviewed 2026-11-07, and the [MedGemma limitations](https://developers.google.com/health-ai-developer-foundations/medgemma/model-card). Publisher benchmarks are motivation only, not rcagent evaluation results.

## Practical local combinations

1. **Lean first system:** deterministic parsing/validation + Qwen3.5-9B + compartment-bound lexical retrieval. This is the primary architecture to beat.
2. **Medical adaptation comparison:** MedGemma versus Gemma-3-4B with the same evidence and task rubric. Keep it as an empirical comparison rather than assigning medical tasks by brand.
3. **Staged local system:** rules or LFM extraction → the better qualified general/medical reasoner → a different local model checking source support and omissions. Route only within admitted capabilities. Require an ablation showing the critic improves material-error/coverage outcomes; correlated agreement is not validation.
4. **Resource-constrained fallback:** rules and a small extractor produce chronology and evidence links, with judgement withheld. A useful bounded product can exist without a model that passes interpretation.

Load models sequentially if concurrent memory is excessive. A model cascade should use calibrated task/uncertainty rules and local state, not unrestricted multi-agent deliberation. Keep deterministic checks outside all model authority.

## Hardware and runtime evaluation

As arithmetic lower bounds, four-bit storage is roughly 0.5 bytes per parameter: about 0.6 GB for 1.2B, 2 GB for 4B, 4.5 GB for 9B and 13.5 GB for 27B. These are decimal weight-only approximations, not deployment memory requirements; quantisation metadata, unquantised modules, activation/KV caches, context, runtime and operating system add memory. Measure actual peak RSS/VRAM and wall time on the intended device. Do not claim a fit from model size alone.

Reuse llama.cpp for supported GGUF/CPU/GPU configurations, MLX for supported Apple silicon configurations, and Transformers/vLLM when the available GPU and architecture support justify them. ONNX/OpenVINO are candidates for compatible small-model paths, not assumed universally interchangeable.

Record cold load and warm inference separately; test short and long source contexts, batch size one first, then intended concurrency. Fix source evidence and cap generated tokens/reasoning budget. A model that silently truncates a critical cue is a failed configuration even if its output is valid JSON.

Pin acquisition outside the sensitive execution environment. [Hugging Face offline mode](https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables) and [Ollama local-only configuration](https://docs.ollama.com/faq) supplement, but do not replace, the enforced network boundary.

## Existing user adapters

- [qwen3-4b-hermes-lora-peft-converted](https://huggingface.co/edithatogo/qwen3-4b-hermes-lora-peft-converted): a candidate tool-format adapter. The card's format instructions and small pilot examples do not establish clinical value. Compare it against its exact Qwen3 base for tool/schema tasks before considering it in this programme.
- [lfm2.5-1.2b-intel-lora](https://huggingface.co/edithatogo/lfm2.5-1.2b-intel-lora): the card describes synthetic smoke-test weights, not a fully trained LFM clinical model. It must not be treated as the official Liquid model or a clinically fine-tuned candidate.

## Fine-tuning value test

Start untuned. Fix source preparation, retrieval, prompts, output constraints and decoding first. Trigger one bounded adaptation only for a reproducible residual error with adequate authorised labels. Use the paired, case-family-held-out decision rule in the [evaluation design](./evaluation-design.md). Compare against the strongest untuned system, not an intentionally weak prompt.

If fine-tuning produces no reliable patient-relevant quality improvement, worsens abstention/grounding, memorises source text or adds unjustified maintenance cost, retain the untuned model. This negative result is part of the research contribution.
