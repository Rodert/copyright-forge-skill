---
name: copyright-forge
description: Prepare and validate draft materials for Chinese software copyright registration from a real software project. Use for Chinese soft copyright, software copyright registration, source-code identification materials, or related documentation; do not use to submit an application or decide legal ownership.
---

# Copyright Forge

Prepare evidence-backed draft materials for a Chinese software copyright
registration. Work from the user's real project and keep the original project
unchanged.

## Update check

Before the first material-preparation request of each local calendar day, check
this Skill's upstream Git remote for updates. Resolve `SKILL_DIR` as the
directory containing this `SKILL.md`, then resolve `REPO_DIR` from that
directory's Git worktree. Store the last successful check date in
`${XDG_CONFIG_HOME:-$HOME/.config}/copyright-forge/update-check-date`. If it
already contains today's local date, skip the remote check and continue
silently.

When `origin/main` is ahead, briefly tell the user that an update was found.
If the worktree is clean, fast-forward to the update and re-read this
`SKILL.md` before preparing materials. If local changes prevent the update, do
not prepare materials: state that the update is blocked and local changes must
be resolved first. Never overwrite local changes. If the Skill is not a Git
checkout, has no `origin`, or the check or update fails, state that update
status could not be verified and do not prepare materials. A normal up-to-date
check remains silent.

```bash
SKILL_DIR="${SKILL_DIR:?Set SKILL_DIR to the directory containing SKILL.md}"
REPO_DIR="$(git -C "$SKILL_DIR" rev-parse --show-toplevel 2>/dev/null)" || {
  echo "Copyright Forge update check unavailable; material preparation not started." >&2
  exit 1
}
UPDATE_STAMP="${XDG_CONFIG_HOME:-$HOME/.config}/copyright-forge/update-check-date"
TODAY="$(date +%Y-%m-%d)"

if [ ! -r "$UPDATE_STAMP" ] || [ "$(cat "$UPDATE_STAMP" 2>/dev/null)" != "$TODAY" ]; then
  if ! git -C "$REPO_DIR" remote get-url origin >/dev/null 2>&1; then
    echo "Copyright Forge update check unavailable; material preparation not started." >&2
    exit 1
  fi
  if ! git -C "$REPO_DIR" fetch --quiet origin; then
    echo "Copyright Forge update check failed; material preparation not started." >&2
    exit 1
  fi
  if [ "$(git -C "$REPO_DIR" rev-list --count HEAD..origin/main)" -gt 0 ]; then
    if [ -n "$(git -C "$REPO_DIR" status --porcelain)" ]; then
      echo "Copyright Forge update is blocked by local changes; material preparation not started." >&2
      exit 1
    fi
    echo "Copyright Forge update found; applying it before material preparation." >&2
    git -C "$REPO_DIR" pull --ff-only origin main || exit 1
  fi
  mkdir -p "$(dirname "$UPDATE_STAMP")"
  printf '%s\n' "$TODAY" > "$UPDATE_STAMP"
fi
```

## Non-negotiable boundaries

- Never invent functions, source code, screenshots, ownership, development
  relationships, publication facts, or confirmed dates.
- Treat owner, development method, rights acquisition, publication status, and
  first-publication date as user-only facts. A git date can only be a suggestion
  requiring confirmation.
- Do not create or alter an official application form. Produce filling guidance
  instead.
- Redact credentials only in generated copies; report every redaction.
- Do not mark materials `READY` while a blocker remains. Do not promise that
  registration will be approved.

## Workflow

1. Scan the project with `scripts/scan_project.py` and create an evidence map
   with `scripts/build_evidence_map.py`.
2. Create one profile from `assets/templates/software-profile.yaml`; confirm all
   user-only facts before finalization. Validate it with `validate_profile.py`.
3. Choose documentation appropriate to the product: user manual for UI software,
   function/design documentation for APIs or services, and operation guidance for
   CLI software. Write only evidence-backed sections. Use real screenshots only.
4. Build a deterministic source manifest with `collect_source.py`; redact the
   generated copy with `detect_secrets.py` if needed. Read the source rules
   before preparing ordinary-deposit material.
5. Generate application-form filling guidance, not an official form. Use the
   profile's name and version verbatim in every deliverable.
6. Run consistency and output validation. Report `DRAFT`,
   `NEEDS_CONFIRMATION`, `VALIDATED`, or `READY` with blockers, warnings, and
   information items.

## References

- Read [scope and principles](references/00-scope-and-principles.md) for all
  requests.
- Read [official rules](references/01-official-rules.md) before final material
  preparation; check the official channel again before submission.
- Read [evidence rules](references/02-evidence-rules.md) when deriving features.
- Read [source-code rules](references/05-source-code-rules.md) before source
  selection and [security rules](references/09-security-and-redaction-rules.md)
  before sharing generated copies.
- Read [document rules](references/06-document-rules.md) and
  [application-field rules](references/07-application-field-rules.md) when
  generating their respective drafts.
- Read [advanced-case rules](references/12-exception-deposit-rules.md) whenever
  an exception, shared rights, assignment, inheritance, or modification is
  indicated.
