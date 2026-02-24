# STAMP/STPA — Systems-Theoretic Accident Model and Processes

STAMP (Leveson, 2004) is a causality model based on systems theory and control theory. STPA (System-Theoretic Process Analysis) is the analysis technique derived from STAMP.

STAMP views accidents not as chains of events but as failures of control — where a controller (person, system, or organisation) fails to enforce constraints needed to prevent harm.

## Core Concepts

**Safety Constraints**: Conditions that must hold for the system to remain safe
Example: "Blood type must be verified before transfusion"

**Control Structure**: The hierarchy of controllers and controlled processes
- Controllers: Staff, systems, protocols, management
- Control actions: Orders, decisions, automated commands, policies
- Feedback: Vital signs, alerts, audit results, incident reports
- Controlled processes: Clinical care delivery

**Unsafe Control Actions (UCAs)**: When a controller provides the wrong action:
- Action not provided when needed
- Unsafe action provided
- Action provided too early, too late, or for too long
- Action stopped too soon

## STAMP Accident Causation

An accident occurs when:
1. Safety constraints are violated
2. Control actions fail to maintain those constraints
3. Inadequate feedback prevents controllers from knowing the system is out of safe state

## STPA Process

### Step 1: Define the accident and hazards
- Accident: Patient harmed (final outcome to prevent)
- Hazard: System state that leads to accident under certain conditions
Example hazard: "Patient receives incorrect blood product"

### Step 2: Map the control structure
Draw the hierarchy of controllers relevant to this process:
- Hospital policy/management → Department protocols → Clinical supervisor → Bedside nurse → Patient

### Step 3: Identify unsafe control actions
For each control link, identify UCAs across all four types (not provided, unsafe when provided, timing, duration)

### Step 4: Identify loss scenarios
For each UCA, identify the causal scenarios that could produce it:
- Controller had inadequate process model (wrong belief about system state)
- Controller received inadequate feedback
- Control algorithm was flawed (wrong protocol)
- Physical control failure (equipment malfunction)

### Step 5: Generate safety constraints and requirements
For each UCA, define the control constraint that would prevent it.
These become the system requirements for safe design.

## When to Use STAMP/STPA

STAMP/STPA is most powerful for:
- Complex sociotechnical systems with multiple interacting controllers
- Technology-heavy processes (EMR, automated systems, robotics)
- Proactive analysis of new systems or pathways before implementation
- Events where multiple controllers contributed and the interaction pattern is the problem
- Healthcare system redesign and safety architecture

## Mermaid Diagram

Use template `assets/templates/mermaid/stamp-control-structure.mmd`

## Note on Complexity

STAMP/STPA is the most technically sophisticated method in this suite. Use it for SAC 1 events with complex technology or system interactions, or for major system redesign projects. For most clinical adverse events, Yorkshire Framework + London Protocol + Swiss Cheese will be sufficient and more accessible for clinical teams.
