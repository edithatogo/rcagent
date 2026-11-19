# AcciMap — Accident Mapping

Use AcciMap to examine how decisions, activities and conditions across a
sociotechnical system contributed to an incident or shaped its consequences.
Keep the purpose focused on system improvement and the conditions of normal
work. A plausible diagram, a citation or a completed review does not prove a
causal explanation.

## Contents

- [Select a profile](#select-a-profile)
- [Facilitate the analysis](#facilitate-the-analysis)
- [Check the map](#check-the-map)
- [Produce the diagram and handoff](#produce-the-diagram-and-handoff)
- [Select complementary methods](#select-complementary-methods)
- [Sources and adaptation](#sources-and-adaptation)

## Select a profile

Record the profile and why it fits the question. AcciMap variants use different
level structures; the existing template is a healthcare adaptation authored for
rcagent, not a universal six-level standard. Preserve its legacy level numbers
when reusing an existing map; changing a profile requires reviewing placement.

| Position from top | `rcagent-healthcare-six-v1` | `rasmussen-svedung-six-v1` |
|---|---|---|
| 1 | Government and policy; legacy level 6 | Government policy and budgeting |
| 2 | Regulatory bodies; legacy level 5 | Regulatory bodies and associations |
| 3 | Hospital management; legacy level 4 | Local government / company management |
| 4 | Physical and technical environment; legacy level 3 | Technical and operational management |
| 5 | Staff and operators; legacy level 2 | Physical processes and actor activities |
| 6 | Patient and activity; legacy level 1 | Equipment and surroundings |

The original hierarchy distinguishes organisational leadership from operational
management. In a healthcare adaptation, explain where service-level management,
rostering and coordination sit rather than hiding them inside staff actions.
Outcome is a node role: the original profile does not require a patient outcome
to be placed in equipment/surroundings. Keep patient context distinguishable from
the adverse outcome and from claims about responsibility.

Do not invent factors to populate every level. Record whether a level was
examined, outside the agreed scope, or remains unexplored. Leave uncertain
placement explicitly unassigned, with a rationale and a question for review.

## Facilitate the analysis

Apply the shared investigation workflow and evidence boundary first. These steps
are an original facilitation synthesis of the sources below and rcagent's
existing evidence/review requirements; they are not a jurisdictional mandate.

1. **Define scope and outcomes.** State the question, system boundary, time
   period and event/outcomes. Agree who needs to participate, including knowledge
   of frontline work, management decisions and relevant policies. Preserve
   patient/family perspectives and unresolved differences.
2. **Assemble evidence and chronology.** Gather authorised records, accounts and
   applicable policy versions. Separate observations, accounts and inferences;
   record missing information. A timeline is an organising aid, not proof of a
   causal connection.
3. **Identify and consolidate factors.** Describe specific conditions and
   decisions, including normal adaptations and successful controls. Combine
   genuine duplicates while preserving distinct mechanisms and conflicting
   accounts. Avoid labels such as "human error" as the explanation.
4. **Place factors deliberately.** Use the selected profile, explain ambiguous
   placement and consider organisational/external influences. Split a compound
   factor when it contains distinct decisions at different levels.
5. **Propose relationships.** For each connection record its direction,
   mechanism/rationale, supporting evidence, conflicting evidence, alternatives
   and uncertainty. Distinguish supported, hypothetical and contested links.
   Multiple causes/effects, same-level links and skipped levels are possible.
6. **Expose gaps.** Look for missing intermediate conditions, unexamined upstream
   influences and disconnected factors. Request evidence or retain the gap;
   never add a convenient link simply to complete a pathway.
7. **Challenge the explanation.** Check chronology and causal logic, alternative
   explanations, hindsight and whether a proposed link exceeds the evidence.
   A graph path establishes connectivity only. Factor counts are not estimates
   of causal importance, effect size or an organisation's share of responsibility.
8. **Develop improvements.** Link each recommendation to the factor or
   relationship it addresses and explain the intended safety mechanism. Assign
   actions through actual governance authority; define implementation evidence,
   outcome/process/balancing measures and an effectiveness review.
9. **Validate and revise.** Ask knowledgeable participants to check the account
   and other readers to check intelligibility. Preserve dissent and unresolved
   evidence. Record the reviewed revision, reviewer role, disposition and limits;
   changes to the map or evidence require renewed review of the affected claims.

## Check the map

Before presenting a map as reviewed, check:

- Outcomes are explicit and incident outcomes are separate from later learning
  or action-effectiveness measures.
- Nodes and links have stable identifiers; each claim resolves to its source.
- A supporting citation has not been silently converted into a causal arrow.
- Hypotheses and contested relationships remain visibly labelled in every view.
- Gaps and unassigned/disconnected factors remain visible without forced links.
- Recommendations address specific mechanisms, with any missing ownership or
  measurement plan acknowledged.
- The review applies to the current evidence/map revision. A typed reviewer name
  records a declaration; it does not authenticate approval.

Return a bounded evidence-gap plan when the explanation cannot be supported.
An incomplete draft can still help the team decide what to investigate next.

## Produce the diagram and handoff

For the legacy healthcare profile, use
`assets/templates/mermaid/accimap-levels.mmd` and apply
`assets/template-use-contract.md`. Its pre-drawn example arrows are synthetic
prompts; remove or replace them with the relationships actually examined.
Keep the profile name and draft/review status in the accompanying caption.

For another profile, explicitly define and review the level structure. Do not
relabel existing factors automatically. Keep a readable legend and an evidence
table for nodes and connections; use line styles and words, not colour alone,
to distinguish supported links from hypotheses or contested explanations.

Pass the reviewed map, evidence references, alternatives, gaps, recommendations
and review record to the shared reporting and action/effectiveness workflows.
Route recommendations to the actual accountable owner. A level number alone
does not establish committee responsibility, delegation or a reporting duty.

The separate repository companion tool checks synthetic graph structure and
produces Mermaid from linked records. It is not included automatically in a
previously released skills-only package and does not validate causal truth or
authorise clinical use. The portable workflow remains usable without that tool.

## Select complementary methods

Select AcciMap when an unanswered question concerns interactions across system
levels. Severity alone does not establish that need. Apply the applicable
investigation policy and record the rationale for method selection; the
repository's SAC budgets and default combinations are project heuristics, not
properties of AcciMap itself. Resolve a conflict in scope explicitly.

Timeline and a contributing-factor framework can provide inputs. Yorkshire is
one option, not a prerequisite intrinsic to AcciMap. Use SEIPS for work-system
design questions; HFACS for a useful human-performance classification; and
STAMP/CAST or STPA for their respective retrospective or prospective
control/feedback questions. Justify overlap rather than applying every method.

Rasmussen and Svedung's broader proactive programme also discusses generic
AcciMaps, ActorMaps and InfoMaps. A single retrospective map does not demonstrate
that entire programme or predict the effect of a proposed intervention.

## Sources and adaptation

- Rasmussen, J., & Svedung, I. (2000). *Proactive Risk Management in a Dynamic
  Society*. Swedish Rescue Services Agency. [Publisher PDF](https://rib.msb.se/filer/pdf/16252.pdf),
  printed pp. 18–23: original hierarchy, actors, scenarios and work analysis.
- Branford, K., Naikar, N., & Hopkins, A. (2009). Guidelines for AcciMap analysis.
  In A. Hopkins (Ed.), *Learning from High Reliability Organisations*, pp. 193–212.
  [ANU publication record](https://researchportalplus.anu.edu.au/en/publications/guidelines-for-accimap-analysis/)
  verifies 2009; the previous guide's 2011 year was inaccurate for this chapter.
  ANU metadata orders the authors differently from the indexed chapter header.
  Full chapter download was unavailable during this revision.
- *Developing an AcciMap*, version 1.0, June 2025.
  [Healthcare facilitation guide](https://designpsychology.company/wp-content/uploads/2025/09/20250710-qrg-developing-an-accimap.pdf).
  This first-party adaptation uses five levels, including a separate patient
  context level, and describes group facilitation and subsequent validation.
  It is not a Queensland Health mandate or the source of rcagent's legacy six
  levels.

Sources checked 16 November 2026. These are links and original synthesis;
third-party texts and templates are not redistributed. Source attribution,
software tests and diagram review do not establish clinical effectiveness.
