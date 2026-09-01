# Rules Update Check

Read `references/official/source-registry.yaml` and perform a best-effort check
of its official sources when network access is available. Produce a dated
change proposal with the retrieved evidence, affected rule IDs, and a semantic
diff against local rules. Do not edit rules, templates, or core workflow files
automatically. A human must review and approve every proposed rule update.
