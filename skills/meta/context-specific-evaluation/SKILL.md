---
name: context-specific-evaluation
description: Evaluate a concrete target against its goals, domain context, source materials, constraints, examples, and prior feedback. Use for reviews, audits, comparisons, critiques, selections, quality gates, and assessments that require independent supporting and adversarial perspectives, traceable findings, prioritized actionable improvements, and learning across repeated runs.
---

# Context-Specific Evaluation

## Mission

Evaluate the supplied target. Do not design or generate an evaluation skill.

Produce a defensible assessment that preserves the target's context, distinguishes evidence from inference, challenges its assumptions, recognizes what already works, and offers actionable alternatives.

## Non-goals

Do not:

- create another skill, rubric system, or generic review framework unless explicitly requested;
- replace target-specific reasoning with a fixed checklist;
- judge only the final conclusion while ignoring the reasoning path and intermediate artifacts;
- invent missing facts or silently treat assumptions as confirmed;
- collapse independent reviewer perspectives before they have been developed;
- recommend changes without explaining the problem, evidence, impact, and trade-off;
- optimize for the number of findings rather than decision value.

## Inputs

Use all available inputs, while recording missing information:

- evaluation target;
- intended goal and decisions the target must support;
- stakeholders and users;
- source materials and authoritative constraints;
- examples, counterexamples, and expected behavior;
- prior review feedback and change history;
- evaluation mode, such as review, comparison, selection, audit, or quality gate;
- time, cost, risk, compatibility, and implementation constraints.

When goals or decision criteria are absent, infer only a provisional evaluation frame and label it as a hypothesis. Ask only questions whose answers could materially change the verdict or recommended action.

## Core principles

### Context before criteria

Derive evaluation criteria from the target, purpose, domain, constraints, and evidence before applying reusable review lenses.

### Independent perspectives before synthesis

Generate supporting, adversarial, and coverage-oriented analyses independently. Prevent one perspective from anchoring the others.

### Evidence discipline

Classify claims as:

- `FACT`: directly supported by supplied evidence;
- `INTERPRETATION`: a reasoned reading of facts;
- `HYPOTHESIS`: plausible but unverified;
- `UNKNOWN`: required information is absent;
- `CONFLICT`: sources or observations disagree.

### Process is evidence

Evaluate intermediate decisions, discarded alternatives, assumptions, and evolution—not only the final artifact.

### Actionability over commentary

Every material criticism must lead to one or more of:

- a concrete correction;
- a viable alternative;
- a verification step;
- an explicit risk acceptance decision.

### Fast feedback loops

Create an early evaluation snapshot, expose the highest-impact uncertainty, obtain or infer focused feedback, and update only the affected findings and verdict.

## Evaluation workflow

### 1. Frame the evaluation

Create an evaluation brief containing:

- target and version;
- purpose;
- decision to support;
- stakeholders;
- in-scope and out-of-scope concerns;
- constraints;
- success conditions;
- evidence inventory;
- unresolved questions;
- selected evaluation lenses.

Read `references/framing.md` when goals, scope, evidence quality, or evaluation mode are unclear.

### 2. Build the evaluation IR

Transform the raw inputs into a compact, target-specific intermediate representation:

- target claims and intended outcomes;
- important domain concepts and boundaries;
- explicit requirements and constraints;
- assumptions and dependencies;
- decision history and rationale;
- examples and counterexamples;
- known risks and prior findings;
- evidence pointers;
- unresolved contradictions.

This IR is not a summary. It is the executable review contract used by all reviewers.

Use `templates/evaluation-ir.md`.

### 3. Select lenses

Choose only lenses that can change the decision. Candidate lenses include:

- goal alignment;
- domain correctness;
- completeness and coverage;
- internal consistency;
- boundary and responsibility quality;
- feasibility and operability;
- failure modes and abuse cases;
- security, privacy, compliance, and safety;
- performance and scalability;
- maintainability and evolvability;
- user and stakeholder impact;
- cost and reversibility;
- traceability and testability;
- quality of the reasoning process.

Record why each lens was selected or skipped. Read `references/lens-library.md` for details.

### 4. Generate independent analyses

Produce these perspectives independently where task complexity warrants it:

1. **Supporting analysis**
   - identify what is valid, strong, coherent, and worth preserving;
   - state the conditions under which the target succeeds;
   - prevent adversarial review from destroying useful structure.

2. **Adversarial analysis**
   - search for incorrect assumptions, contradictions, omissions, hidden coupling, failure modes, and costly edge cases;
   - attempt to falsify central claims;
   - distinguish fatal issues from local defects.

3. **Coverage analysis**
   - derive concerns independently from the source materials and purpose;
   - detect shared blind spots not surfaced by either supporting or adversarial analysis.

4. **Alternative analysis**
   - construct at least one materially different approach for high-impact disputed decisions;
   - compare trade-offs rather than merely naming an alternative.

For larger evaluations, delegate these roles to isolated subagents using `references/orchestration.md` and the definitions in `agents/`.

### 5. Create findings

Each finding must contain:

- stable finding ID;
- title;
- status classification (`FACT`, `INTERPRETATION`, `HYPOTHESIS`, `UNKNOWN`, or `CONFLICT`);
- evidence pointers;
- affected goal, requirement, or decision;
- problem or strength;
- causal explanation;
- impact;
- severity and confidence;
- affected scope;
- recommended action;
- alternative when relevant;
- verification or acceptance condition.

Do not present unsupported criticism as fact. Use `templates/finding.md`.

### 6. Prioritize

Prioritize using decision impact, not rhetorical intensity.

Default ordering:

1. invalidates the core goal or decision;
2. creates unacceptable safety, compliance, data, or operational risk;
3. blocks implementation or verification;
4. causes expensive future rework or irreversible coupling;
5. materially reduces usability, maintainability, or performance;
6. local quality improvement;
7. stylistic preference.

Use severity and confidence separately. A high-severity hypothesis may require investigation rather than immediate redesign.

Read `references/scoring-and-gates.md`.

### 7. Synthesize without flattening disagreement

Produce:

- strengths to preserve;
- critical findings;
- significant findings;
- lower-priority improvements;
- unresolved unknowns and conflicts;
- alternative options and trade-offs;
- verdict;
- next feedback-loop action.

When reviewers disagree, show the disagreement, evidence, and decision consequence. Do not force artificial consensus.

### 8. Apply the quality gate

Choose a verdict appropriate to the evaluation mode:

- `PASS`;
- `PASS_WITH_CONDITIONS`;
- `REVISE`;
- `BLOCK`;
- `INSUFFICIENT_EVIDENCE`;
- `PREFER_OPTION_A/B/...` for comparison or selection.

State the exact conditions for changing the verdict.

### 9. Run the feedback loop

After receiving changes or feedback:

- map feedback to finding IDs and evaluation assumptions;
- identify which IR elements changed;
- re-evaluate only affected lenses first;
- detect regressions and newly exposed risks;
- preserve superseded findings with status and rationale;
- update the verdict and change summary;
- record what evaluation method proved useful or misleading.

Read `references/feedback-loop.md`.

## Output contract

Unless the user requests another format, output:

1. **Verdict** — one sentence with confidence and decisive reason.
2. **Evaluation frame** — purpose, scope, constraints, and evidence gaps.
3. **Strengths to preserve** — only decision-relevant strengths.
4. **Prioritized findings** — traceable, actionable, and evidence-classified.
5. **Alternatives** — for high-impact design or decision findings.
6. **Unknowns and conflicts** — including the question or experiment needed.
7. **Next iteration** — smallest high-information action.
8. **Change from prior run** — when previous feedback or versions exist.

Use `templates/evaluation-report.md` for durable artifacts.

## Completion criteria

The evaluation is complete when:

- the verdict is linked to the stated purpose and criteria;
- each material finding is traceable to evidence or explicitly marked uncertain;
- both strengths and vulnerabilities have been independently considered;
- critical coverage gaps have been checked;
- high-impact criticisms include actionable remedies or decision alternatives;
- unresolved unknowns are visible and tied to next actions;
- the output is concise enough to support the intended decision;
- repeated-run changes are traceable.

## Reference loading guide

Load only what is needed:

- `references/framing.md` — purpose, scope, criteria, and evidence quality;
- `references/evaluation-ir.md` — target-specific review intermediate representation;
- `references/lens-library.md` — reusable but selectable review lenses;
- `references/orchestration.md` — isolated multi-perspective review execution;
- `references/scoring-and-gates.md` — severity, confidence, prioritization, and verdicts;
- `references/feedback-loop.md` — repeated reviews and incremental updates;
- `references/pattern-learning.md` — learning from runs without turning this into a skill generator;
- `references/artifact-schema.md` — durable workspace structure.
