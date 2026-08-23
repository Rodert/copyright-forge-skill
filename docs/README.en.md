# Copyright Forge Skill

> Evidence-backed draft materials for Chinese software copyright registration.

[简体中文](../README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Français](README.fr.md)

Copyright Forge is an AI Agent Skill that prepares draft registration materials
from a real software project. It maps claims to project evidence, keeps one
canonical software profile, and helps prepare documentation, source-code
identification materials, and application-field guidance.

## Give This to Your Agent

```text
Install and use Copyright Forge Skill from https://github.com/Rodert/copyright-forge-skill.

Read skills/copyright-forge/SKILL.md, then prepare draft Chinese software copyright registration materials from my real project.

Before the first material-preparation request each day, check the Skill's upstream Git update. If a clean checkout has an update, fast-forward before continuing. Stay silent when current; if checking or updating fails, or local changes block the update, explain the reason and do not prepare materials. Never overwrite local changes.

Use only real project evidence and facts I confirm. Never invent functionality, source code, screenshots, ownership, development relationships, publication facts, or dates. Do not alter my project, recreate an official form, or promise registration approval. Write outputs to a separate directory outside the project and flag every fact requiring my confirmation.
```

## What It Provides

- Project scanning for Go, Java, Python, Node.js, Vue, and React.
- Evidence mapping from candidate features to code, routes, models, or pages.
- A single `software-profile.yaml` for names, version, and confirmed facts.
- Deterministic source manifests for ordinary deposit preparation.
- Secret detection and redaction in generated copies only.
- Profile, consistency, and final-status validation reports.

## Trust Boundaries

Copyright Forge does not submit applications, determine legal facts, alter
official forms, change the analyzed project, or guarantee approval. It supports
ordinary deposit in the current release. Exceptional deposit and complex rights
cases require manual review and current official guidance.

## Use

The Skill entrypoint is [skills/copyright-forge/SKILL.md](../skills/copyright-forge/SKILL.md).
See the [Chinese README](../README.md) for command-line examples, architecture,
and supported-project details.

## License

Apache-2.0. See [LICENSE](../LICENSE).
