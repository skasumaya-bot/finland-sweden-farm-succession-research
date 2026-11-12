# Farm Succession and Ownership Transitions: Finland–Sweden Research Demonstration

**Independent methodological portfolio using 100% synthetic microdata.** Not an analysis of actual Finnish or Swedish farm owners, an official tax-policy evaluation, or a completed causal study. Not affiliated with the University of Helsinki or its advertised research project.

This reproducible Python project demonstrates how longitudinal ownership histories can be processed to identify farm transfers, classify transfer modes, link transfer events to farm economic outcomes, audit data integrity, and estimate illustrative farm and year fixed-effects models with farm-clustered standard errors.

## Research question
How can longitudinal ownership registers be processed to identify farm transfers, classify transfer types, link succession to farm outcomes, and prepare credible comparative econometric analyses?

## Project contents
- `src/pipeline.py` — reproducible Python pipeline
- `tests/test_pipeline.py` — integrity and reproducibility tests
- `data/` — created by running the pipeline: synthetic farm, ownership, transfer, and economic outcome records
- `outputs/` — created by running the pipeline: linked panel, audit, summaries and visualization
- `docs/research_design.md` — design, assumptions and limitations
- `docs/data_dictionary.md` — variable definitions
- `results/` — locally validated sample summary, regression summary, and validation report
- `.github/workflows/validate.yml` — automated tests and generated data/output artifacts

## Reproduce
```bash
python -m pip install -r requirements.txt
python src/pipeline.py
python -m pytest -q
```

## Validated demonstration

The default seeded run produces **800 synthetic farms**, **19,200 farm-years**, and **533 detected and matched transfers**. Four local tests passed. The post-transfer fixed-effects coefficient is **1.0418 percentage points** (clustered SE **0.0347**), which describes only the simulated observations. See [`results/validation_report.md`](results/validation_report.md) for the audit and methodological qualifications.

The full generated datasets and figures are created by running the pipeline and are not committed as source data. A GitHub Actions workflow is configured to generate them as downloadable run artifacts.

## Research integrity and limitations
The data are simulated and **cannot** establish the effects of inheritance taxation or describe real farms. Sweden’s 2005 inheritance-tax abolition is not automatically a valid difference-in-differences design. Any causal study requires defensible counterfactuals, adequate before/after exposure, institutional validity, anticipation checks, and appropriate data access.

## Planned extensions
Real openly licensed aggregate data from Finnish and Swedish statistical providers; privacy-aware administrative-data schemas; multiple owner changes and co-ownership; suitable event-study and placebo diagnostics; and a research paper grounded in real evidence.
