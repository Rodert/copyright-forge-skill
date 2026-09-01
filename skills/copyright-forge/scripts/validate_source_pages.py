#!/usr/bin/env python3
"""Validate source page selection for ordinary-deposit preparation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("page_plan", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.page_plan.read_text(encoding="utf-8"))
    blockers = []
    if plan.get("available_pages", 0) < 1:
        blockers.append({"code": "SOURCE_EMPTY", "message": "No source program pages were generated."})
    if plan.get("lines_per_page", 0) < 50:
        blockers.append({"code": "SOURCE_LINES_PER_PAGE", "message": "Source pages must contain at least 50 lines."})
    available, included = plan.get("available_pages", 0), plan.get("included_original_pages", [])
    expected = list(range(1, available + 1)) if available < 60 else list(range(1, 31)) + list(range(available - 29, available + 1))
    if included != expected:
        blockers.append({"code": "SOURCE_CONTINUITY", "message": "Selected pages do not match the ordinary-deposit continuity rule."})
    write_json(args.output, {"status": "READY" if not blockers else "NEEDS_FIX", "blockers": blockers, "warnings": [], "info": [{"available_pages": available, "included_pages": len(included)}]})


if __name__ == "__main__":
    main()
