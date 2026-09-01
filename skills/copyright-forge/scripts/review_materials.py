#!/usr/bin/env python3
"""Run Copyright Forge's eight deterministic quality gates."""
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
    return {"software.full_name": value(software.get("full_name")), "software.version": value(software.get("version")), "applicant": value(profile.get("applicant"))}


def gate(gate_id: str, name: str, findings: list[dict[str, Any]]) -> dict[str, Any]:
    return {"id": gate_id, "name": name, "status": "PASS" if not findings else "FAIL", "findings": findings}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    parser.add_argument("evidence_map", type=Path)
    parser.add_argument("materials", type=Path)
    parser.add_argument("--task-dir", type=Path, required=True)
    parser.add_argument("--feature-graph", type=Path)
    parser.add_argument("--source-page-plan", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    profile = load_profile(args.profile)
    evidence = json.loads(args.evidence_map.read_text(encoding="utf-8"))
    state_path = args.task_dir / ".copyright-forge" / "workflow-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    checked: list[str] = []
    gates: list[dict[str, Any]] = []

    fact_findings = []
    if state.get("state") not in {"REVIEWING", "READY"}:
        fact_findings.append({"code": "REVIEW_STATE_REQUIRED", "message": "Task must be in REVIEWING before final review."})
    fingerprint = hashlib.sha256(args.profile.read_bytes()).hexdigest()
    if not state.get("facts_fingerprint"):
        fact_findings.append({"code": "FACTS_NOT_LOCKED", "message": "Profile facts have not been locked in the task."})
    elif state["facts_fingerprint"] != fingerprint:
        fact_findings.append({"code": "LOCKED_FACTS_CHANGED", "message": "Profile changed after facts were locked."})
    gates.append(gate("G1", "Fact Gate", fact_findings)); blockers.extend(fact_findings)

    evidence_features = {item.get("id"): item for item in evidence.get("features", []) if item.get("evidence")}
    profile_features = profile.get("features", [])
    evidence_findings = []
    if not isinstance(profile_features, list):
        evidence_findings.append({"code": "PROFILE_FEATURES_INVALID", "message": "Profile features must be a list of evidence-backed feature ids."}); profile_features = []
    for feature_id in profile_features:
        if feature_id not in evidence_features:
            evidence_findings.append({"code": "UNSUPPORTED_CLAIM", "feature_id": feature_id, "message": "Profile feature has no project evidence."})
    if args.feature_graph and args.feature_graph.exists():
        graph = json.loads(args.feature_graph.read_text(encoding="utf-8"))
        for feature in graph.get("features", []):
            if feature.get("id") in profile_features and not feature.get("documentation_eligibility"):
                evidence_findings.append({"code": "FEATURE_GRAPH_INELIGIBLE", "feature_id": feature["id"], "message": "Feature score does not meet the documentation threshold."})
    gates.append(gate("G2", "Evidence Gate", evidence_findings)); blockers.extend(evidence_findings)

    consistency_findings, privacy_findings, hallucination_findings = [], [], []
    for path in sorted(args.materials.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        relative = path.relative_to(args.materials).as_posix(); checked.append(relative)
        for label, expected in identity_values(profile).items():
            if expected and expected not in text:
                consistency_findings.append({"code": "IDENTITY_MISMATCH", "path": relative, "field": label, "message": "Material does not contain the locked identity value."})
        for feature_id, item in evidence_features.items():
            name = str(item.get("name", "")).strip()
            if name and name in text and feature_id not in profile_features:
                hallucination_findings.append({"code": "UNSUPPORTED_CLAIM", "path": relative, "feature_id": feature_id, "message": "Material names a feature not approved in the locked profile."})
        if re.search(r"(?i)\b(api[_-]?key|access[_-]?token|password|private key)\b\s*[:=]", text):
            privacy_findings.append({"code": "SENSITIVE_CONTENT", "path": relative, "message": "Potential sensitive content must be redacted before delivery."})
    if not checked:
        consistency_findings.append({"code": "NO_MATERIALS", "message": "No reviewable material files were found."})
    gates.append(gate("G3", "Consistency Gate", consistency_findings)); blockers.extend(consistency_findings)

    source_findings = []
    if args.source_page_plan and args.source_page_plan.exists():
        plan = json.loads(args.source_page_plan.read_text(encoding="utf-8"))
        if plan.get("lines_per_page", 0) < 50:
            source_findings.append({"code": "SOURCE_LINES_PER_PAGE", "message": "Source pages contain fewer than 50 lines."})
    else:
        warnings.append({"code": "SOURCE_GATE_PENDING", "message": "No source page plan was supplied for final source-material review."})
    gates.append(gate("G4", "Source Gate", source_findings)); blockers.extend(source_findings)

    document_findings = []
    if not any(path.endswith((".md", ".html", ".docx", ".pdf")) for path in checked):
        document_findings.append({"code": "DOCUMENT_MISSING", "message": "No documentation artifact was found."})
    gates.append(gate("G5", "Document Gate", document_findings)); blockers.extend(document_findings)
    gates.append(gate("G6", "Privacy Gate", privacy_findings)); blockers.extend(privacy_findings)
    gates.append(gate("G7", "Hallucination Gate", hallucination_findings)); blockers.extend(hallucination_findings)
    preflight_findings = []
    if value(profile.get("copyright", {}).get("rights_acquisition")) in {"委托开发", "合作开发", "受让", "继承", "修改他人软件"}:
        preflight_findings.append({"code": "RIGHTS_CHAIN_REVIEW", "message": "Complex rights chain needs contract and ownership review before submission."})
    gates.append(gate("G8", "Submission Preflight", preflight_findings)); warnings.extend(preflight_findings)
    score = max(0, 100 - len(blockers) * 12 - len(warnings) * 3)
    status = "READY" if not blockers else "NEEDS_FIX"
    write_json(args.output, {"status": status, "quality_score": score, "quality_label": "READY" if status == "READY" and not warnings else "READY_WITH_WARNINGS" if status == "READY" else "NEEDS_FIX", "gates": gates, "blockers": blockers, "warnings": warnings, "info": [{"checked_files": checked}, {"evidence_backed_feature_count": len(profile_features)}]})


if __name__ == "__main__":
    main()
