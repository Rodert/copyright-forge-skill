#!/usr/bin/env python3
"""Create a deterministic first-party source manifest; never edit the project."""
from __future__ import annotations

import argparse
from pathlib import Path

from common import SOURCE_EXTENSIONS, is_probably_text, iter_project_files, write_json

PRIORITY = ("main", "app", "server", "router", "route", "handler", "controller", "service", "repository", "model", "middleware", "component", "page", "view")


def rank(relative: str) -> tuple[int, str]:
    lower = relative.lower()
    for index, word in enumerate(PRIORITY):
        if word in lower:
            return (index, lower)
    return (len(PRIORITY), lower)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-files", type=int, default=200)
    args = parser.parse_args()
    root, selected = args.project.resolve(), []
    for path in iter_project_files(root):
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() not in SOURCE_EXTENSIONS or not is_probably_text(path):
            continue
        try:
            lines = len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
        except OSError:
            continue
        selected.append({"path": relative, "lines": lines})
    selected.sort(key=lambda item: rank(item["path"]))
    selected = selected[: args.max_files]
    write_json(args.output, {"project": str(root), "selection_rule": "deterministic core-code ranking; review before final pagination", "files": selected, "total_lines": sum(item["lines"] for item in selected), "ordinary_deposit_note": "Apply current official continuity and page-count requirements when formatting final materials."})


if __name__ == "__main__":
    main()
