"""Reproducible, entirely synthetic farm succession demonstration."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"

def generate(seed=42, n_farms=800):
    rng = np.random.default_rng(seed)
    years = np.arange(2000, 2024)
    farms = pd.DataFrame({
        "farm_id": np.arange(1, n_farms + 1),
        "country": rng.choice(["Finland", "Sweden"], n_farms),
        "region": rng.choice(["North", "South", "East", "West"], n_farms),
        "hectares": rng.lognormal(3.7, .6, n_farms).round(1)
    })
    records = []
    histories = []
    transfer_details = {}
    for f in farms.itertuples(index=False):
        transfer_year = int(rng.integers(2005, 2020)) if rng.random() < .68 else None
        mode = rng.choice(["inheritance", "gift", "market_sale", "other"], p=[.30, .22, .40, .08]) if transfer_year else None
        family = bool(mode in ("inheritance", "gift") or (mode == "market_sale" and rng.random() < .16)) if mode else False
        if transfer_year is not None:
            transfer_details[f.farm_id] = (transfer_year, mode, int(family))
        old = f"P{f.farm_id:05d}A"
        new = f"P{f.farm_id:05d}B"
        farm_effect = rng.normal(0, 1.7)
        for y in years:
            after = transfer_year is not None and y >= transfer_year
            owner = new if after else old
            policy = (f.country == "Sweden" and y >= 2005)
            investment = 8 + farm_effect + .012 * f.hectares + .045 * (y - 2000) + (.9 if after else 0) + (.35 if after and family else 0) + rng.normal(0, 1.3)
            productivity = 70 + .25 * f.hectares + .5 * (y - 2000) + (2 if after else 0) + rng.normal(0, 7)
            records.append((f.farm_id, f.country, f.region, y, f.hectares, owner, investment, productivity, int(policy)))
            histories.append((f.farm_id, y, owner, "owner_register_simulated"))
    panel = pd.DataFrame(records, columns=["farm_id", "country", "region", "year", "hectares", "owner_id", "investment_rate_pct", "productivity_index", "sweden_post_2005"])
    ownership = pd.DataFrame(histories, columns=["farm_id", "year", "owner_id", "source"])
    events = pd.DataFrame(
        [(farm_id, year, mode, family) for farm_id, (year, mode, family) in transfer_details.items()],
        columns=["farm_id", "transfer_year", "transfer_mode", "family_transfer"],
    )
    events["classification_source"] = "synthetic_transfer_registry"
    DATA.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    farms.to_csv(DATA / "farms.csv", index=False)
    ownership.to_csv(DATA / "ownership_history.csv", index=False)
    events.to_csv(DATA / "transfer_registry.csv", index=False)
    panel.drop(columns=["owner_id"]).to_csv(DATA / "farm_outcomes.csv", index=False)
    return farms, ownership, events, panel

def detect(ownership):
    x = ownership.sort_values(["farm_id", "year"]).copy()
    x["previous_owner"] = x.groupby("farm_id").owner_id.shift()
    x["previous_year"] = x.groupby("farm_id").year.shift()
    x["changed"] = x.previous_owner.notna() & x.owner_id.ne(x.previous_owner)
    x["gap_in_history"] = x.previous_year.notna() & x.year.sub(x.previous_year).ne(1)
    return x.loc[x.changed, ["farm_id", "year", "previous_owner", "owner_id", "gap_in_history"]].rename(columns={"year": "detected_transfer_year"})

def link(panel, events, detected):
    assert not panel.duplicated(["farm_id", "year"]).any()
    assert not events.duplicated(["farm_id", "transfer_year"]).any()
    joined = panel.merge(events, on="farm_id", how="left", validate="many_to_one", indicator=True)
    joined["event_time"] = joined.year - joined.transfer_year
    joined["post_transfer"] = ((joined.event_time >= 0) & joined.transfer_year.notna()).astype(int)
    joined["treated_ever"] = joined.transfer_year.notna().astype(int)
    audit = detected.merge(events, left_on=["farm_id", "detected_transfer_year"], right_on=["farm_id", "transfer_year"], how="outer", indicator=True)
    audit.to_csv(OUT / "transfer_linkage_audit.csv", index=False)
    joined.drop(columns=["_merge"]).to_csv(OUT / "analysis_panel.csv", index=False)
    return joined, audit

def analyze(df):
    summary = df.groupby(["country", "year"], as_index=False).agg(mean_investment=("investment_rate_pct", "mean"), farms=("farm_id", "nunique"))
    summary.to_csv(OUT / "country_year_summary.csv", index=False)
    counts = df.groupby("country", as_index=False).agg(farms=("farm_id", "nunique"))
    transferred = df.loc[df.treated_ever.eq(1)].groupby("country").farm_id.nunique()
    counts["transferred"] = counts.country.map(transferred).fillna(0).astype(int)
    counts.to_csv(OUT / "sample_summary.csv", index=False)
    try:
        import statsmodels.formula.api as smf
        model = smf.ols("investment_rate_pct ~ post_transfer + C(farm_id) + C(year)", data=df).fit(cov_type="cluster", cov_kwds={"groups": df.farm_id})
        (OUT / "model_summary.txt").write_text(
            f'POST_TRANSFER coefficient: {model.params["post_transfer"]:.4f}\n'
            f'Clustered SE: {model.bse["post_transfer"]:.4f}\n'
            f'P-value: {model.pvalues["post_transfer"]:.5f}\n'
            f'N: {int(model.nobs)}\n'
            'Interpretation: descriptive association only; timing may be endogenous.\n'
        )
    except ImportError:
        (OUT / "model_summary.txt").write_text("Install statsmodels to estimate fixed-effects regression.\n")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for country, group in summary.groupby("country"):
        ax.plot(group.year, group.mean_investment, label=country)
    ax.set(xlabel="Year", ylabel="Mean investment rate (%)", title="Synthetic farm investment by country")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "investment_trends.png", dpi=160)
    plt.close(fig)
    return counts

if __name__ == "__main__":
    farms, ownership, events, panel = generate()
    detected = detect(ownership)
    linked, audit = link(panel, events, detected)
    analyze(linked)
    print(f"Generated {len(linked)} farm-years; {len(events)} transfer events; linkage audit: {audit._merge.value_counts().to_dict()}")
