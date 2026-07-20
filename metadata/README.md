# Metadata status

`configuration-blueprint.json` is a human-readable design manifest, **not an importable DHIS2 metadata package**.

DHIS2 metadata schemas and dependency fields can vary by version. The final `malaria-aggregate-metadata.json` must be produced by configuring and testing the design in a blank DHIS2 instance, then using a dependency-aware export.

Before publishing a real export, record:

- DHIS2 version tested
- Export date
- Import strategy and atomic mode
- Validation/dry-run result
- Fresh-instance import result
- Analytics generation result
- Any expected conflicts or manual post-import steps

Never place credentials, API tokens, production URLs, real users, or operational metadata in this directory.

