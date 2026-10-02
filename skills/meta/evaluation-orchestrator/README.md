# Evaluation Orchestrator

An orchestration Skill for running rigorous, context-specific evaluations. It evaluates targets; it does not create or package other Skills.

It converts source material, goals, rejected alternatives, operating rules, and prior feedback into:

- traceable, decision-centered evaluation IR;
- independent adversary, advocate, and blind-coverage paths;
- explicit integration, semantic deduplication, dissent preservation, and epistemic reclassification;
- target-derived case axes, visible cases, and protected holdouts;
- run-specific evaluator instructions and execution plans;
- independent judging, earliest-stage failure localization, and reversible improvement records;
- a vendor-neutral execution harness with dependency, visibility, artifact, retry, and routing gates.

## Core distinction

The reusable mechanism is generic. The target's meaning is not discarded; it is stored in the evaluation IR with provenance. The primary IR unit binds a decision to its rationale, invariants, attack, defense, verification, and structural alternatives.

## Validate the package

```bash
python scripts/validate_orchestration.py templates/orchestration.yaml
python scripts/lint_evaluation.py .
```

## Quick start

1. Copy and fill `templates/evaluation-charter.yaml`.
2. Reconstruct the target into `templates/evaluation-ir.yaml`.
3. Define information separation in `templates/context-topology.yaml`.
4. Instantiate and validate `templates/orchestration.yaml`.
5. Run adversary, advocate, and blind paths from immutable input snapshots.
6. Integrate findings, preserve dissent, and reclassify epistemic status.
7. Derive case-generation axes and create visible and holdout cases.
8. Plan, execute, and independently judge the evaluation.
9. Localize failures and replay regression cases before promoting improvements.

## Stateful execution harness

The harness does not call a particular LLM. It creates a safe stage packet for the surrounding agent runtime and verifies declared outputs before releasing downstream stages.

```bash
python scripts/orchestrate.py init templates/orchestration.yaml \
  --run-dir ./runs/example \
  --bind source_materials=/absolute/path/to/source

python scripts/orchestrate.py ready --run-dir ./runs/example
python scripts/orchestrate.py start source_normalizer --run-dir ./runs/example
# Execute the emitted packet and write its declared artifacts.
python scripts/orchestrate.py complete source_normalizer --run-dir ./runs/example
python scripts/orchestrate.py status --run-dir ./runs/example
```

Use `packet`, `fail`, `set`, and `publish` for inspection, routing, outer-loop control, and canonical artifact publication.

## Package contents

- `SKILL.md`: evaluation orchestration contract.
- `FEEDBACK-MAPPING.md`: trace from review feedback to concrete implementation.
- `CHANGELOG.md`: packaged changes by version.
- `references/evaluation-ir.md`: canonical decision-centered intermediate representation.
- `references/evaluation-primitives.md`: reusable evaluation operations.
- `references/evaluation-patterns.md`: suitable loop topologies.
- `references/orchestration.md`: execution graph, stage contracts, integration rules, and failure routing.
- `references/agent-contracts.md`: shared agent execution rules.
- `references/evaluation-smells.md`: common failure patterns.
- `templates/`: charters, IR, findings, orchestration, cases, topology, traces, contracts, and improvements.
- `scripts/lint_evaluation.py`: package and reference lint.
- `scripts/validate_orchestration.py`: structural graph, contract, artifact, dependency, and isolation validation.
- `scripts/orchestrate.py`: stateful vendor-neutral execution harness.
- `examples/catalog-review/`: compact reconstruction of the motivating catalog-model workflow.
