# Architecture

`software-profile.yaml` is the canonical record of resolved names, version,
confirmed application facts, detected technology, and approved feature IDs.
Every generated material reads it rather than deciding software facts
independently. Each resolved field records its source, confidence, and whether
human confirmation was required.

```text
project -> adapter scan -> evidence map -> feature graph -> confirmation -> facts lock -> materials -> eight quality gates
```

`workflow-state.json` records the sole workflow states: `ANALYZING`,
`WAITING_FOR_CONFIRMATION`, `FACTS_LOCKED`, `GENERATING`, `REVIEWING`,
`NEEDS_FIX`, and `READY`. It also stores a project snapshot and the fingerprint
of the locked profile, so a resumed task cannot silently reuse stale evidence
or changed facts.

Scripts are read-only with respect to the input project. They write only to a
user-selected output directory.

`SKILL.md` is deliberately a thin router. The detailed create, review, resume,
correction, and rules-update workflows live under `prompts/`. The rules registry
records authority, source URL, classification, applicability, and verification
date; the rules radar produces only a human-reviewable change report.
