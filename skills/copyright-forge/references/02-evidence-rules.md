# Evidence Rules

Use evidence in this order: user-provided information, project README/docs,
source code, routes/APIs, database schema, front-end pages, configuration, git
history, then AI inference. AI inference alone cannot establish a feature.

`owner`, `development_method`, `rights_acquisition`, `completion_date`,
`publication_status`, and `first_publication_date` are not inferable facts. Git
history may suggest a date, but must be labeled `requires_confirmation`.

Feature evidence should cite paths and types. A feature with no source, route,
model, page, or user-provided evidence must not enter the documentation.
