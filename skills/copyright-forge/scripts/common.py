#!/usr/bin/env python3
"""Small standard-library helpers shared by Copyright Forge scripts."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

EXCLUDED_DIRS = {
    ".git", ".github", ".idea", ".vscode", "node_modules", "vendor", "dist",
    "build", "coverage", "target", ".next", ".nuxt", ".output", ".cache",
    "__pycache__", ".venv", "venv",
}
SOURCE_EXTENSIONS = {".go", ".java", ".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".cs", ".cpp", ".c", ".h", ".php", ".rb", ".rs", ".kt", ".sql"}
EXCLUDED_NAMES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "go.sum", "cargo.lock"}


def iter_project_files(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
        for name in sorted(files):
            path = Path(current, name)
            if name in EXCLUDED_NAMES or name.endswith((".min.js", ".map", ".lock")):
                continue
            yield path


def is_probably_text(path: Path) -> bool:
    try:
        return b"\0" not in path.read_bytes()[:4096]
    except OSError:
        return False


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_profile(path: Path) -> dict[str, Any]:
    """Read JSON profiles or the bundled simple YAML profile shape without PyYAML."""
    text = path.read_text(encoding="utf-8")
    if text.lstrip().startswith("{"):
        return json.loads(text)
    result: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, result)]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or raw.lstrip().startswith("-"):
            continue
        match = re.match(r"^(\s*)([A-Za-z_][\w-]*):\s*(.*?)\s*$", raw)
        if not match:
            continue
        indent, key, value = len(match.group(1)), match.group(2), match.group(3)
        while stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if not value:
            node: dict[str, Any] = {}
            parent[key] = node
            stack.append((indent, node))
        elif value == "[]":
            parent[key] = []
        elif value.lower() in {"true", "false"}:
            parent[key] = value.lower() == "true"
        else:
            parent[key] = value.strip("\"'")
    return result
