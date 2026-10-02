# Evaluation IR

The Evaluation IR preserves target-specific meaning while allowing the evaluation mechanism to remain reusable. Its primary unit is a **decision record**, not a detached checklist item or free-floating finding.

## Why decision-centered records

A useful evaluation must keep these together:

- what the target explicitly does;
- why that choice was made;
- which invariants make it viable;
- the strongest falsifiable attack;
- the strongest defense and its required conditions;
- evidence or tests that distinguish the competing claims;
- structural alternatives and their costs.

Splitting these across unrelated findings makes later agents reconstruct relationships from prose and encourages interpretation laundering. Use `templates/evaluation-ir.yaml` as the canonical schema.

## Required sections

### Target

- identity, version, source list, scope, exclusions;
- decision supported by the evaluation;
- stakeholders, consequences, reversibility.

### Source items

Each item contains:

- stable ID;
- epistemic class;
- normalized statement;
- source location or direct support;
- confidence;
- dependencies and contradiction links.

### Decision records

Each material decision contains:

- `observed_design`: source-grounded statement of the current choice;
- `rationale`: stated or reconstructed reason, separately classified;
- `rejected_alternatives`: option and rejection evidence;
- `invariants`: owner, enforcement, detection, repair, and consequence;
- `attack`: hypotheses, counterexamples, and failure mechanisms;
- `defense`: strongest case, required conditions, supporting evidence, and collapse conditions;
- `verification`: questions, missing evidence, and distinguishing tests;
- `candidate_alternatives`: structurally different choices and migration costs;
- `current_assessment`: status, severity, confidence, dissent, and linked findings.

Do not compress an attack label into a presumed verdict. Keep observation, attack hypothesis, defense hypothesis, and verification separate.

### Evaluation dimensions

- dimension ID and name;
- purpose and linked decisions;
- evidence required;
- pass / concern / fail anchors;
- severity mapping;
- blind spots;
- actions enabled by a failure.

### Invariants and enforceability

For each invariant record:

- statement;
- owner;
- enforcement layer;
- prevention and detection method;
- repair method;
- violation consequence.

Enforcement layers:

- model/schema;
- deterministic validation;
- write path or workflow;
- CI/lint/audit;
- human review;
- not realistically enforceable.

### Decision boundaries

- selected option;
- supporting conditions;
- evidence against;
- would-flip-if conditions;
- distinguishing tests;
- confidence and authority.

### Failure modes

- triggering input, transition, or state;
- mechanism of failure;
- observable symptom;
- consequence;
- detectability;
- reversibility and repairability;
- candidate alternative.

### Ambiguity ledger

- unresolved question;
- plausible interpretations;
- downstream decisions affected;
- recommended default;
- escalation owner.

### Case-generation axes

Generate cases from the target state space rather than copying one memorable example. Derive applicable axes such as:

- state variants;
- transitions and ordering changes;
- ownership and authority;
- lifecycle phases;
- content or representation differences;
- distribution, region, platform, or environment;
- failure detection and recovery.

Use risk-based or pairwise combinations unless the state space is small enough for a full cross-product.

### Counterexample status

Label every counterexample as:

- verified real case;
- needs fact verification;
- synthetic thought experiment.

### Evaluation cases

Reference normal, boundary, ambiguous, adversarial, prior-failure, regression, and holdout cases. Store both expected result and expected trace.
