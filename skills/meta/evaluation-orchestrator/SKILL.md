---
name: evaluation-orchestrator
description: Orchestrate traceable, adversarial, context-specific evaluations from source materials, goals, examples, and prior feedback. Use for reviews, audits, comparisons, selections, critiques, quality gates, or assessments that must preserve domain context, generate independent perspectives, integrate and reclassify findings, produce actionable alternatives, and improve from repeated runs.
---

# Evaluation Orchestrator

Run a disciplined evaluation system, not merely a judging prompt. The system must reconstruct what matters in the target, convert it into traceable evaluation IR, generate independent supporting and opposing perspectives, define observable evidence, execute the evaluation, and improve without overfitting to one case.

## Core principle

Do not generalize by deleting target context. Generalize the mechanism while preserving target-specific meaning in a separate IR.

```text
source reality
  -> evaluation framing
  -> evidence-grounded evaluation IR
  -> independent perspectives
  -> evaluation plan and tests
  -> evaluation run plan and instructions
  -> evaluation run
  -> observations and dissent
  -> localized repair
  -> versioned improvement
```

The durable assets are, in priority order:

1. evaluation cases and expected traces;
2. evaluation IR and provenance;
3. decision boundaries and failure catalog;
4. transformation records from weak to strong evaluations;
5. runtime prompts and agent topology.

## Required outputs

Produce these artifacts unless the user explicitly narrows the request:

- `evaluation-charter.yaml`
- `evaluation-ir.yaml`
- `context-topology.yaml`
- `orchestration.yaml`
- normalized `finding` artifacts and integrated finding set
- `evaluation-cases/` and separately protected holdout expectations
- `evaluation-run-plan.yaml` and evaluator instructions
- `run-trace.yaml`
- `failure-localization.yaml` when repair is required
- `improvement-candidates.yaml` and regression evidence when the outer loop runs

Use the templates in `templates/`.

## Phase 1: Frame the evaluation

Define:

- target being evaluated;
- decision or action the evaluation must support;
- unit of evaluation;
- stakeholders and consequences;
- acceptable false-positive and false-negative costs;
- authority of the evaluator;
- evidence available and unavailable;
- time, cost, safety, and reversibility constraints;
- output consumers and required actionability.

Do not begin by listing generic criteria. First identify what failure would matter in reality.

## Phase 2: Reconstruct the target

Read the target and associated materials. Extract:

- explicit claims and commitments;
- rationale and rejected alternatives;
- invariants and operating rules;
- intended users and workflows;
- boundaries and interfaces;
- examples, counterexamples, and exceptions;
- implementation or execution dependencies;
- migration, rollback, and maintenance assumptions;
- unresolved questions.

Classify every extracted item as one of:

- `observation`
- `interpretation`
- `assumption`
- `hypothesis`
- `decision`
- `constraint`
- `unknown`

Never allow an upstream agent's interpretation to become an unmarked fact. Preserve source references for every material item.

## Phase 3: Build evaluation IR

Normalize the extracted context using `references/evaluation-ir.md`.

At minimum include:

- target map and source items;
- decision-centered records that keep observed design, rationale, invariants, attack, defense, verification, and structural alternatives together;
- evaluation dimensions;
- decision boundaries;
- failure modes;
- required evidence;
- ambiguity ledger;
- rejected alternatives;
- operational enforceability;
- candidate counterexamples;
- case-generation axes;
- actionability requirements.

Do not store a conclusion-loaded label such as “X breaks” where the IR can preserve an observation, attack hypothesis, defense hypothesis, and distinguishing test separately. Use `templates/evaluation-ir.yaml` as the canonical schema.

For each criterion define:

- why it matters;
- observable evidence;
- pass, concern, and fail anchors;
- severity or consequence;
- known blind spots;
- what recommendation becomes possible when it fails.

## Phase 4: Orchestrate independent evaluation paths

Use the canonical execution graph in `references/orchestration.md` and instantiate `templates/orchestration.yaml`. The default graph is mandatory unless evaluation evidence justifies a simpler topology:

```text
Source Normalizer
  -> [Adversarial Extractor || Advocate Extractor || Blind Coverage Explorer]
  -> Finding Integrator
  -> Epistemic Reclassifier
  -> Evaluation Case Designer
  -> Evaluation Run Planner
  -> Final Evaluator
  -> Blinded Evaluation Judge
  -> [conditional: Failure Localizer -> Improvement Candidate Generator -> Regression Replay -> Promotion Judge]
```

The three extraction paths must run from immutable input snapshots without cross-agent visibility. The blind path must not see seeded concerns, upstream interpretations, or other findings. Adversarial and advocate paths must read primary sources directly and use `source_ir_v0` only as an index; both must report source discoveries omitted from the IR or explicitly report that none were found.

Choose roles based on failure risks, not theatrical variety.

Recommended roles:

- **Reconstructor**: produces source-grounded IR.
- **Advocate**: builds the strongest case that the target is sound under explicit conditions.
- **Adversary**: seeks counterexamples, hidden assumptions, exploit paths, and irreversible failures.
- **Independent evaluator**: reads the source without the first reconstructor's framing.
- **Alternative designer**: proposes structurally different options, not cosmetic patches.
- **Implementation witness**: asks whether a practitioner can act without inventing missing rules.
- **Judge / synthesizer**: reconciles evidence while preserving unresolved dissent.

Define information topology explicitly:

- what each role sees;
- what is hidden;
- when other outputs are revealed;
- what each role may modify;
- which failure the separation is intended to catch.

Use `templates/context-topology.yaml`. Agent independence comes from information asymmetry, not role names.

### Integrate, deduplicate, and reclassify

After the parallel paths complete:

1. normalize every result with `templates/finding.yaml`;
2. cluster findings only when claim, mechanism, consequence, and evidence basis are materially equivalent;
3. preserve conflicting conclusions as linked dissent rather than averaging them away;
4. mark findings discovered only by the blind path;
5. retain source references and origin-agent IDs;
6. reclassify every merged statement epistemically;
7. prohibit agent consensus from promoting a hypothesis into an observation;
8. produce evaluation IR v1 and an epistemic change log.

Do not proceed to evaluator generation until integration and reclassification assertions pass.

### Execution and failure routing

Each stage must declare required inputs, produced artifacts, success assertions, retry limit, failure route, and escalation condition. A downstream stage starts only after its dependencies pass structural validation. On failure, route to the earliest responsible stage rather than retrying the immediately preceding stage.

Run `scripts/validate_orchestration.py templates/orchestration.yaml` before execution. Run `scripts/lint_evaluation.py .` before packaging or publishing the Skill.

For stateful execution, use `scripts/orchestrate.py`. It generates stage packets containing only allowed inputs, enforces dependency and artifact gates, applies retry budgets, and routes failures to the earliest responsible stage. It is vendor-neutral: the surrounding agent runtime executes each packet and writes the declared outputs.

## Phase 5: Construct the evaluation attack plan

Translate the IR into executable evaluation operations. Prefer composable primitives:

- extract and cite claims;
- recover rationale;
- identify assumptions;
- derive decision boundaries;
- steelman the current option;
- steelman rejected alternatives;
- generate counterexamples;
- test boundary and transition cases;
- compare structurally different alternatives;
- test implementation ambiguity;
- test enforceability;
- test migration and rollback;
- classify evidence confidence;
- synthesize with dissent;
- convert criticism into actionable changes.

Use `references/evaluation-primitives.md`.

Every material criticism must include at least one of:

- a concrete failing input or scenario;
- a falsifying observation;
- an executable alternative;
- a distinguishing test;
- a repair owner and verification method.

Do not permit criticism that cannot change a decision or action.

## Phase 6: Design evaluation cases before the final prompt

Create cases covering:

- normal success;
- boundary conditions;
- ambiguous classification;
- contradictory evidence;
- incomplete evidence;
- misleading or adversarial input;
- rejected alternative that is actually superior under some conditions;
- target that should pass unchanged;
- irreversible or high-loss failure;
- prior failure or regression;
- holdout cases hidden from evaluation-planning and execution roles.

Before generating cases, derive applicable variation axes from the target:

- state and classification;
- transitions, ordering, insertion, split, merge, and deletion;
- ownership and authority;
- lifecycle and migration;
- content or representation differences;
- region, platform, environment, or distribution;
- detection, rollback, and recovery.

Use risk-based or pairwise combinations unless a full cross-product is small and justified. For each case record both:

- expected result;
- expected trace: discoveries, questions, prohibited shortcuts, escalation decisions.

Store holdout expectations separately from the planner and evaluator. Use `templates/evaluation-case.yaml`.

## Phase 7: Plan the evaluation run

Transform the integrated evaluation IR into run-specific evaluator instructions and an execution plan. This Skill orchestrates evaluation; it does not create or package other Skills.

The evaluator must contain:

1. role and non-goals;
2. target context and special properties;
3. evidence policy and epistemic labels;
4. required evaluation dimensions;
5. explicit evaluation procedure;
6. mandatory target-specific questions;
7. alternative and counterexample requirements;
8. severity / scoring anchors;
9. output format tied to actions;
10. completion checklist.

Target-specific questions must be generated from the IR, not copied from a fixed universal checklist.

Output constraints should force evidence, comparison, and actionability, but should not create box-filling. Require depth based on risk and novelty rather than arbitrary counts alone.

## Phase 8: Execute and judge the evaluation

Execute the planned evaluation against the target and prepared cases. Measure:

- coverage of important claims;
- provenance accuracy;
- unsupported-assumption rate;
- counterexample quality;
- strength of steelman;
- alternative structural diversity;
- implementation actionability;
- severity calibration;
- false-positive and false-negative behavior;
- independent discovery beyond seeded questions;
- unnecessary verbosity and loop cost;
- human intervention required.

Do not allow the executing evaluator to be its only judge. Use deterministic checks, a blinded judge, or human review for high-impact cases. The judge receives holdout expectations and charter thresholds but not evaluator self-grades or the current improvement proposal.

## Phase 9: Localize failures

When output is weak, locate the earliest responsible stage:

- framing failure;
- source reconstruction failure;
- provenance loss;
- IR compression loss;
- perspective anchoring;
- weak attack plan;
- poor evaluation cases;
- output-format distortion;
- execution failure;
- scoring or judging failure.

Repair the earliest responsible stage. Do not append instructions to the final prompt when the cause is upstream.

## Phase 10: Improve safely

Maintain two loops:

### Fast inner loop

Repair the current run using the smallest responsible component. Preserve the orchestration contract unchanged unless a separate improvement proposal is created.

### Slow outer loop

Across completed runs:

1. collect run traces and correction deltas;
2. identify repeated failure patterns;
3. propose a versioned change;
4. replay golden, boundary, prior-failure, and holdout cases;
5. compare quality, cost, context growth, and intervention;
6. promote, retain experimentally, or reject;
7. preserve rollback information.

Use `templates/run-trace.yaml`, `templates/transformation-record.yaml`, and `templates/improvement-candidate.yaml`. The canonical graph implements this as conditional `failure_localizer`, `improvement_candidate_generator`, `regression_replay`, and `improvement_promotion_judge` stages.

Promotion ladder:

`provisional note -> experimental patch -> target-specific rule -> cross-target pattern -> core invariant`

Never promote a one-off tactic directly into a universal criterion.

## Phase 11: Refactor for leverage

Periodically ask:

- Can a repeated criterion become an evaluation primitive?
- Can a subjective rule become a deterministic validator?
- Can two roles be merged without losing independent discovery?
- Is any role duplicating the same context and reasoning?
- Can evaluation happen earlier in the workflow?
- Are seeded examples anchoring discovery?
- Can a failure pattern become a lint rule?
- Is the evaluation corpus more valuable than the prompt and being maintained accordingly?

Use `references/evaluation-smells.md` and run `scripts/lint_evaluation.py`.

## Completion gate

Do not declare the evaluation run complete unless:

- target-specific context is represented in traceable IR;
- facts and interpretations remain distinguishable;
- seeded concerns and independent discovery both exist;
- advocacy and adversity are both represented;
- important criticism produces an actionable alternative or test;
- implementation / execution ambiguity is tested;
- evaluation cases include expected traces and holdouts;
- severity and scoring have observable anchors;
- failure routing and retry limits are defined;
- the canonical orchestration graph or an evidence-backed simplification is explicit;
- the blind path is isolated from seeded concerns and upstream interpretations;
- integration preserves dissent, provenance, and blind-only discoveries;
- post-integration epistemic reclassification is complete;
- the final evaluation is judged independently;
- any failure is localized to the earliest responsible stage;
- any promoted improvement has golden, boundary, prior-failure, and holdout replay evidence;
- self-improvement is evidence-based and reversible;
- package references, templates, contracts, and orchestration structure pass lint and validation.
