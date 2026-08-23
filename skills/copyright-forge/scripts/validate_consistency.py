#!/usr/bin/env python3
"""Check profile identity and evidence references against draft materials."""
from __future__ import annotations

import argparse
from pathlib import Path

from common import load_profile, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    parser.add_argument("materials", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    software = load_profile(args.profile).get("software", {})
    required = [str(software.get("full_name", "")).strip(), str(software.get("version", "")).strip()]
    blockers, checked = [], []
    for path in sorted(args.materials.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".json", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        missing = [value for value in required if value and value not in text]
        checked.append(path.relative_to(args.materials).as_posix())
        if missing:
            blockers.append({"code": "IDENTITY_MISMATCH", "path": checked[-1], "missing": missing})
    write_json(args.output, {"status": "READY" if not blockers else "NOT_READY", "blockers": blockers, "warnings": [], "checked_files": checked})


if __name__ == "__main__":
    main()
