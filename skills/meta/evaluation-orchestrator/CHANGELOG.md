# Changelog

## 2.0 — Feedback integration

### Decision-centered IR
- Added `templates/evaluation-ir.yaml` with a canonical decision record binding observed design, rationale, invariants, attack, defense, verification, and structural alternatives.
- Added explicit case-generation axes and epistemic change logging.

### Independent evaluation paths
- Required adversary and advocate agents to read primary sources directly and use normalized IR only as an index.
- Strengthened blind-path visibility constraints and direct-source discovery assertions.

### Executable orchestration
- Added `templates/agent-contracts.yaml` and output schemas for every stage.
- Added `evaluation_case_designer` and conditional improvement-loop stages to the orchestration graph.
- Added `scripts/orchestrate.py` for state, dependency, input visibility, artifact, retry, failure-routing, and publication gates.

### Validation and package completeness
- Replaced string-based orchestration checking with YAML structural validation of stages, dependencies, cycles, artifacts, contracts, parallel isolation, and failure routes.
- Added `scripts/lint_evaluation.py` to detect missing documented assets, invalid YAML, incomplete decision IR, and broken package references.
- Added all templates, references, and examples previously declared but missing.

### Evaluation cases and safe improvement
- Added risk-derived case axes, protected holdout expectations, judge reports, failure localization, regression replay, promotion decisions, and rollback-aware improvement candidates.
- Added a compact catalog-model example demonstrating how to separate observation from attack and defense hypotheses.
