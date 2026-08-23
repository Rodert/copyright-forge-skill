#!/usr/bin/env python3
"""Scan a project without modifying it and write a compact analysis report."""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from common import SOURCE_EXTENSIONS, iter_project_files, write_json

LANGUAGES = {".go": "Go", ".java": "Java", ".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript", ".vue": "Vue", ".rs": "Rust", ".kt": "Kotlin"}
MARKERS = {"go.mod": "Go modules", "pom.xml": "Maven", "build.gradle": "Gradle", "requirements.txt": "Python requirements", "pyproject.toml": "Python project", "package.json": "Node.js", "vite.config.ts": "Vite", "vue.config.js": "Vue CLI", "manage.py": "Django"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()
    files = list(iter_project_files(root))
    extensions = Counter(path.suffix.lower() for path in files)
    languages = sorted({LANGUAGES[ext] for ext in extensions if ext in LANGUAGES})
    markers = sorted(name for name in MARKERS if (root / name).exists())
    source_files = [path.relative_to(root).as_posix() for path in files if path.suffix.lower() in SOURCE_EXTENSIONS]
    write_json(args.output, {"project": str(root), "file_count": len(files), "source_file_count": len(source_files), "languages": languages, "markers": [{"file": name, "meaning": MARKERS[name]} for name in markers], "extension_counts": dict(sorted(extensions.items())), "source_files": source_files})


if __name__ == "__main__":
    main()
