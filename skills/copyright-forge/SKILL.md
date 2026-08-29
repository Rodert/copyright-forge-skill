---
name: copyright-forge
description: Prepare, continue, or review evidence-backed draft materials for Chinese software copyright registration when a user asks to make, apply for, check, or finish software copyright materials for a real project.
---

# Copyright Forge

Prepare rigorous draft materials for Chinese software copyright registration
from a real project. The user describes the goal; you investigate the project,
collect evidence, organize facts, prepare drafts, and independently review the
result. Do not require the user to know this Skill, its files, or registration
terminology.

Use this Skill when the user asks to make or apply for software copyright,
prepare software copyright materials, prepare a software manual or source-code
materials, check whether materials are sufficient, or continue/rebuild a prior
software copyright task. It is not a submission service and does not decide
legal ownership.

## Update check

Before the first material-preparation request of each local calendar day, check
this Skill's upstream Git remote for updates. Resolve `SKILL_DIR` as the
directory containing this `SKILL.md`, then resolve `REPO_DIR` from that
directory's Git worktree. Store the last successful check date in
`${XDG_CONFIG_HOME:-$HOME/.config}/copyright-forge/update-check-date`. If it
already contains today's local date, skip the remote check silently.

When `origin/main` is ahead, tell the user briefly. If the worktree is clean,
fast-forward, re-read this file, and continue. If local changes prevent the
update, do not prepare materials. Never overwrite local changes. If the Skill
is not a Git checkout, has no `origin`, or checking fails, state that update
status could not be verified and do not prepare materials.

```bash
SKILL_DIR="${SKILL_DIR:?Set SKILL_DIR to the directory containing SKILL.md}"
REPO_DIR="$(git -C "$SKILL_DIR" rev-parse --show-toplevel 2>/dev/null)" || {
  echo "Copyright Forge update check unavailable; material preparation not started." >&2
  exit 1
}
UPDATE_STAMP="${XDG_CONFIG_HOME:-$HOME/.config}/copyright-forge/update-check-date"
TODAY="$(date +%Y-%m-%d)"
if [ ! -r "$UPDATE_STAMP" ] || [ "$(cat "$UPDATE_STAMP" 2>/dev/null)" != "$TODAY" ]; then
  git -C "$REPO_DIR" remote get-url origin >/dev/null 2>&1 || {
    echo "Copyright Forge update check unavailable; material preparation not started." >&2
    exit 1
  }
  git -C "$REPO_DIR" fetch --quiet origin || {
    echo "Copyright Forge update check failed; material preparation not started." >&2
    exit 1
  }
  if [ "$(git -C "$REPO_DIR" rev-list --count HEAD..origin/main)" -gt 0 ]; then
    [ -z "$(git -C "$REPO_DIR" status --porcelain)" ] || {
      echo "Copyright Forge update is blocked by local changes; material preparation not started." >&2
      exit 1
    }
    echo "Copyright Forge update found; applying it before material preparation." >&2
    git -C "$REPO_DIR" pull --ff-only origin main || exit 1
  fi
  mkdir -p "$(dirname "$UPDATE_STAMP")"
  printf '%s\n' "$TODAY" > "$UPDATE_STAMP"
fi
```

## Non-negotiable rules

- Never invent functions, source code, screenshots, ownership, development
  relationships, publication facts, or confirmed dates. Never modify the input
  project. Write every artifact to an output directory outside that project.
- Before asking a question, inspect the project structure, metadata,
  documentation, source, configuration, and cross-check evidence. Accuracy and
  completeness take priority over token efficiency.
- Determine technical facts from evidence. Recommend and ask confirmation for
  naming, an unproven version, and software-purpose wording. Require the user
  to provide rights, applicant, development, and real publication/date facts.
- Ask in ordinary language about real-world facts, not registration field names.
  Batch only the unresolved questions after investigation; do not conduct a
  form-like interrogation at the beginning.
- A significant function may enter a draft only when it has a matching entry in
  `evidence-map.json`. Remove unsupported claims during review.
- Use `software-profile.yaml` only after facts are locked as the sole source for
  software name, short name, version, applicant, dates, and features.
- Do not create or alter official application forms. Produce filling guidance.
  Do not promise approval. Escalate shared rights, assignment, inheritance,
  commissioned development, modification of another's software, and exception
  deposit to human review.

## Routes

### Create materials

For requests such as "帮我给这个项目做软著", begin quietly: inspect the
project, then show a short plain-language progress summary. Create a new output
directory outside the project and run:

```bash
python3 scripts/manage_task.py init /path/to/project /path/out
python3 scripts/scan_project.py /path/to/project --output /path/out/project-analysis.json
python3 scripts/build_evidence_map.py /path/to/project --output /path/out/evidence-map.json
```

Copy `assets/templates/software-profile.yaml` to `/path/out/software-profile.yaml`.
Fill every field with `value`, `source`, `confidence`, and
`requires_confirmation`. Record automatic facts with project paths; record
recommendations as requiring confirmation. Do more investigation before asking
for unknown facts.

Then give one concise confirmation panel in Chinese: proposed name/version and
purpose, plus only genuinely user-only facts. Explain choices in ordinary
language (for example, ask who developed the software and whether it has
actually been made available publicly). On confirmation, record it in
`user-confirmations.json`, set the relevant fields to `confirmed`, validate,
and lock facts:

```bash
python3 scripts/validate_profile.py /path/out/software-profile.yaml --output /path/out/profile-validation.json
python3 scripts/manage_task.py lock /path/out --profile /path/out/software-profile.yaml
```

Only after a successful lock, generate drafts from that profile, move the task
to `GENERATING`, and include only evidence-backed features. Run source selection
and security checks on generated copies, never on a modified original project.

### Check materials

For requests to inspect materials or identify gaps, initialize or resume the
task, scan the project and evidence, then run the Reviewer route below. Explain
findings as clear blockers, warnings, and next actions, rather than internal
script or rule names unless requested.

### Continue or regenerate

For requests such as "继续刚才的软著", locate the prior independent output
directory and run `python3 scripts/manage_task.py status /path/out`. The script
compares the project snapshot. If unchanged, continue from the recorded stage;
do not repeat answered questions. If changed, return to analysis and identify
which facts/evidence require confirmation again. A renamed product or amended
confirmed fact invalidates the lock and requires a fresh confirmation before
regeneration.

## Reviewer gate

After generation, set the task to `REVIEWING` and independently review it as a
software copyright materials reviewer. Check: (1) each documented feature has
project evidence, (2) identity, applicant, dates, technology, and feature names
match the locked profile, (3) applicable material rules are met, and (4)
generated copies contain no unaddressed sensitive data. Run:

```bash
python3 scripts/review_materials.py /path/out/software-profile.yaml /path/out/evidence-map.json /path/out/materials --task-dir /path/out --output /path/out/review-report.json
python3 scripts/validate_output.py /path/out/profile-validation.json /path/out/review-report.json --output /path/out/final-validation.json
```

When the review finds a fixable unsupported claim, search again, remove it if
still unsupported, regenerate the affected section, and review again. Ask the
user only when a real-world fact remains unresolved. Mark `READY` only when no
blocker remains; otherwise keep `NEEDS_FIX` or `WAITING_FOR_CONFIRMATION`.

## State and user progress

The only internal states are `ANALYZING`, `WAITING_FOR_CONFIRMATION`,
`FACTS_LOCKED`, `GENERATING`, `REVIEWING`, `NEEDS_FIX`, and `READY`. Preserve
`workflow-state.json`, `software-profile.yaml`, `evidence-map.json`, and
`user-confirmations.json` in the output directory. Report simple progress such
as "已识别项目结构" and "还有 2 项需要确认", not internal implementation
details.

## References

Read [scope and principles](references/00-scope-and-principles.md) for every
request. Read [evidence rules](references/02-evidence-rules.md) while deriving
features, [official rules](references/01-official-rules.md) before final
material preparation, and the relevant document, application, source, security,
consistency, and exception rules before their respective work.
