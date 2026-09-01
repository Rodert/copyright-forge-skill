#!/usr/bin/env python3
"""Create a human-reviewable rules-source availability report; never edit rules."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from common import write_json


def load_registry(path: Path) -> list[dict]:
    # The registry is deliberately a constrained YAML list; JSON avoids a new dependency.
    entries, current = [], None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("- id:"):
            current = {"id": line.split(":", 1)[1].strip()}; entries.append(current)
        elif current and ":" in line:
            key, value = line.split(":", 1); current[key.strip()] = value.strip().strip('"')
    return entries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fetch", action="store_true", help="Best-effort fetch official pages; failures are reported, never fatal")
    args = parser.parse_args()
    sources = load_registry(args.registry)
    findings = []
    for source in sources:
        result = {"id": source.get("id"), "url": source.get("source_url"), "status": "not_checked"}
        if args.fetch and source.get("source_url"):
            try:
                request = Request(source["source_url"], headers={"User-Agent": "Copyright-Forge-Rules-Radar/1.0"})
                with urlopen(request, timeout=15) as response:
                    body = response.read(2_000_000)
                    result.update({"status": "retrieved", "http_status": response.status, "content_sha256": hashlib.sha256(body).hexdigest(), "retrieved_on": str(date.today())})
            except (URLError, TimeoutError, OSError) as exc:
                result.update({"status": "unavailable", "message": str(exc)})
        findings.append(result)
    write_json(args.output, {"status": "REVIEW_REQUIRED", "checked_on": str(date.today()), "sources": findings, "message": "This report records source availability and content fingerprints only. It does not change rules; compare retrieved content and approve any rule revision manually."})


if __name__ == "__main__":
    main()
