#!/usr/bin/env python3
"""Build conservative path-based feature evidence from a project tree."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import SOURCE_EXTENSIONS, is_probably_text, iter_project_files, write_json

PATTERNS = [
    ("route", re.compile(r"\b(GET|POST|PUT|PATCH|DELETE)\s*\(|\b(router|app)\.(get|post|put|patch|delete)\b|\bhttp\.Handle(?:Func)?\s*\(", re.I)),
    ("model", re.compile(r"\b(class|struct|type)\s+\w+|\bCREATE\s+TABLE\b", re.I)),
    ("handler", re.compile(r"\b(handler|controller|service|repository)\b", re.I)),
    ("source_code", re.compile(r"\bfunc\s+\w+|\bdef\s+\w+|\b(class|function)\s+\w+", re.I)),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root, features = args.project.resolve(), []
    for path in iter_project_files(root):
        if path.suffix.lower() not in SOURCE_EXTENSIONS or not is_probably_text(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")[:200_000]
        except OSError:
            continue
        evidence = [kind for kind, pattern in PATTERNS if pattern.search(text)]
        if evidence:
            features.append({"id": path.relative_to(root).as_posix().replace("/", "-").replace(".", "-"), "name": path.stem.replace("_", " ").replace("-", " "), "confidence": "medium", "evidence": [{"type": kind, "path": path.relative_to(root).as_posix()} for kind in evidence]})
    write_json(args.output, {"project": str(root), "features": features, "note": "Path-based candidate evidence. Confirm feature names before use in a document."})


if __name__ == "__main__":
    main()
