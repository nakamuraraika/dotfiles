#!/usr/bin/env python3
"""Validate that a ROM workspace contains required sections and flag empty critical fields."""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys

REQUIRED_HEADINGS = [
    "Frame", "Current highlights", "Evidence inventory", "Concept inventory",
    "Current model", "Challenge results", "Decisions", "Learning log", "Next feedback"
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args()
    if not args.workspace.is_file():
        print(f"ERROR: file not found: {args.workspace}")
        return 2
    text = args.workspace.read_text(encoding="utf-8")
    headings = set(re.findall(r"^#{1,6}\s+(?:\d+\.\s*)?(.+?)\s*$", text, re.M))
    missing = [h for h in REQUIRED_HEADINGS if h not in headings]
    if missing:
        print("ERROR: missing sections: " + ", ".join(missing))
        return 1
    warnings = []
    for field in ["Purpose:", "Decision supported:", "Highest-value next question:"]:
        if re.search(rf"^- {re.escape(field)}\s*$", text, re.M):
            warnings.append(field.rstrip(":"))
    print("OK: required sections found")
    if warnings:
        print("WARNING: empty critical fields: " + ", ".join(warnings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
