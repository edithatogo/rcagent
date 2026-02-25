# Literature Review — AI-Assisted RCA Investigation Evaluation

**Version**: 1.0
**Date**: 2026-02-25

---

## 1. Investigation Methods

### 1.1 Core Methods

**RCA²** (Root Cause Analysis and Action)
Joint Commission. (2015). *Root Cause Analysis in Health Care: Tools and Techniques* (5th ed.). Joint Commission Resources.
- Enhanced RCA framework emphasizing action strength hierarchy (strong → intermediate → weak)
- Introduced requirement that every root cause must have at least one strong or intermediate action
- Standard of care for US healthcare; influential in AU/NZ practice via ACSQHC adoption

**5 Whys**
Ohno, T. (1988). *Toyota Production System: Beyond Large-Scale Production*. Productivity Press.
- Originally developed for manufacturing root cause drilling
- Adapted for healthcare by NHS Improvement (2018). *Root cause analysis: using five whys*
- Simple iterative technique: ask "why?" successively to drill from symptom to root cause
- Best suited for SAC 3–4 events with relatively linear causal chains

**Fishbone / Ishikawa Diagram**
Ishikawa, K. (1968). *Guide to Quality Control*. Asian Productivity Organization.
- Cause-and-effect diagram organizing contributing factors into categories
- Adapted for healthcare by the Institute for Healthcare Improvement (IHI)
- Standard categories adapted for healthcare: Staff, Environment, Equipment, Process/Task, Organisation, Patient factors
- Visual tool for brainstorming sessions with investigation teams

**Timeline Analysis**
Vincent, C. (2010). *Patient Safety* (2nd ed.). Wiley-Blackwell. Chapter 11.
- Chronological reconstruction of events from multiple evidence sources
- Foundation method — used in combination with virtually all other methods
- Identifies critical intervals, decision points, information gaps, and escalation delays
- Cross-references clinical record timeline with staff interview timelines

### 1.2 Systems Methods

**Yorkshire Contributory Factors Framework**
Lawton, R., McEachan, R. R. C., Giles, S. J., Sirriyeh, R., Watt, I. S., & Wright, J. (2012). Development of an evidence-based framework of factors contributing to patient safety incidents in hospital settings: a systematic review. *BMJ Quality & Safety*, 21(5), 369–380. https://doi.org/10.1136/bmjqs-2011-000443
- Evidence-based taxonomy of contributing factors derived from systematic review of 95 studies
- 5 domains: Active failures, Situational factors, Local working conditions, Latent/organisational factors, Latent/external factors
- 20 contributing factor categories with operational definitions
- Considered state-of-the-art for structured contributing factor identification in healthcare RCA
- Adopted by NHS England and influential in AU/NZ practice

**SEIPS 3.0** (Systems Engineering Initiative for Patient Safety)
Carayon, P., Wooldridge, A., Hoonakker, P., Hundt, A. S., & Kelly, M. M. (2020). SEIPS 3.0: Human-centered design of the patient journey for patient safety. *Applied Ergonomics*, 84, 103033. https://doi.org/10.1016/j.apergo.2019.103033
- Work system model: Person × Tasks × Tools/Technology × Organisation × Internal Environment × External Environment
- SEIPS 3.0 adds patient journey lens and collaborative cross-professional work
- Useful for understanding how work system design contributes to adverse events
- Complements Yorkshire Framework with explicit work system structure

Carayon, P., Schoofs Hundt, A., Karsh, B.-T., Gurses, A. P., Alvarado, C. J., Smith, M., & Flatley Brennan, P. (2006). Work system design for patient safety: the SEIPS model. *Quality and Safety in Health Care*, 15(Suppl 1), i50–i58.
- Original SEIPS model establishing the work system → process → outcome framework

**Swiss Cheese Model**
Reason, J. (1990). *Human Error*. Cambridge University Press.
Reason, J. (2000). Human error: models and management. *BMJ*, 320(7237), 768–770. https://doi.org/10.1136/bmj.320.7237.768
- Organisational accident model: hazards pass through successive defence layers (slices)
- Holes in defences (latent conditions + active failures) align to allow harm
- Foundation of modern patient safety theory
- Underpins the multi-barrier approach to healthcare safety design

**London Protocol**
Vincent, C., Taylor-Adams, S., & Stanhope, N. (1998). Framework for analysing risk and safety in clinical medicine. *BMJ*, 316(7138), 1154–1157.
Vincent, C., Taylor-Adams, S., Chapman, E. J., Hewett, D., Prior, S., Strange, P., & Tizzard, A. (2000). How to investigate and analyse clinical incidents: Clinical Risk Unit and Association of Litigation and Risk Management protocol. *BMJ*, 320(7237), 777–781.
Taylor-Adams, S., & Vincent, C. (2004). Systems analysis of clinical incidents: the London Protocol. *Clinical Risk*, 10(6), 211–220.
- Systematic protocol for clinical incident investigation
- Contributing factor taxonomy: Patient, Task/procedure, Individual staff, Team, Work environment, Organisation/management, Institutional context
- Widely adopted in UK NHS and internationally
- Step-by-step investigation guide suitable for non-specialist investigators

### 1.3 Structured Analysis Methods

**Bow-Tie Analysis**
de Ruijter, A., & Guldenmund, F. (2016). The bowtie method: A review. *Safety Science*, 88, 211–218. https://doi.org/10.1016/j.ssci.2016.03.001
- Visual risk model mapping: Threats → Prevention barriers → TOP EVENT → Mitigation barriers → Consequences
- Identifies both preventive and mitigative barriers and their failure modes
- Originally from oil/gas industry; adapted for healthcare
- Particularly useful for SAC 1 events with clear hazard-harm pathway

**Barrier Analysis**
Hollnagel, E. (2004). *Barriers and Accident Prevention*. Ashgate Publishing.
- Systematic identification of barriers (physical, functional, symbolic, incorporeal) that should have prevented harm
- Classifies barriers as: intact, failed, missing, or bypassed
- Complements Swiss Cheese by providing specific barrier failure taxonomy
- Useful when the question is "what defences failed and why?"

**FMEA** (Failure Mode and Effects Analysis)
DeRosier, J., Stalhandske, E., Bagian, J. P., & Nudell, T. (2002). Using health care Failure Mode and Effect Analysis: the VA National Center for Patient Safety's prospective risk analysis system. *Joint Commission Journal on Quality Improvement*, 28(5), 248–267.
- Proactive risk analysis — identifies potential failure modes BEFORE they cause harm
- Risk Priority Number (RPN) = Severity × Occurrence × Detection
- Developed for VA National Center for Patient Safety (HFMEA variant)
- Used for process redesign, not incident investigation per se

**HFACS** (Human Factors Analysis and Classification System)
Shappell, S. A., & Wiegmann, D. A. (2000). *The Human Factors Analysis and Classification System — HFACS*. DOT/FAA/AM-00/7. Federal Aviation Administration.
Wiegmann, D. A., & Shappell, S. A. (2003). *A Human Error Approach to Aviation Accident Analysis*. Ashgate.
- Four-level taxonomy: Unsafe acts → Preconditions → Unsafe supervision → Organisational influences
- Based on Reason's Swiss Cheese model but with specific classification categories
- Originally aviation; adapted for healthcare by several research groups
- Useful for classifying the TYPE of human factors contribution

ElBardissi, A. W., Wiegmann, D. A., Dearani, J. A., Daly, R. C., & Sundt, T. M. (2007). Application of the human factors analysis and classification system methodology to the cardiovascular surgery operating room. *Annals of Thoracic Surgery*, 83(4), 1412–1419.
- Healthcare adaptation of HFACS for surgical settings

### 1.4 Advanced Systems Methods

**AcciMap**
Rasmussen, J., & Svedung, I. (2000). *Proactive Risk Management in a Dynamic Society*. Swedish Rescue Services Agency (Räddningsverket).
Rasmussen, J. (1997). Risk management in a dynamic society: a modelling problem. *Safety Science*, 27(2–3), 183–213.
- Multi-level systemic accident mapping across 6 levels: Government/regulatory → Regulatory bodies → Company management → Technical management → Physical processes → Equipment/environment
- Maps causal relationships across organisational levels
- Reveals how high-level decisions create conditions for frontline failures
- Useful for SAC 1 events with clear organisational/systemic contributions

Branford, K. (2011). Seeing the big picture of mishaps: applying the AcciMap approach to analyze system accidents. *Aviation Psychology and Applied Human Factors*, 1(1), 31–37.
- Practical application guide for AcciMap methodology

**STAMP/STPA** (Systems-Theoretic Accident Model and Processes / System-Theoretic Process Analysis)
Leveson, N. G. (2004). A new accident model for engineering safer systems. *Safety Science*, 42(4), 237–270. https://doi.org/10.1016/j.ssci.2003.09.002
Leveson, N. G. (2012). *Engineering a Safer World: Systems Thinking Applied to Safety*. MIT Press.
- Treats safety as a control problem: accidents result from inadequate enforcement of safety constraints
- STPA: Systematic analysis of control structure, control actions, and unsafe control actions
- Most theoretically rigorous method; identifies control flaws at all system levels
- Computationally intensive; best suited for complex SAC 1 events with system design questions

### 1.5 Safety Paradigms

**Safety-II**
Hollnagel, E., Wears, R. L., & Braithwaite, J. (2015). *From Safety-I to Safety-II: A White Paper*. EUROCONTROL.
Hollnagel, E. (2014). *Safety-I and Safety-II: The Past and Future of Safety Management*. Ashgate.
- Safety-I: Focus on what goes wrong (traditional)
- Safety-II: Focus on what usually goes right and why (resilience)
- Work-as-Done (WAD) vs Work-as-Imagined (WAI): actual practice vs prescribed procedure
- Complementary to investigation — asks "why does this usually work?" not just "why did it fail?"

Braithwaite, J., Wears, R. L., & Hollnagel, E. (2015). Resilient health care: turning patient safety on its head. *International Journal for Quality in Health Care*, 27(5), 418–420.

**Just Culture**
Marx, D. (2001). *Patient Safety and the "Just Culture": A Primer for Health Care Executives*. Columbia University.
Dekker, S. (2007). *Just Culture: Balancing Safety and Accountability*. Ashgate.
Reason, J. (1997). *Managing the Risks of Organizational Accidents*. Ashgate. Chapter 9.
- Framework for fair accountability: human error → console; at-risk behaviour → coach; reckless behaviour → discipline
- Substitution test: "Would a similarly trained person, in similar circumstances, have made the same error?"
- Essential for maintaining reporting culture while ensuring accountability
- Integrated into ACSQHC RCA guidelines and rcagent skill suite

---

## 2. RCA Quality and Limitations

Peerally, M. F., Carr, S., Waring, J., & Dixon-Woods, M. (2017). The sustainability of healthcare improvements: what are we not yet getting right? *BMJ Quality & Safety*, 26(2), 141–144.

Nicolini, D., Waring, J., & Mengis, J. (2011). Policy and practice in the use of root cause analysis to investigate clinical adverse events: Mind the gap. *Social Science & Medicine*, 73(2), 217–225. https://doi.org/10.1016/j.socscimed.2011.05.010
- Critical analysis showing gap between RCA policy intent and practice reality
- Investigations often stop at individual error, produce weak recommendations
- Organisational and cultural factors often missed

Wu, A. W., Lipshutz, A. K. M., & Pronovost, P. J. (2008). Effectiveness and efficiency of root cause analysis in medicine. *JAMA*, 299(6), 685–687. https://doi.org/10.1001/jama.299.6.685
- Questions whether RCA consistently produces effective safety improvements
- Calls for better evidence on RCA effectiveness

Kellogg, K. M., Hettinger, Z., Shah, M., Wears, R. L., Sellers, C. R., Squires, M., & Fairbanks, R. J. (2017). Our current approach to root cause analysis: is it contributing to our failure to improve patient safety? *BMJ Quality & Safety*, 26(5), 381–387.
- Systematic critique of current RCA practice
- Identifies common failure patterns: hindsight bias, linear thinking, stopping at human error

Hibbert, P. D., Thomas, M. J. W., Deakin, A., Runciman, W. B., Carson-Stevens, A., Braithwaite, J., ... & Donaldson, L. (2018). Are root cause analyses recommendations effective and sustainable? An observational study. *International Journal for Quality in Health Care*, 30(2), 124–131.
- Found only 55% of RCA recommendations were fully implemented at 12 months
- Weak actions (training) had higher implementation but lower effectiveness

---

## 3. AI in Clinical Domains

Singhal, K., Azizi, S., Tu, T., Mahdavi, S. S., Wei, J., Chung, H. W., ... & Natarajan, V. (2023). Large language models encode clinical knowledge. *Nature*, 620(7972), 172–180. https://doi.org/10.1038/s41586-023-06291-2
- Med-PaLM 2 achieves expert-level performance on medical question answering
- Demonstrates clinical knowledge encoding in LLMs

Nori, H., King, N., McKinney, S. M., Carignan, D., & Horvitz, E. (2023). Capabilities of GPT-4 on medical competency examinations. *arXiv preprint* arXiv:2303.13375.
- GPT-4 passes US medical licensing examination with high margins
- Demonstrates structured clinical reasoning capability

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., ... & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. *Advances in Neural Information Processing Systems*, 35, 24824–24837.
- Chain-of-thought prompting improves structured reasoning
- Relevant to investigation methodology: step-by-step causal analysis

Thirunavukarasu, A. J., Ting, D. S. J., Elangovan, K., Gutierrez, L., Tan, T. F., & Ting, D. S. W. (2023). Large language models in medicine. *Nature Medicine*, 29(8), 1930–1940.
- Comprehensive review of LLM applications in medicine
- Discusses opportunities and limitations for clinical decision support

---

## 4. Evaluation Methodology

Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1), 37–46.
- Cohen's kappa: inter-rater reliability coefficient for categorical ratings
- Used in this study for human–AI rater agreement assessment

Krippendorff, K. (2004). *Content Analysis: An Introduction to Its Methodology* (2nd ed.). Sage Publications.
- Gold standard text for content analysis methodology
- Informs our approach to normalizing and evaluating investigation outputs

Likert, R. (1932). A technique for the measurement of attitudes. *Archives of Psychology*, 22(140), 1–55.
- Foundation for the 1–5 Likert scale used in the evaluation rubric

Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.
- Effect size conventions: small (d=0.2), medium (d=0.5), large (d=0.8)
- Used in this study as descriptive measures only (insufficient N for inferential testing)

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics*, 33(1), 159–174.
- Kappa interpretation: <0 poor, 0–0.20 slight, 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, 0.81–1.00 almost perfect
- Threshold for this study: kappa ≥ 0.60 (moderate agreement)

---

## 5. Regulatory Framework (AU/NZ)

Australian Commission on Safety and Quality in Health Care (ACSQHC). (2021). *National Safety and Quality Health Service (NSQHS) Standards* (2nd ed.).
- Standard 1: Clinical Governance — requires incident investigation systems
- Standard 8: Recognising and Responding to Acute Deterioration
- Mandates RCA for SAC 1 events

ACSQHC. (2014). *National Open Disclosure Framework*.
- Requirements for open disclosure following adverse events
- Integrates with RCA investigation process

Health Quality & Safety Commission New Zealand (HQSC). (2017). *Learning from adverse events*.
- NZ national guidance on adverse event investigation
- Aligns with but adapts from ACSQHC framework

Health and Disability Commissioner (HDC) New Zealand. Published decisions.
- Independent investigation reports publicly available
- Contains detailed contributing factor analysis — serves as gold standard for this evaluation

---

## 6. Agent Harness and AI Tool Literature

Anthropic. (2025). Claude Code documentation. https://docs.anthropic.com
- Claude Code agent harness capabilities, skill loading, tool use
- Relevant to understanding how Condition A (skill-native) operates

Google. (2025). Gemini CLI documentation.
- Gemini CLI agent harness, system prompt injection
- Relevant to Condition B (prompt-injected) implementation for H3

OpenAI. (2025). Codex CLI documentation.
- Codex CLI agent harness, instruction injection
- Relevant to Condition B implementation for H4

Shinn, N., Cassano, F., Gopinath, A., Shakkottai, K., Labash, A., & Karpas, E. (2023). Reflexion: Language agents with verbal reinforcement learning. *Advances in Neural Information Processing Systems*, 36.
- Framework for language agent self-reflection and improvement
- Relevant to understanding agent harness contribution to output quality

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. *International Conference on Learning Representations*.
- ReAct framework combining reasoning and action in language agents
- Foundation for understanding agentic harness architectures
