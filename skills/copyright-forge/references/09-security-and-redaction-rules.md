# Security and Redaction Rules

Scan generated source copies for `.env` content, API keys, access keys, private
keys, passwords, tokens, connection strings, personal identifiers, internal
hosts, and customer data. Redact a matching value as `[REDACTED]`; preserve the
file path, line number, match type, and reason in a separate report.

Secret detection is heuristic. Treat a clean report as a review aid, not proof
that no sensitive information remains.
