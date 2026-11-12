# Validation of synthetic farm succession pipeline

The default demonstration uses a seeded simulation (seed 42) with 800 fictional farms and 24 annual observations per farm (2000–2023).

## Results from local validation
- Farms: 800 (Finland: 394; Sweden: 406)
- Farm-years: 19,200
- Detected and registered transfer events: 533
- Transfer records matched in the linkage audit: 533
- Left-only and right-only linkage discrepancies: 0
- Automated Python tests: 4 passed (local validation)

## Descriptive regression
A farm-and-year fixed-effects model of simulated investment rates on a post-succession indicator, estimated with farm-clustered standard errors, yielded:

- Post-transfer coefficient: 1.0418 percentage points
- Clustered standard error: 0.0347
- Observations: 19,200

This coefficient describes **only the synthetic dataset**. Simulated transfer timing and economic outcomes are built into the example; the estimate is not a causal effect of actual succession, inheritance taxation, or Sweden's 2005 reforms.

## Reproduction
```bash
python -m pip install -r requirements.txt
python -m pytest -q
python src/pipeline.py
```

The script generates the full synthetic CSV tables and the investment figure into `data/` and `outputs/`. Those files are intentionally not versioned in the repository. A GitHub Actions workflow is configured to validate the pipeline and attach generated files to completed workflow runs.

This report records local validation; it does not itself certify that a GitHub-hosted workflow run has succeeded.
