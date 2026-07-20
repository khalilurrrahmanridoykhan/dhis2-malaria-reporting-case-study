# Indicator reference

All indicators must explicitly distinguish missing data from reported zero. Indicator expressions below use descriptive codes; the configured DHIS2 version will replace them with stable UIDs.

| Indicator | Numerator | Denominator | Factor | Interpretation |
|---|---|---|---:|---|
| Malaria test positivity rate | Confirmed cases | RDT tests + microscopy tests | 100 | Confirmed positive tests per 100 tests |
| Confirmed malaria incidence | Confirmed cases | Estimated population | 1,000 | Confirmed cases per 1,000 population |
| Malaria case fatality rate | Malaria deaths | Confirmed cases | 100 | Deaths per 100 confirmed cases |
| Treatment coverage | Confirmed cases treated | Confirmed cases | 100 | Confirmed cases treated, as a percentage |
| Reporting completeness | Reports received | Reports expected | 100 | Expected monthly reports received |
| P. falciparum proportion | P. falciparum cases | Confirmed cases | 100 | Confirmed cases classified as P. falciparum |
| Imported-case proportion | Imported cases | Confirmed cases | 100 | Confirmed cases classified as imported |
| Severe-malaria proportion | Severe cases | Confirmed cases | 100 | Confirmed cases classified as severe |

## Expression design notes

- Suppress ratios when the denominator is missing or zero; do not silently replace them with zero.
- Use indicator types with the correct factor (`100` or `1000`).
- Confirm whether `tests_rdt + tests_microscopy` represents people tested or tests performed before operational use.
- Reconcile duplicate testing if a person may receive both diagnostic methods.
- Use relative periods such as “last 12 months” in dashboard favorites.
- Review all definitions with the epidemiology and programme teams before configuration.

