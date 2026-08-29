#!/usr/bin/env python3
"""Independent reviewer gate for generated Copyright Forge materials."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from common import load_profile, write_json

TEXT_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml", ".html"}


def value(entry: Any) -> str:
    return str(entry.get("value", "")).strip() if isinstance(entry, dict) else str(entry or "").strip()


def identity_values(profile: dict[str, Any]) -> dict[str, str]:
    software = profile.get("software", {})
    return {
        "software.full_name": value(software.get("full_name")),
        "software.version": value(software.get("version")),
        "applicant": value(profile.get("applicant")),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    parser.add_argument("evidence_map", type=Path)
    parser.add_argument("materials", type=Path)
    parser.add_argument("--task-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    profile = load_profile(args.profile)
    evidence = json.loads(args.evidence_map.read_text(encoding="utf-8"))
    state_path = args.task_dir / ".copyright-forge" / "workflow-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    checked: list[str] = []
    if state.get("state") not in {"REVIEWING", "READY"}:
        blockers.append({"code": "REVIEW_STATE_REQUIRED", "message": "Task must be in REVIEWING before final review."})
    fingerprint = hashlib.sha256(args.profile.read_bytes()).hexdigest()
    if not state.get("facts_fingerprint"):
        blockers.append({"code": "FACTS_NOT_LOCKED", "message": "Profile facts have not been locked in the task."})
    elif state["facts_fingerprint"] != fingerprint:
        blockers.append({"code": "LOCKED_FACTS_CHANGED", "message": "Profile changed after facts were locked."})
    evidence_features = {item.get("id"): item for item in evidence.get("features", []) if item.get("evidence")}
    profile_features = profile.get("features", [])
    if not isinstance(profile_features, list):
        blockers.append({"code": "PROFILE_FEATURES_INVALID", "message": "Profile features must be a list of evidence-backed feature ids."})
        profile_features = []
    for feature_id in profile_features:
        if feature_id not in evidence_features:
            blockers.append({"code": "UNSUPPORTED_CLAIM", "feature_id": feature_id, "message": "Profile feature has no project evidence."})
    for path in sorted(args.materials.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        relative = path.relative_to(args.materials).as_posix()
        checked.append(relative)
        for label, expected in identity_values(profile).items():
            if expected and expected not in text:
                blockers.append({"code": "IDENTITY_MISMATCH", "path": relative, "field": label, "message": "Material does not contain the locked identity value."})
        for feature_id, item in evidence_features.items():
            name = str(item.get("name", "")).strip()
            if name and name in text and feature_id not in profile_features:
                blockers.append({"code": "UNSUPPORTED_CLAIM", "path": relative, "feature_id": feature_id, "message": "Material names a feature that is not approved in the locked profile."})
        if re.search(r"(?i)\b(api[_-]?key|access[_-]?token|password|private key)\b\s*[:=]", text):
            blockers.append({"code": "SENSITIVE_CONTENT", "path": relative, "message": "Potential sensitive content must be redacted in the generated copy before delivery."})
    if not checked:
        blockers.append({"code": "NO_MATERIALS", "message": "No reviewable material files were found."})
    write_json(args.output, {"status": "READY" if not blockers else "NEEDS_FIX", "blockers": blockers, "warnings": warnings, "info": [{"checked_files": checked}, {"evidence_backed_feature_count": len(profile_features)}]})


if __name__ == "__main__":
    main()
