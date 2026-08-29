#!/usr/bin/env python3
"""Validate required profile fields and confirmation state."""
from __future__ import annotations

import argparse
from pathlib import Path

from common import load_profile, write_json

USER_ONLY = (
    ("applicant", None),
    ("copyright", "development_method"),
    ("copyright", "rights_acquisition"),
    ("dates", "completion_date"),
    ("dates", "publication_status"),
)


def resolved_entry(profile: dict, group: str, field: str | None) -> dict:
    entry = profile.get(group, {})
    entry = entry.get(field, {}) if field else entry
    # Version 1 profile compatibility: fields were nested under copyright.
    return entry if isinstance(entry, dict) else {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    profile = load_profile(args.profile)
    blockers, warnings = [], []
    software = profile.get("software", {})
    for field in ("full_name", "version"):
        entry = resolved_entry(profile, "software", field)
        value = entry.get("value", software.get(field, ""))
        if not str(value).strip():
            blockers.append({"code": "PROFILE_REQUIRED", "field": f"software.{field}", "message": "Required software identity is missing."})
    for group, field in USER_ONLY:
        entry = resolved_entry(profile, group, field)
        label = f"{group}.{field}" if field else group
        if entry.get("status") != "confirmed" or not str(entry.get("value", "")).strip():
            blockers.append({"code": "CONFIRMATION_REQUIRED", "field": label, "message": "User-only fact must be confirmed."})
    if profile.get("status", {}).get("profile_confirmed") is not True:
        warnings.append({"code": "PROFILE_NOT_CONFIRMED", "message": "Profile confirmation flag is not true."})
    write_json(args.output, {"status": "READY" if not blockers else "NEEDS_CONFIRMATION", "blockers": blockers, "warnings": warnings, "info": [{"rules_version": "2026.08"}]})


if __name__ == "__main__":
    main()
