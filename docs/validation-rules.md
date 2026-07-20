# Validation and data-quality rules

## Blocking data-entry checks

| Code | Left expression | Operator | Right expression | Message |
|---|---|---|---|---|
| VR01 | Confirmed cases | <= | RDT tests + microscopy tests | Confirmed cases cannot exceed total tests |
| VR02 | Malaria deaths | <= | Confirmed cases | Deaths cannot exceed confirmed cases |
| VR03 | Severe cases | <= | Confirmed cases | Severe cases cannot exceed confirmed cases |
| VR04 | Confirmed cases treated | <= | Confirmed cases | Treated cases cannot exceed confirmed cases without review |
| VR05 | Pf + Pv + mixed cases | == | Confirmed cases | Species classifications must reconcile with confirmed cases |
| VR06 | Indigenous + imported cases | == | Confirmed cases | Case-origin classifications must reconcile with confirmed cases |
| VR07 | Reports received | <= | Reports expected | Received reports cannot exceed expected reports |
| VR08 | Stock-out days | <= | Days in reporting month | Stock-out days exceed the reporting period |

## Review flags

These should produce a warning or appear in a quality dashboard rather than automatically reject a report:

- Confirmed cases increase by more than 100% from the preceding month.
- Test positivity exceeds a locally approved threshold.
- Stock-out days are greater than zero.
- Reporting completeness falls below 90%.
- A facility reports zero tests for two consecutive months.
- Confirmed cases are present but estimated population is missing.

Unusual does not necessarily mean incorrect. Each warning requires contextual review.

