#!/usr/bin/env python3
"""Convert conservative evidence candidates into a scored feature graph."""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

from common import write_json


def key_for(item: dict) -> str:
    stem = str(item.get("name", item.get("id", ""))).lower()
    stem = re.sub(r"(?:controller|service|handler|repository|model|view|page|api)$", "", stem)
    return re.sub(r"[^a-z0-9]+", "-", stem).strip("-") or str(item.get("id", "feature"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_map", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence_map = json.loads(args.evidence_map.read_text(encoding="utf-8"))
    groups: dict[str, list[dict]] = defaultdict(list)
    for item in evidence_map.get("features", []):
        if item.get("evidence"):
            groups[key_for(item)].append(item)
    features = []
    for index, (key, items) in enumerate(sorted(groups.items()), 1):
        evidence = [entry for item in items for entry in item["evidence"]]
        types = {entry["type"] for entry in evidence}
        paths = {entry["path"] for entry in evidence}
        score = min(1.0, round(0.18 * len(types) + 0.10 * min(len(paths), 4), 2))
        eligible = score >= 0.5 and len(paths) >= 2
        features.append({
            "id": f"F{index:03d}",
            "name": items[0]["name"],
            "support_score": score,
            "documentation_eligibility": eligible,
            "evidence": evidence,
            "source_candidates": [item["id"] for item in items],
        })
    write_json(args.output, {
        "schema_version": "1.0",
        "project": evidence_map.get("project"),
        "features": features,
        "note": "Feature names remain candidates. Documentation eligibility is a deterministic minimum gate, not proof of a user-facing claim.",
    })


if __name__ == "__main__":
    main()
