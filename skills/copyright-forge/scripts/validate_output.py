#!/usr/bin/env python3
"""Combine validation reports into a final gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    blockers, warnings, info = [], [], []
    for report_path in args.reports:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        blockers.extend({"report": report_path.name, **item} if isinstance(item, dict) else {"report": report_path.name, "message": str(item)} for item in report.get("blockers", []))
        warnings.extend(report.get("warnings", []))
        info.extend(report.get("info", []))
    status = "READY" if not blockers else "NOT_READY"
    write_json(args.output, {"rules_version": "2026.08", "status": status, "blockers": blockers, "warnings": warnings, "info": info})


if __name__ == "__main__":
    main()
