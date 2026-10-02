#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

REQUIRED_PATHS = [
    "README.md",
    "SKILL.md",
    "FEEDBACK-MAPPING.md",
    "CHANGELOG.md",
    "references/evaluation-ir.md",
    "references/evaluation-primitives.md",
    "references/evaluation-patterns.md",
    "references/evaluation-smells.md",
    "references/orchestration.md",
    "references/agent-contracts.md",
    "templates/evaluation-charter.yaml",
    "templates/evaluation-ir.yaml",
    "templates/evaluation-case.yaml",
    "templates/evaluation-run-plan.yaml",
    "templates/context-topology.yaml",
    "templates/finding.yaml",
    "templates/orchestration.yaml",
    "templates/run-trace.yaml",
    "templates/transformation-record.yaml",
    "templates/improvement-candidate.yaml",
    "templates/epistemic-change-log.yaml",
    "templates/agent-contracts.yaml",
    "templates/source-snapshot.yaml",
    "templates/findings-set.yaml",
    "templates/judge-report.yaml",
    "templates/failure-localization.yaml",
    "templates/regression-replay-report.yaml",
    "templates/promotion-decision.yaml",
    "templates/evaluation-run-instructions.md",
    "templates/final-evaluation.md",
    "scripts/validate_orchestration.py",
    "scripts/orchestrate.py",
    "examples/catalog-review/README.md",
    "examples/catalog-review/evaluation-charter.yaml",
    "examples/catalog-review/evaluation-ir.yaml",
    "examples/catalog-review/evaluation-cases/CASE-PRIMARY-ARC.yaml",
]


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML in {path.relative_to(path.parents[1])}: {exc}") from exc


def nested_keys(mapping: Any, path: list[str]) -> bool:
    current = mapping
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return False
        current = current[key]
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint an evaluation-orchestrator Skill package.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    for relative in REQUIRED_PATHS:
        if not (root / relative).exists():
            errors.append(f"missing required path: {relative}")

    for unwanted in [".DS_Store", "__pycache__"]:
        found = list(root.rglob(unwanted))
        if found:
            errors.append(f"unwanted package artifact: {found[0].relative_to(root)}")

    for yaml_path in sorted(root.rglob("*.yaml")):
        try:
            load_yaml(yaml_path)
        except ValueError as exc:
            errors.append(str(exc))

    ir_path = root / "templates/evaluation-ir.yaml"
    if ir_path.exists():
        ir = load_yaml(ir_path)
        required_ir = [
            ["target"],
            ["source_items"],
            ["decisions"],
            ["evaluation_dimensions"],
            ["case_generation_axes"],
        ]
        for key_path in required_ir:
            if not nested_keys(ir, key_path):
                errors.append(f"evaluation IR missing: {'.'.join(key_path)}")
        decisions = ir.get("decisions", []) if isinstance(ir, dict) else []
        if not decisions or not isinstance(decisions[0], dict):
            errors.append("evaluation IR must contain a decision record example")
        else:
            decision = decisions[0]
            for key in ["observed_design", "rationale", "invariants", "attack", "defense", "verification", "candidate_alternatives"]:
                if key not in decision:
                    errors.append(f"decision record missing key: {key}")

    # Detect stale backticked package references in the primary documentation.
    reference_pattern = re.compile(r"`((?:templates|references|scripts|examples)/[^`\s]+)`")
    for doc_name in ["README.md", "SKILL.md"]:
        doc = root / doc_name
        if not doc.exists():
            continue
        for ref in reference_pattern.findall(doc.read_text(encoding="utf-8")):
            cleaned = ref.rstrip(".,;:")
            if any(token in cleaned for token in ["*", "{"]):
                continue
            candidate = root / cleaned
            if not candidate.exists():
                errors.append(f"{doc_name} references missing path: {cleaned}")

    validator = root / "scripts/validate_orchestration.py"
    orchestration = root / "templates/orchestration.yaml"
    if validator.exists() and orchestration.exists():
        result = subprocess.run(
            [sys.executable, str(validator), str(orchestration)],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            errors.append("orchestration validation failed")
            errors.extend(f"validator: {line}" for line in result.stdout.splitlines()[1:])

    skill = (root / "SKILL.md").read_text(encoding="utf-8") if (root / "SKILL.md").exists() else ""
    if "does not create or package other Skills" not in skill:
        warnings.append("SKILL.md should explicitly state that this Skill evaluates targets rather than creating Skills")

    if errors:
        print("Evaluation package lint failed:")
        for error in errors:
            print(f"- {error}")
        for warning in warnings:
            print(f"warning: {warning}")
        return 1

    print(f"Evaluation package lint passed: {root}")
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
