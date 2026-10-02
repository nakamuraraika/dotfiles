# Feedback Mapping

| Feedback | Implementation |
|---|---|
| Decision-centered IR was conceptual but not a concrete schema | Added `templates/evaluation-ir.yaml`; each decision binds observed design, rationale, invariants, attack, defense, verification, and structural alternatives. |
| Required templates, references, scripts, and examples were missing | Added complete template set, `references/evaluation-patterns.md`, `scripts/lint_evaluation.py`, and `examples/catalog-review/`. |
| Validator only matched strings and could pass a broken package | Rebuilt `scripts/validate_orchestration.py` around parsed YAML, dependency/cycle checks, artifact and contract resolution, isolation checks, and failure-route validation. |
| Orchestration had no execution layer | Added `scripts/orchestrate.py` for stage packets, dependency gates, visible/hidden input boundaries, artifact gates, retries, earliest-stage routing, conditions, and publication. |
| Adversary and advocate could share omissions from the normalizer | Added primary-source supremacy rules and assertions requiring direct source reads and independent-discovery reporting. |
| Edge cases were categories rather than target-derived generation axes | Added state, transition, ownership, lifecycle, authority, representation, environment, and recovery axes to IR and case templates. |
| Failure localization and improvement phases were not connected to the graph | Added conditional `failure_localizer`, `improvement_candidate_generator`, `regression_replay`, and `improvement_promotion_judge` stages. |
| Artifact names and published outputs were inconsistent | Added canonical artifact registry and `published_artifacts` mapping in `templates/orchestration.yaml`. |
| Role separation lacked executable contracts | Added `templates/agent-contracts.yaml` plus output schemas for every stage. |
| The motivating example could anchor the entire evaluator | Recast it as a synthetic transition-axis case in `examples/catalog-review/`, while the reusable mechanism remains domain-independent. |
