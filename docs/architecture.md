# Architecture

`software-profile.yaml` is the canonical record of names, version, confirmed
application facts, detected technology, and evidence-backed features. Every
generated material reads it rather than deciding software facts independently.

```text
project -> scan -> evidence map -> software profile -> materials -> validation
```

Scripts are read-only with respect to the input project. They write only to a
user-selected output directory.
