# Copyright Forge Skill

Copyright Forge Skill is an AI Agent Skill for preparing draft materials for
Chinese software copyright registration from real software projects.

It analyzes a project, records evidence for each described feature, builds one
canonical software profile, prepares documentation and source-code materials,
and checks consistency and likely secrets before handoff.

It does not submit an application, create an official application form, modify
the original project, invent facts or functionality, or guarantee registration
approval.

## Included

- Project and technology-stack scanning for Go, Java, Python, Node.js, Vue,
  and React projects.
- Evidence-first feature mapping.
- One `software-profile.yaml` as the source of truth for every deliverable.
- Deterministic source-code selection for ordinary deposit materials.
- Secret detection and redaction in generated copies only.
- Profile, consistency, and output validation reports.

## Layout

The distributable skill is [skills/copyright-forge](skills/copyright-forge).
Use its [SKILL.md](skills/copyright-forge/SKILL.md) as the entrypoint.

## Quick Start

Run the helpers with Python 3.10+; they use only the standard library and do
not modify the analyzed project.

```bash
SKILL=skills/copyright-forge
OUT=/tmp/copyright-forge-output

python3 "$SKILL/scripts/scan_project.py" /path/to/project --output "$OUT/project-scan.json"
python3 "$SKILL/scripts/build_evidence_map.py" /path/to/project --output "$OUT/evidence-map.json"
python3 "$SKILL/scripts/collect_source.py" /path/to/project --output "$OUT/source-manifest.json"
```

Copy the profile template into the output directory, confirm user-only facts,
then run `validate_profile.py`. Use the generated JSON as review input; do not
treat it as a completed registration application.

## Scope

The first release supports ordinary deposit workflows. Exceptional deposit,
joint development, commissioned development, inherited or transferred rights,
and modified third-party software are identified as manual-review cases.

Rules are for preparation and validation only. Confirm application facts and
current requirements through the applicable official registration channel
before submission.

## License

Apache-2.0. See [LICENSE](LICENSE).
