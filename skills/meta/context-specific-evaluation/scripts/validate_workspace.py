#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_FILES = {
    "00-brief.md",
    "02-evaluation-ir.md",
    "07-findings.md",
    "08-report.md",
}
FINDING_PATTERN = re.compile(r"\bFND-\d{3,}\b")
CLASSIFICATIONS = ("FACT", "INTERPRETATION", "HYPOTHESIS", "UNKNOWN", "CONFLICT")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    if not root.is_dir():
        return [f"Workspace does not exist or is not a directory: {root}"]

    present = {p.name for p in root.iterdir() if p.is_file()}
    for name in sorted(REQUIRED_FILES - present):
        errors.append(f"Missing required file: {name}")

    findings = root / "07-findings.md"
    if findings.exists():
        text = findings.read_text(encoding="utf-8")
        if not FINDING_PATTERN.search(text):
            errors.append("07-findings.md contains no stable FND-### ID")
        if not any(label in text for label in CLASSIFICATIONS):
            errors.append("07-findings.md contains no evidence classification")

    report = root / "08-report.md"
    if report.exists():
        text = report.read_text(encoding="utf-8").upper()
        if "VERDICT" not in text and "判定" not in text:
            errors.append("08-report.md has no verdict section")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an evaluation workspace")
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args()

    errors = validate(args.workspace)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Workspace structure is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
