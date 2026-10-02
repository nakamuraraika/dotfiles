#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

FILES = {
    "00-brief.md": "# Evaluation Brief\n",
    "01-evidence-map.md": "# Evidence Map\n",
    "02-evaluation-ir.md": "# Evaluation IR\n",
    "03-supporting-review.md": "# Supporting Review\n",
    "04-adversarial-review.md": "# Adversarial Review\n",
    "05-coverage-review.md": "# Coverage Review\n",
    "06-alternatives.md": "# Alternatives\n",
    "07-findings.md": "# Findings\n\n## FND-000 — Initial placeholder\n\n- Classification: UNKNOWN\n- Severity: NOTE\n- Confidence: LOW\n\nReplace or remove this placeholder after the first evaluation run.\n",
    "08-report.md": "# Evaluation Report\n\n## Verdict\n",
    "09-change-log.md": "# Evaluation Change Log\n",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an evaluation workspace")
    parser.add_argument("destination", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    dest = args.destination
    if dest.exists() and any(dest.iterdir()) and not args.force:
        raise SystemExit(f"Destination is not empty: {dest}. Use --force to overwrite known files.")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "evidence").mkdir(exist_ok=True)
    for name, content in FILES.items():
        path = dest / name
        if not path.exists() or args.force:
            path.write_text(content, encoding="utf-8")
    print(f"Created workspace: {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
