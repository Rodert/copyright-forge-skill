#!/usr/bin/env python3
"""Select a deterministic, first-party source sequence for ordinary deposit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import is_probably_text, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    files, total = [], 0
    for item in manifest.get("files", []):
        path = root / item["path"]
        if not path.is_file() or not is_probably_text(path):
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        if not lines:
            continue
        files.append({"path": item["path"], "lines": len(lines), "start_line": total + 1, "end_line": total + len(lines)})
        total += len(lines)
    write_json(args.output, {
        "schema_version": "1.0",
        "project": str(root),
        "files": files,
        "total_lines": total,
        "selection_rule": "Whole first-party files in deterministic manifest order; no source content is edited.",
        "ordinary_deposit_note": "Formatting selection is validated against the local rules registry; confirm current official service guidance before submission.",
    })


if __name__ == "__main__":
    main()
