#!/usr/bin/env python3
"""Validate required profile fields and confirmation state."""
from __future__ import annotations

import argparse
from pathlib import Path

from common import load_profile, write_json

USER_ONLY = ("owner", "development_method", "rights_acquisition", "completion_date", "publication_status")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    profile = load_profile(args.profile)
    blockers, warnings = [], []
    software = profile.get("software", {})
    for field in ("full_name", "version"):
        if not str(software.get(field, "")).strip():
            blockers.append({"code": "PROFILE_REQUIRED", "field": f"software.{field}", "message": "Required software identity is missing."})
    copyright = profile.get("copyright", {})
    for field in USER_ONLY:
        value = copyright.get(field, {})
        if not isinstance(value, dict) or value.get("status") != "confirmed" or not str(value.get("value", "")).strip():
            blockers.append({"code": "CONFIRMATION_REQUIRED", "field": f"copyright.{field}", "message": "User-only fact must be confirmed."})
    if profile.get("status", {}).get("profile_confirmed") is not True:
        warnings.append({"code": "PROFILE_NOT_CONFIRMED", "message": "Profile confirmation flag is not true."})
    write_json(args.output, {"status": "READY" if not blockers else "NEEDS_CONFIRMATION", "blockers": blockers, "warnings": warnings, "info": [{"rules_version": "2026.08"}]})


if __name__ == "__main__":
    main()
