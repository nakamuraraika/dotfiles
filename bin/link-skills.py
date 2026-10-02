#!/usr/bin/env python3
"""Link personal skills without overwriting existing installations (dry run by default)."""
import argparse
import os
from pathlib import Path
import sys

CATEGORIES = ("core", "frontend", "backend", "experimental", "meta")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="create links; default: preview")
    parser.add_argument("--target", choices=("codex", "claude", "both"), default="both")
    parser.add_argument("--codex-dir", type=Path, default=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills")
    parser.add_argument("--claude-dir", type=Path, default=Path.home() / ".claude" / "skills")
    args = parser.parse_args()
    source_root = Path(__file__).resolve().parents[1] / "skills"
    skills = {}
    for category in CATEGORIES:
        for entry in sorted((source_root / category).iterdir()):
            if not (entry / "SKILL.md").is_file():
                continue
            if entry.name in skills:
                raise ValueError(f"Duplicate skill name: {entry.name}")
            skills[entry.name] = entry.resolve()
    if not skills:
        raise ValueError("No skills found")
    targets = []
    if args.target in ("codex", "both"):
        targets.append(args.codex_dir.expanduser().absolute())
    if args.target in ("claude", "both"):
        targets.append(args.claude_dir.expanduser().absolute())
    pending, conflicts = [], []
    seen = set()
    for target in targets:
        # Do not write into the source tree, even through a directory symlink.
        resolved = target.resolve()
        if resolved == source_root or source_root in resolved.parents:
            raise ValueError(f"Destination is inside the source tree: {target}")
        if resolved in seen:
            continue
        seen.add(resolved)
        ancestor = target
        while not os.path.lexists(ancestor):
            ancestor = ancestor.parent
        if not ancestor.is_dir():
            raise ValueError(f"Destination ancestor is not a directory: {ancestor}")
        for name, source in sorted(skills.items()):
            destination = target / name
            if destination.is_symlink() and destination.resolve() == source:
                print(f"OK {destination}")
            elif os.path.lexists(destination):
                conflicts.append(destination)
            else:
                pending.append((source, destination))
                print(f"LINK {destination} -> {source}")
    if conflicts:
        for destination in conflicts:
            print(f"CONFLICT {destination} (preserved; move aside after reviewing)", file=sys.stderr)
        return 1
    if args.apply:
        for source, destination in pending:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(source, target_is_directory=True)
        print(f"Created {len(pending)} links.")
    else:
        print(f"Dry run: {len(pending)} links; use --apply to create them.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
