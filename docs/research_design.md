# Research design and methodological boundaries

## Purpose
This is an independent, synthetic-data demonstration of the data construction required for a Finland–Sweden farm succession study. It is not a policy impact evaluation and has no real individual or farm records.

## Research workflow
1. Generate fictional farm metadata and annual owner histories for 2000–2023.
2. Sort records by farm and year; detect an owner change relative to the prior observed year.
3. Flag year gaps, which make precise succession timing uncertain in real data.
4. Join owner changes to a synthetic transfer registry with declared transfer type and family relationship.
5. Audit detected transfers against registry records and enforce farm-year and transfer-event key integrity.
6. Link events to longitudinal investment and productivity outcomes; generate relative event-time indicators.
7. Summarize trends and estimate a descriptive farm/year fixed-effects association using clustered standard errors.

## Identification
The outcome model compares years before and after a simulated transfer with farm and calendar-year effects. It does **not** identify the causal effect of succession: transfers are not randomly assigned; selection, anticipation, time-varying confounding, and endogenous timing remain possible.

Sweden abolished inheritance and gift taxes in 2005, while Finland retained a different framework. This institutional contrast alone does **not** establish parallel trends or a valid difference-in-differences identification strategy. Additional pre-policy observations, valid controls, relevant risk sets, exposure definitions, and institutional details would be needed.

## Linking limitations
- The demonstration creates at most one ownership transition per farm. Transfer modes and family indicators are recorded once per simulated event and used consistently in the synthetic outcomes and registry.
- Annual observation gives only yearly event dates.
- Transfer types and family relations come from an explicitly synthetic registry, not surnames or guessed kinship.
- Missing records, ownership shares, co-ownership, parcel ownership, identifier re-use, and farm restructuring require additional work before administrative-data application.
- The illustrative file-level registry is regenerated alongside the synthetic ownership histories.

## Roadmap for credible evidence
- Obtain legally accessible real datasets, documenting source, license, unit, definitions and extraction date.
- Understand Finnish and Swedish tax treatment, relief rules, registration and transfer mechanisms.
- Design clean controls and event cohorts, examine pre-trends and anticipation, and report uncertainty.
- Add administrative-data linkage quality checks, privacy safeguards and access constraints.
- Validate conclusions against real sources before publication.

## Reproducibility
Run `python src/pipeline.py` then `python -m pytest -q` from the repository root.
