# Implementation guide

## 1. Use an isolated environment

Configure this project only in a blank or disposable DHIS2 test instance. Record the exact DHIS2 version and database backup before importing metadata. Never test against an operational national or partner instance.

## 2. Create metadata in dependency order

1. Organisation-unit levels and fictional organisation units
2. Indicator types
3. Category options, categories, and category combinations
4. Data elements and data-element groups
5. Monthly dataset and dataset sections
6. Validation rules and validation-rule group
7. Indicators and indicator group
8. Visualizations, maps, and dashboard
9. User groups, sharing, and dataset assignment

## 3. Configure the dataset

- Name: `Monthly Malaria Facility Report — DEMO`
- Period type: Monthly
- Completion: required after validation
- Entry level: facility
- Sections: case detection; laboratory testing; confirmed cases; treatment and outcomes; commodities; reporting performance
- Expiry/late-entry settings: document the selected operational policy

## 4. Configure access

| Role | Metadata | Data capture | Data view | Approval |
|---|---|---|---|---|
| Demo facility entry | View | Assigned facilities | Assigned facilities | No |
| Demo district reviewer | View | Optional correction | District subtree | Review/approve |
| Demo national analyst | View | No | National aggregate | No |
| Demo administrator | Manage | Manage | Manage | Manage |

Do not export real users, credentials, API tokens, or operational sharing references.

## 5. Validate before importing

- Confirm that every UID is exactly 11 alphanumeric characters and begins with a letter.
- Check code, name, short-name, and UID collisions.
- Run a metadata validation/dry run before committing.
- Read the complete import report; an HTTP success response is not enough.
- Import metadata before data values.
- Run analytics tables after importing synthetic data.

## 6. Acceptance tests

- A facility user can see only assigned fictional facilities.
- Every dataset section renders correctly.
- Valid zero values can be entered and are distinguishable from missing values.
- Each blocking validation rule fails with its expected test record.
- Dataset completion and review follow the documented workflow.
- Indicators match independent spreadsheet calculations.
- Relative-period dashboard items update after analytics processing.
- Aggregate values roll up correctly across the hierarchy.

## 7. Produce a publishable export

After successful testing, use DHIS2's dependency-aware metadata export for the configured dataset and dashboard. Export sharing only when intentionally designed; otherwise omit instance-specific sharing. Then:

1. Search for and remove server URLs, usernames, emails, tokens, and operational identifiers.
2. Confirm that all organisation units and values are fictional.
3. Store the exact DHIS2 version in `metadata/README.md`.
4. Save the dry-run/import report alongside the export.
5. Re-import into a fresh test instance and repeat acceptance tests.

