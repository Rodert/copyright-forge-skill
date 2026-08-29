#!/usr/bin/env python3
"""Create, resume, and safely transition a Copyright Forge task."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import iter_project_files, load_profile, write_json

STATE_FILE = ".copyright-forge/workflow-state.json"
STATES = {"ANALYZING", "WAITING_FOR_CONFIRMATION", "FACTS_LOCKED", "GENERATING", "REVIEWING", "NEEDS_FIX", "READY"}
TRANSITIONS = {
    "ANALYZING": {"WAITING_FOR_CONFIRMATION", "FACTS_LOCKED"},
    "WAITING_FOR_CONFIRMATION": {"ANALYZING", "FACTS_LOCKED"},
    "FACTS_LOCKED": {"GENERATING", "ANALYZING"},
    "GENERATING": {"REVIEWING", "NEEDS_FIX"},
    "REVIEWING": {"READY", "NEEDS_FIX"},
    "NEEDS_FIX": {"GENERATING", "WAITING_FOR_CONFIRMATION", "ANALYZING"},
    "READY": {"ANALYZING"},
}


def project_snapshot(project: Path) -> str:
    digest = hashlib.sha256()
    for path in iter_project_files(project):
        try:
            digest.update(path.relative_to(project).as_posix().encode() + b"\0")
            digest.update(hashlib.sha256(path.read_bytes()).digest())
        except OSError:
            continue
    return digest.hexdigest()


def state_path(task_dir: Path) -> Path:
    return task_dir / STATE_FILE


def read_state(task_dir: Path) -> dict[str, Any]:
    path = state_path(task_dir)
    if not path.exists():
        raise SystemExit(f"No Copyright Forge task exists in {task_dir}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(task_dir: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    write_json(state_path(task_dir), state)


def missing_confirmed_facts(profile: dict[str, Any]) -> list[str]:
    required = [("software", field) for field in ("full_name", "short_name", "version")]
    required.append(("applicant", None))
    required += [("copyright", field) for field in ("development_method", "rights_acquisition")]
    required += [("dates", field) for field in ("completion_date", "publication_status")]
    missing = []
    for group, field in required:
        entry = profile.get(group, {})
        entry = entry.get(field, {}) if field else entry
        if not isinstance(entry, dict) or not str(entry.get("value", "")).strip() or entry.get("status") != "confirmed":
            missing.append(f"{group}.{field}" if field else group)
    return missing


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("project", type=Path)
    init.add_argument("task_dir", type=Path)
    status = sub.add_parser("status")
    status.add_argument("task_dir", type=Path)
    transition = sub.add_parser("transition")
    transition.add_argument("task_dir", type=Path)
    transition.add_argument("to", choices=sorted(STATES))
    lock = sub.add_parser("lock")
    lock.add_argument("task_dir", type=Path)
    lock.add_argument("--profile", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "init":
        project, task_dir = args.project.resolve(), args.task_dir.resolve()
        if not project.is_dir():
            raise SystemExit("Project directory does not exist")
        if task_dir == project or project in task_dir.parents:
            raise SystemExit("Task output directory must be outside the project")
        if state_path(task_dir).exists():
            raise SystemExit("Task already exists; use status or transition to resume it")
        state = {"schema_version": "1.0", "state": "ANALYZING", "project": str(project), "project_snapshot": project_snapshot(project), "facts_fingerprint": None, "history": [{"state": "ANALYZING", "reason": "task initialized"}]}
        save_state(task_dir, state)
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return

    task_dir = args.task_dir.resolve()
    state = read_state(task_dir)
    project_changed = project_snapshot(Path(state["project"])) != state["project_snapshot"]
    if args.command == "status":
        state["project_changed"] = project_changed
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return
    if args.command == "lock":
        if project_changed:
            raise SystemExit("Project changed since analysis; return task to ANALYZING before locking facts")
        missing = missing_confirmed_facts(load_profile(args.profile))
        if missing:
            raise SystemExit("Facts require confirmation: " + ", ".join(missing))
        if state["state"] not in {"ANALYZING", "WAITING_FOR_CONFIRMATION"}:
            raise SystemExit("Facts can only be locked after analysis or confirmation")
        state["state"] = "FACTS_LOCKED"
        state["facts_fingerprint"] = hashlib.sha256(args.profile.read_bytes()).hexdigest()
        state["history"].append({"state": "FACTS_LOCKED", "reason": "confirmed facts locked"})
        save_state(task_dir, state)
        return
    if args.to not in TRANSITIONS[state["state"]]:
        raise SystemExit(f"Invalid transition: {state['state']} -> {args.to}")
    state["state"] = args.to
    if args.to == "ANALYZING":
        state["project_snapshot"] = project_snapshot(Path(state["project"]))
        state["facts_fingerprint"] = None
    state["history"].append({"state": args.to, "reason": "workflow transition"})
    save_state(task_dir, state)


if __name__ == "__main__":
    main()
