# Method Selection Matrix

> **Heuristics before methods.** Select the smallest method set that answers
> the investigation's open questions. Adding a method must serve an articulated,
> unanswered question — never completeness. See "Agent Selection Heuristics"
> below; escalating or stacking methods without an evidence signal is an error,
> not thoroughness.


## Primary Selection: By SAC Level

| SAC Level | Event Type | Recommended Methods | Timeframe |
|---|---|---|---|
| **SAC 1** | Death or serious harm; sentinel event | Timeline + Yorkshire Framework + Bow-Tie + SEIPS 3.0 ± London Protocol | 8–12 weeks |
| **SAC 2** | Moderate harm; significant temporary harm | Timeline + Yorkshire Framework + Fishbone OR London Protocol | 4–6 weeks |
| **SAC 3** | Minor harm; additional treatment required | 5 Whys + Yorkshire Framework (abbreviated) | 1–2 weeks |
| **SAC 4** | Near miss; no harm | 5 Whys | 48h–1 week |
| **Proactive** | New service, pathway, or high-risk process | FMEA + Bow-Tie | 2–4 weeks |

## Secondary Selection: By Event Characteristic

| Event Characteristic | Add This Method |
|---|---|
| Technology/device/EMR prominent | + SEIPS 3.0 |
| Human error prominent | + HFACS |
| Multiple organisational levels involved | + AcciMap |
| Complex sociotechnical system | + STAMP/STPA |
| Complex defence failures | + Swiss Cheese / Barrier Analysis |
| Patient safety culture concern | + Safety-II principles lens |

## Decision Questions

**Q1: What is the SAC level?** → Use SAC table above for baseline method set

**Q2: Is technology a major factor?** → Add SEIPS 3.0

**Q3: Are there significant human factors (fatigue, communication, decision-making)?** → Add HFACS

**Q4: Does the event reflect organisational or policy failures beyond the ward?** → Add AcciMap

**Q5: Are there multiple barrier failures?** → Add Swiss Cheese / Barrier Analysis

**Q6: Is this a proactive review of a new or high-risk process?** → Switch to FMEA + Bow-Tie

## Minimum Viable Investigation by SAC Level

**SAC 1 minimum**: Timeline + Yorkshire Framework + at least one systems-thinking method (SEIPS or London Protocol) + Bow-Tie for recommendations

**SAC 2 minimum**: Timeline + Yorkshire Framework

**SAC 3 minimum**: 5 Whys

**SAC 4 minimum**: 5 Whys or local team discussion with documented outcome

## Agent Selection Heuristics

Agents must choose methods from evidence signals, apply explicit stop rules,
and escalate only on triggers. Never run every applicable method; overlapping
methods re-answer the same question and dilute findings.

### Evidence-Signal Triggers

Inspect the timeline and preliminary contributing-factor pass **before**
selecting systems methods:

| Signal observed | Escalate to | Because |
|---|---|---|
| Contributing factor traced above ward level (Yorkshire category A/B/C reaching hospital executive, policy, regulator) | **+ AcciMap** | Factor sits outside local control; needs multi-level causal mapping |
| Human-performance chain dominates (fatigue, slips, communication breakdown, violations) and linkage to organisational pressures matters | **HFACS** (not AcciMap) | HFACS maps act → precondition → supervision → organisational influence directly |
| Control-structure flaw: automation governed poorly, responsibilities ambiguous between system elements, controller-feedback gaps | **STAMP/STPA** | AcciMap/HFACS map causality, not flawed control loops |
| Work-system redesign question raised (tooling, tasks, environment, organisation interactions) | **SEIPS 3.0** | Produces actionable work-system dimensions, not just causes |
| Recurrent event type, trend across investigations | Aggregation note → register | Single-case deep dive adds little; aggregate analysis does |
| No factor above ward level, no technology, no human-factors depth | Stop at baseline set | Deepening adds cost without new answer classes |

### Mutually Exclusive Escalations

Do **not** stack these unless SAC 1 with multi-agency scope makes each
individually justified:

- **HFACS vs AcciMap**: pick by dominant locus — human-performance chains → HFACS; policy/regulatory/system-design chains → AcciMap. Both when an incident genuinely spans both domains end-to-end.
- **AcciMap vs STAMP/STPA**: pick by failure logic — causal flow across organisational tiers → AcciMap; unsafe *control* and feedback structure → STAMP/STPA.
- **London Protocol vs Yorkshire Framework**: either satisfies systematic contributing-factor identification; never both. Default Yorkshire (matches AU/NZ practice); London Protocol when structured clinician interviews will drive factor capture.

### Method Budget and Stop Rules

| SAC | Maximum distinct methods (incl. mandatory set) | Mandatory set |
|---|---|---|
| SAC 1 | 4 | Timeline + Yorkshire + 1 systems method |
| SAC 2 | 3 | Timeline + Yorkshire (abbreviated) |
| SAC 3 | 2 | 5 Whys + abbreviated Yorkshire |
| SAC 4 | 1 | 5 Whys |

Stop rules:

1. **Open-question rule.** Add a method only when a specific, stated question remains unanswered and the method is designed to answer it. Record the question before applying the method.
2. **Delta rule.** If a completed method changed neither any finding nor any recommendation versus prior methods, record why it ran (or that selection erred) and exclude it from this scenario signature next time.
3. **No-summary-stacking.** Methods in the summary/report repeat no other method's output; if two outputs coincide, keep the stronger-grained one and cite it.
4. **Proactivity gate.** FMEA/Bow-Tie are prospective tools; they never substitute for retrospective analysis after an event, and retrospective reviews never default into proactive tooling without a scoped redesign request.

### Anti-Patterns

- Running AcciMap "for completeness" on every SAC 2 — its value collapses when four of six levels hold no actors with causal contribution.
- Six-method "kitchen sink" reports: each extra method reduces reader retention of genuine systemic findings.
- Starting at Bow-Tie/FMEA (barriers/prospective) before factual timeline exists (see Method Combination Guide sequencing).
- Treating method count as rigour: rubric dimension scores reward correctly-scoped systemic analysis, not volume (see evaluation-rubric D-dimensions).
