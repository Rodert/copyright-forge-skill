#!/usr/bin/env python3
"""Report or redact likely secrets in a generated copy, never the input project."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import is_probably_text, iter_project_files, write_json

RULES = [
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("generic_api_key", re.compile(r"\b(?:sk|api)[_-][A-Za-z0-9_-]{16,}\b", re.I)),
    ("assignment_secret", re.compile(r"(?i)\b(password|passwd|secret|token|api[_-]?key|access[_-]?key)\b\s*[:=]\s*[\"']([^\"']{8,})[\"']")),
    ("connection_string", re.compile(r"(?i)\b(?:postgres|mysql|mongodb(?:\+srv)?|redis)://[^\s\"']+")),
]


def redact_line(line: str) -> tuple[str, list[str]]:
    matches = []
    for name, pattern in RULES:
        if pattern.search(line):
            matches.append(name)
            if name == "assignment_secret":
                line = pattern.sub(lambda m: m.group(1) + " = [REDACTED]", line)
            else:
                line = pattern.sub("[REDACTED]", line)
    return line, matches


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Generated copy to inspect")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--redact-to", type=Path, help="Optional separate redacted copy")
    args = parser.parse_args()
    root, findings = args.source.resolve(), []
    for path in iter_project_files(root):
        if not is_probably_text(path):
            continue
        relative = path.relative_to(root)
        try:
            lines = path.read_text(encoding="utf-8", errors="surrogateescape").splitlines(keepends=True)
        except OSError:
            continue
        rewritten = []
        for number, line in enumerate(lines, 1):
            changed, kinds = redact_line(line)
            rewritten.append(changed)
            for kind in kinds:
                findings.append({"path": relative.as_posix(), "line": number, "type": kind, "reason": "Potential sensitive value"})
        if args.redact_to:
            target = args.redact_to / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("".join(rewritten), encoding="utf-8", errors="surrogateescape")
    write_json(args.output, {"source": str(root), "finding_count": len(findings), "findings": findings, "note": "Heuristic scan; review manually before sharing."})


if __name__ == "__main__":
    main()
