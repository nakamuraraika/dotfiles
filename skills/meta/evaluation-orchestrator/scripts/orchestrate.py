#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from validate_orchestration import validate

STATE_NAME = ".evaluation-orchestrator-state.yaml"
TERMINAL_SUCCESS = {"passed", "skipped"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def save_yaml(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False, allow_unicode=True), encoding="utf-8")


def parse_pairs(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected key=value, got: {value}")
        key, raw = value.split("=", 1)
        if not key:
            raise ValueError(f"empty key in binding: {value}")
        result[key] = raw
    return result


def parse_scalar(value: str) -> Any:
    lowered = value.strip().lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value.strip().strip('"\'')


def state_path(run_dir: Path) -> Path:
    return run_dir / STATE_NAME


def load_state(run_dir: Path) -> dict[str, Any]:
    path = state_path(run_dir)
    if not path.exists():
        raise ValueError(f"run state not found: {path}; run init first")
    state = load_yaml(path)
    if not isinstance(state, dict):
        raise ValueError(f"invalid run state: {path}")
    return state


def save_state(run_dir: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = now()
    save_yaml(state_path(run_dir), state)


def package_root_from_orchestration(path: Path) -> Path:
    return path.resolve().parent.parent


def resolve_artifact_path(state: dict[str, Any], run_dir: Path, artifact_name: str) -> Path | None:
    binding = state.get("bindings", {}).get(artifact_name)
    if binding:
        path = Path(binding)
        return path if path.is_absolute() else (run_dir / path)
    artifact_rel = state.get("workflow", {}).get("artifacts", {}).get(artifact_name)
    if not isinstance(artifact_rel, str):
        return None
    path = Path(artifact_rel)
    return path if path.is_absolute() else (run_dir / path)


def resolve_value(state: dict[str, Any], run_dir: Path, token: str) -> tuple[bool, Any]:
    if token in state.get("variables", {}):
        return True, state["variables"][token]
    parts = token.split(".")
    artifact_path = resolve_artifact_path(state, run_dir, parts[0])
    if artifact_path is None or not artifact_path.exists() or artifact_path.is_dir():
        return False, None
    try:
        value = load_yaml(artifact_path)
    except Exception:
        return False, None
    for part in parts[1:]:
        if not isinstance(value, dict) or part not in value:
            return False, None
        value = value[part]
    return True, value


def eval_atom(state: dict[str, Any], run_dir: Path, atom: str) -> bool | None:
    match = re.fullmatch(r"\s*([A-Za-z_][\w.]*)\s*(==|!=)\s*(.*?)\s*", atom)
    if not match:
        return None
    token, operator, raw_expected = match.groups()
    found, actual = resolve_value(state, run_dir, token)
    if not found:
        return None
    expected = parse_scalar(raw_expected)
    return actual == expected if operator == "==" else actual != expected


def eval_condition(state: dict[str, Any], run_dir: Path, expression: str) -> bool | None:
    or_groups = [group.strip() for group in expression.split(" or ")]
    group_results: list[bool | None] = []
    for group in or_groups:
        atoms = [atom.strip() for atom in group.split(" and ")]
        atom_results = [eval_atom(state, run_dir, atom) for atom in atoms]
        if any(result is False for result in atom_results):
            group_results.append(False)
        elif all(result is True for result in atom_results):
            group_results.append(True)
        else:
            group_results.append(None)
    if any(result is True for result in group_results):
        return True
    if all(result is False for result in group_results):
        return False
    return None


def refresh(state: dict[str, Any], run_dir: Path) -> None:
    stages = state["stages"]
    changed = True
    while changed:
        changed = False
        for stage_id in state["stage_order"]:
            stage_state = stages[stage_id]
            if stage_state["status"] in {"running", "passed", "failed", "escalated"}:
                continue
            definition = state["stage_definitions"][stage_id]
            deps = definition.get("depends_on", [])
            if not all(stages[dep]["status"] in TERMINAL_SUCCESS for dep in deps):
                if stage_state["status"] == "ready":
                    stage_state["status"] = "pending"
                    changed = True
                continue
            condition = definition.get("when")
            if condition:
                result = eval_condition(state, run_dir, condition)
                if result is False and stage_state["status"] != "skipped":
                    stage_state["status"] = "skipped"
                    stage_state["skip_reason"] = f"condition false: {condition}"
                    changed = True
                    continue
                if result is None:
                    if stage_state["status"] == "ready":
                        stage_state["status"] = "pending"
                        changed = True
                    continue
                if result is True and stage_state["status"] == "skipped":
                    stage_state["status"] = "pending"
                    stage_state["skip_reason"] = ""
                    changed = True
            if stage_state["status"] == "pending":
                stage_state["status"] = "ready"
                changed = True


def descendants(state: dict[str, Any], root: str) -> set[str]:
    result = {root}
    changed = True
    while changed:
        changed = False
        for stage_id, definition in state["stage_definitions"].items():
            if stage_id not in result and any(dep in result for dep in definition.get("depends_on", [])):
                result.add(stage_id)
                changed = True
    return result


def initialize(args: argparse.Namespace) -> int:
    orchestration_path = Path(args.orchestration).resolve()
    errors = validate(orchestration_path)
    if errors:
        print("Cannot initialize invalid orchestration:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    workflow = load_yaml(orchestration_path)
    run_dir = Path(args.run_dir).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    if state_path(run_dir).exists() and not args.force:
        print(f"run state already exists: {state_path(run_dir)}", file=sys.stderr)
        return 1

    bindings = parse_pairs(args.bind)
    variables = {key: parse_scalar(value) for key, value in parse_pairs(args.set).items()}
    variables.setdefault("outer_loop_requested", False)
    package_root = package_root_from_orchestration(orchestration_path)
    registry_path = package_root / workflow["contract_registry"]
    contracts = load_yaml(registry_path).get("contracts", {})

    stage_definitions = {stage["id"]: stage for stage in workflow["stages"]}
    state = {
        "version": "1.0",
        "run_id": args.run_id or run_dir.name,
        "created_at": now(),
        "updated_at": now(),
        "orchestration_source": str(orchestration_path),
        "package_root": str(package_root),
        "workflow": {
            "version": workflow.get("version"),
            "workflow_id": workflow.get("workflow_id"),
            "artifacts": workflow.get("artifacts", {}),
            "published_artifacts": workflow.get("published_artifacts", {}),
            "routing": workflow.get("routing", {}),
        },
        "bindings": bindings,
        "variables": variables,
        "stage_order": [stage["id"] for stage in workflow["stages"]],
        "stage_definitions": stage_definitions,
        "contracts": contracts,
        "total_retries": 0,
        "events": [],
        "stages": {
            stage["id"]: {
                "status": "pending",
                "attempts": 0,
                "started_at": "",
                "completed_at": "",
                "last_error": "",
                "skip_reason": "",
                "output_paths": {},
            }
            for stage in workflow["stages"]
        },
    }

    for artifact_path in workflow.get("artifacts", {}).values():
        if isinstance(artifact_path, str) and artifact_path.endswith("/"):
            (run_dir / artifact_path).mkdir(parents=True, exist_ok=True)
        elif isinstance(artifact_path, str):
            (run_dir / artifact_path).parent.mkdir(parents=True, exist_ok=True)

    charter_target = resolve_artifact_path(state, run_dir, "evaluation_charter")
    charter_template = package_root / "templates/evaluation-charter.yaml"
    if charter_target and not charter_target.exists() and charter_template.exists():
        charter_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(charter_template, charter_target)

    metadata_dir = run_dir / ".orchestrator"
    metadata_dir.mkdir(exist_ok=True)
    shutil.copy2(orchestration_path, metadata_dir / "orchestration.snapshot.yaml")
    shutil.copy2(registry_path, metadata_dir / "agent-contracts.snapshot.yaml")

    refresh(state, run_dir)
    state["events"].append({"at": now(), "event": "initialized"})
    save_state(run_dir, state)
    print(f"initialized evaluation run: {run_dir}")
    print(f"edit charter: {charter_target}")
    return 0


def command_status(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state = load_state(run_dir)
    refresh(state, run_dir)
    save_state(run_dir, state)
    print(f"run: {state['run_id']}  retries: {state['total_retries']}")
    width = max(len(stage_id) for stage_id in state["stage_order"])
    for stage_id in state["stage_order"]:
        stage = state["stages"][stage_id]
        suffix = f"  ({stage['skip_reason']})" if stage.get("skip_reason") else ""
        print(f"{stage_id:<{width}}  {stage['status']:<9} attempts={stage['attempts']}{suffix}")
    return 0


def command_ready(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state = load_state(run_dir)
    refresh(state, run_dir)
    save_state(run_dir, state)
    ready = [stage_id for stage_id in state["stage_order"] if state["stages"][stage_id]["status"] == "ready"]
    print("\n".join(ready))
    return 0


def build_packet(state: dict[str, Any], run_dir: Path, stage_id: str) -> dict[str, Any]:
    if stage_id not in state["stage_definitions"]:
        raise ValueError(f"unknown stage: {stage_id}")
    definition = state["stage_definitions"][stage_id]
    visible: dict[str, Any] = {}
    for name in definition.get("visible_inputs", []):
        path = resolve_artifact_path(state, run_dir, name)
        visible[name] = str(path) if path else {"external_input": name}
    outputs: dict[str, str] = {}
    for name in definition.get("outputs", []):
        path = resolve_artifact_path(state, run_dir, name)
        if path:
            outputs[name] = str(path)
    return {
        "run_id": state["run_id"],
        "stage_id": stage_id,
        "status": state["stages"][stage_id]["status"],
        "role": definition.get("role"),
        "contract": copy.deepcopy(state["contracts"].get(definition.get("contract_ref"), {})),
        "visible_inputs": visible,
        "hidden_inputs": definition.get("hidden_inputs", []),
        "forbidden_visibility": definition.get("hidden_inputs", []),
        "outputs": outputs,
        "success_assertions": definition.get("success_assertions", []),
        "failure_route": definition.get("failure_route"),
    }


def command_packet(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state = load_state(run_dir)
    refresh(state, run_dir)
    packet = build_packet(state, run_dir, args.stage)
    print(yaml.safe_dump(packet, sort_keys=False, allow_unicode=True))
    return 0


def command_start(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state = load_state(run_dir)
    refresh(state, run_dir)
    if args.stage not in state["stages"]:
        raise ValueError(f"unknown stage: {args.stage}")
    stage = state["stages"][args.stage]
    if stage["status"] != "ready":
        raise ValueError(f"stage is not ready: {args.stage} ({stage['status']})")
    stage["status"] = "running"
    stage["attempts"] += 1
    stage["started_at"] = now()
    state["events"].append({"at": now(), "event": "stage_started", "stage_id": args.stage, "attempt": stage["attempts"]})
    save_state(run_dir, state)
    print(yaml.safe_dump(build_packet(state, run_dir, args.stage), sort_keys=False, allow_unicode=True))
    return 0


def output_exists(path: Path) -> bool:
    if not path.exists():
        return False
    if path.is_dir():
        return any(path.iterdir())
    return path.stat().st_size > 0


def command_complete(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state = load_state(run_dir)
    if args.stage not in state["stages"]:
        raise ValueError(f"unknown stage: {args.stage}")
    stage_state = state["stages"][args.stage]
    if stage_state["status"] not in {"running", "ready"}:
        raise ValueError(f"stage cannot complete from status: {stage_state['status']}")

    for name, raw_path in parse_pairs(args.artifact).items():
        state["bindings"][name] = raw_path

    definition = state["stage_definitions"][args.stage]
    missing: list[str] = []
    output_paths: dict[str, str] = {}
    for output_name in definition.get("outputs", []):
        path = resolve_artifact_path(state, run_dir, output_name)
        if path is None or not output_exists(path):
            missing.append(f"{output_name} ({path})")
        else:
            output_paths[output_name] = str(path)
    if missing:
        raise ValueError("missing or empty declared outputs: " + ", ".join(missing))

    stage_state["status"] = "passed"
    stage_state["completed_at"] = now()
    stage_state["output_paths"] = output_paths
    stage_state["last_error"] = ""
    state["events"].append({"at": now(), "event": "stage_passed", "stage_id": args.stage})
    refresh(state, run_dir)
    save_state(run_dir, state)
    print(f"completed: {args.stage}")
    return 0


def choose_route(state: dict[str, Any], route_text: str, current: str) -> str | None:
    candidates = [candidate for candidate in route_text.split("|") if candidate in state["stage_definitions"]]
    if not candidates:
        return None
    candidates.sort(key=lambda stage_id: state["stage_order"].index(stage_id))
    non_self = [candidate for candidate in candidates if candidate != current]
    return non_self[0] if non_self else candidates[0]


def command_fail(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state = load_state(run_dir)
    if args.stage not in state["stages"]:
        raise ValueError(f"unknown stage: {args.stage}")
    stage_state = state["stages"][args.stage]
    definition = state["stage_definitions"][args.stage]
    stage_state["last_error"] = args.reason
    state["total_retries"] += 1
    max_total = state["workflow"].get("routing", {}).get("max_total_retries", 0)
    retry_limit = definition.get("retry_limit", 0)

    if state["total_retries"] > max_total:
        stage_state["status"] = "escalated"
        state["events"].append({"at": now(), "event": "retry_budget_exhausted", "stage_id": args.stage, "reason": args.reason})
    elif stage_state["attempts"] <= retry_limit:
        stage_state["status"] = "ready"
        state["events"].append({"at": now(), "event": "stage_retry_scheduled", "stage_id": args.stage, "reason": args.reason})
    else:
        route = choose_route(state, definition.get("failure_route", ""), args.stage)
        if route is None or route == args.stage:
            stage_state["status"] = "escalated"
            state["events"].append({"at": now(), "event": "stage_escalated", "stage_id": args.stage, "reason": args.reason})
        else:
            affected = descendants(state, route)
            for stage_id in affected:
                state["stages"][stage_id]["status"] = "pending"
                state["stages"][stage_id]["completed_at"] = ""
                state["stages"][stage_id]["output_paths"] = {}
            state["stages"][route]["status"] = "ready"
            state["events"].append({
                "at": now(),
                "event": "failure_routed",
                "from_stage": args.stage,
                "to_stage": route,
                "reason": args.reason,
            })
    refresh(state, run_dir)
    save_state(run_dir, state)
    print(f"recorded failure: {args.stage} -> {state['stages'][args.stage]['status']}")
    return 0


def command_set(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state = load_state(run_dir)
    for key, raw in parse_pairs(args.values).items():
        state["variables"][key] = parse_scalar(raw)
    refresh(state, run_dir)
    save_state(run_dir, state)
    print("variables updated")
    return 0


def command_publish(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    state = load_state(run_dir)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    package_root = Path(state["package_root"])
    copied: list[str] = []
    for public_name, artifact_ref in state["workflow"].get("published_artifacts", {}).items():
        if isinstance(artifact_ref, str) and artifact_ref.startswith("templates/"):
            source = package_root / artifact_ref
        else:
            source = resolve_artifact_path(state, run_dir, artifact_ref)
        if source is None or not source.exists():
            if args.allow_missing:
                continue
            raise ValueError(f"cannot publish missing artifact: {public_name} <- {source}")
        target = output_dir / public_name
        if source.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
        copied.append(public_name)
    print("published: " + ", ".join(copied))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stateful execution harness for the evaluation-orchestrator Skill.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("orchestration", nargs="?", default="templates/orchestration.yaml")
    init.add_argument("--run-dir", required=True)
    init.add_argument("--run-id")
    init.add_argument("--bind", action="append", default=[], help="Bind an input/artifact: key=path")
    init.add_argument("--set", action="append", default=[], help="Set a run variable: key=value")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=initialize)

    for name, func in [("status", command_status), ("ready", command_ready)]:
        cmd = sub.add_parser(name)
        cmd.add_argument("--run-dir", required=True)
        cmd.set_defaults(func=func)

    packet = sub.add_parser("packet")
    packet.add_argument("stage")
    packet.add_argument("--run-dir", required=True)
    packet.set_defaults(func=command_packet)

    start = sub.add_parser("start")
    start.add_argument("stage")
    start.add_argument("--run-dir", required=True)
    start.set_defaults(func=command_start)

    complete = sub.add_parser("complete")
    complete.add_argument("stage")
    complete.add_argument("--run-dir", required=True)
    complete.add_argument("--artifact", action="append", default=[], help="Override output artifact: key=path")
    complete.set_defaults(func=command_complete)

    fail = sub.add_parser("fail")
    fail.add_argument("stage")
    fail.add_argument("--run-dir", required=True)
    fail.add_argument("--reason", required=True)
    fail.set_defaults(func=command_fail)

    set_cmd = sub.add_parser("set")
    set_cmd.add_argument("values", nargs="+")
    set_cmd.add_argument("--run-dir", required=True)
    set_cmd.set_defaults(func=command_set)

    publish = sub.add_parser("publish")
    publish.add_argument("--run-dir", required=True)
    publish.add_argument("--output-dir", required=True)
    publish.add_argument("--allow-missing", action="store_true")
    publish.set_defaults(func=command_publish)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (ValueError, OSError, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
