#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

CORE_STAGES = [
    "source_normalizer",
    "adversarial_extractor",
    "advocate_extractor",
    "blind_coverage_explorer",
    "finding_integrator",
    "epistemic_reclassifier",
    "evaluation_case_designer",
    "evaluation_run_planner",
    "final_evaluator",
    "blinded_evaluation_judge",
]

IMPROVEMENT_STAGES = [
    "failure_localizer",
    "improvement_candidate_generator",
    "regression_replay",
    "improvement_promotion_judge",
]

REQUIRED_ASSERTIONS = {
    "finding_integrator": {"dissent_is_preserved", "blind_only_findings_are_marked"},
    "epistemic_reclassifier": {"agent_consensus_does_not_promote_fact_status"},
    "evaluation_case_designer": {"case_generation_axes_are_derived_from_target"},
}


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}") from None
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML in {path}: {exc}") from exc


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def find_package_root(orchestration_path: Path) -> Path:
    for candidate in [orchestration_path.parent, *orchestration_path.parents]:
        if (candidate / "SKILL.md").exists():
            return candidate
    cwd = Path.cwd().resolve()
    if (cwd / "SKILL.md").exists():
        return cwd
    return orchestration_path.parent.parent


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = load_yaml(path)
    except ValueError as exc:
        return [str(exc)]

    if not isinstance(data, dict):
        return ["orchestration root must be a mapping"]

    for key in ["version", "workflow_id", "artifacts", "stages", "parallel_groups", "routing"]:
        if key not in data:
            errors.append(f"missing top-level key: {key}")

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, dict):
        artifacts = {}
        errors.append("artifacts must be a mapping")

    stages_raw = data.get("stages")
    if not isinstance(stages_raw, list):
        return errors + ["stages must be a list"]

    stage_by_id: dict[str, dict[str, Any]] = {}
    positions: dict[str, int] = {}
    for index, stage in enumerate(stages_raw):
        if not isinstance(stage, dict):
            errors.append(f"stage at index {index} must be a mapping")
            continue
        stage_id = stage.get("id")
        if not isinstance(stage_id, str) or not stage_id:
            errors.append(f"stage at index {index} has no valid id")
            continue
        if stage_id in stage_by_id:
            errors.append(f"duplicate stage id: {stage_id}")
            continue
        stage_by_id[stage_id] = stage
        positions[stage_id] = index

    for stage_id in CORE_STAGES + IMPROVEMENT_STAGES:
        if stage_id not in stage_by_id:
            errors.append(f"missing stage: {stage_id}")

    canonical = [s for s in CORE_STAGES + IMPROVEMENT_STAGES if s in positions]
    if canonical != sorted(canonical, key=lambda s: positions[s]):
        errors.append("canonical stage order is not preserved")

    for stage_id, stage in stage_by_id.items():
        for field in [
            "role",
            "contract_ref",
            "depends_on",
            "visible_inputs",
            "hidden_inputs",
            "outputs",
            "success_assertions",
            "retry_limit",
            "failure_route",
        ]:
            if field not in stage:
                errors.append(f"{stage_id}: missing field {field}")

        deps = _as_list(stage.get("depends_on"))
        for dep in deps:
            if dep not in stage_by_id:
                errors.append(f"{stage_id}: dependency does not exist: {dep}")
            elif positions.get(dep, 10**9) >= positions.get(stage_id, -1):
                errors.append(f"{stage_id}: dependency must appear earlier: {dep}")

        visible = set(_as_list(stage.get("visible_inputs")))
        hidden = set(_as_list(stage.get("hidden_inputs")))
        overlap = visible & hidden
        if overlap:
            errors.append(f"{stage_id}: inputs cannot be both visible and hidden: {sorted(overlap)}")

        outputs = _as_list(stage.get("outputs"))
        if not outputs:
            errors.append(f"{stage_id}: outputs must not be empty")
        for output in outputs:
            if output not in artifacts:
                errors.append(f"{stage_id}: output artifact is not declared: {output}")

        retry_limit = stage.get("retry_limit")
        if not isinstance(retry_limit, int) or retry_limit < 0:
            errors.append(f"{stage_id}: retry_limit must be a non-negative integer")

        route = stage.get("failure_route")
        if isinstance(route, str):
            for target in route.split("|"):
                if target and target not in stage_by_id:
                    errors.append(f"{stage_id}: failure_route target does not exist: {target}")
        else:
            errors.append(f"{stage_id}: failure_route must be a stage id or | separated stage ids")

        assertions = set(_as_list(stage.get("success_assertions")))
        for required in REQUIRED_ASSERTIONS.get(stage_id, set()):
            if required not in assertions:
                errors.append(f"{stage_id}: missing success assertion {required}")

    # Detect dependency cycles independently of declaration order.
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(stage_id: str) -> None:
        if stage_id in visiting:
            errors.append(f"dependency cycle detected at: {stage_id}")
            return
        if stage_id in visited or stage_id not in stage_by_id:
            return
        visiting.add(stage_id)
        for dep in _as_list(stage_by_id[stage_id].get("depends_on")):
            if isinstance(dep, str):
                visit(dep)
        visiting.remove(stage_id)
        visited.add(stage_id)

    for stage_id in stage_by_id:
        visit(stage_id)

    blind = stage_by_id.get("blind_coverage_explorer", {})
    blind_visible = set(_as_list(blind.get("visible_inputs")))
    blind_hidden = set(_as_list(blind.get("hidden_inputs")))
    for forbidden in ["source_ir_v0", "seeded_concerns", "adversarial_findings", "advocate_findings"]:
        if forbidden not in blind_hidden:
            errors.append(f"blind_coverage_explorer: must hide {forbidden}")
        if forbidden in blind_visible:
            errors.append(f"blind_coverage_explorer: forbidden visible input {forbidden}")

    parallel_groups = data.get("parallel_groups")
    if not isinstance(parallel_groups, list):
        errors.append("parallel_groups must be a list")
    else:
        perspective_group = None
        for group in parallel_groups:
            if isinstance(group, dict) and group.get("id") == "perspective_extraction":
                perspective_group = group
                break
        if not perspective_group:
            errors.append("missing parallel group: perspective_extraction")
        else:
            expected = {"adversarial_extractor", "advocate_extractor", "blind_coverage_explorer"}
            actual = set(_as_list(perspective_group.get("stages")))
            if actual != expected:
                errors.append(f"perspective_extraction stages must be exactly {sorted(expected)}")
            if perspective_group.get("immutable_input_snapshot") is not True:
                errors.append("perspective_extraction must use immutable_input_snapshot: true")
            if perspective_group.get("cross_agent_visibility") is not False:
                errors.append("perspective_extraction must use cross_agent_visibility: false")

    routing = data.get("routing")
    if not isinstance(routing, dict):
        errors.append("routing must be a mapping")
    else:
        if routing.get("earliest_responsible_stage") is not True:
            errors.append("routing.earliest_responsible_stage must be true")
        if not isinstance(routing.get("max_total_retries"), int):
            errors.append("routing.max_total_retries must be an integer")

    package_root = find_package_root(path)

    published = data.get("published_artifacts")
    if not isinstance(published, dict):
        errors.append("published_artifacts must be a mapping")
    else:
        for public_name, artifact_ref in published.items():
            if isinstance(artifact_ref, str) and artifact_ref.startswith("templates/"):
                candidate = package_root / artifact_ref
                if not candidate.exists():
                    errors.append(f"published artifact path does not exist: {artifact_ref}")
            elif artifact_ref not in artifacts:
                errors.append(f"published artifact {public_name} refers to unknown artifact: {artifact_ref}")

    registry_ref = data.get("contract_registry")
    if not isinstance(registry_ref, str):
        errors.append("contract_registry must be a path string")
    else:
        registry_path = package_root / registry_ref
        try:
            registry = load_yaml(registry_path)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            contracts = registry.get("contracts", {}) if isinstance(registry, dict) else {}
            if not isinstance(contracts, dict):
                errors.append("contract registry must contain a contracts mapping")
            else:
                for stage_id, stage in stage_by_id.items():
                    contract_ref = stage.get("contract_ref")
                    if contract_ref not in contracts:
                        errors.append(f"{stage_id}: contract_ref not found in registry: {contract_ref}")
                        continue
                    contract = contracts.get(contract_ref)
                    if not isinstance(contract, dict):
                        errors.append(f"{stage_id}: contract must be a mapping: {contract_ref}")
                        continue
                    output_schemas = contract.get("output_schemas")
                    if output_schemas is None and isinstance(contract.get("output_schema"), str):
                        output_schemas = [contract.get("output_schema")]
                    if not isinstance(output_schemas, list) or not output_schemas:
                        errors.append(f"{stage_id}: contract has no output_schemas: {contract_ref}")
                    else:
                        for output_schema in output_schemas:
                            if not isinstance(output_schema, str):
                                errors.append(f"{stage_id}: contract output schema must be a string: {output_schema!r}")
                            elif output_schema.startswith("templates/") and not (package_root / output_schema).exists():
                                errors.append(f"{stage_id}: contract output_schema does not exist: {output_schema}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate evaluation orchestration structure and isolation constraints.")
    parser.add_argument("path", nargs="?", default="templates/orchestration.yaml")
    args = parser.parse_args()
    path = Path(args.path).resolve()
    errors = validate(path)
    if errors:
        print("Orchestration validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Orchestration validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
