import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pipeline import generate, detect, link

def test_generated_panel_is_balanced():
    farms, owners, events, panel = generate(seed=42, n_farms=30)
    assert len(panel) == 30 * 24
    assert not panel.duplicated(["farm_id", "year"]).any()

def test_ownership_events_match_registry():
    farms, owners, events, panel = generate(seed=42, n_farms=30)
    detected = detect(owners)
    linked, audit = link(panel, events, detected)
    assert (audit["_merge"] == "both").all()
    assert len(linked) == 30 * 24


def test_transfer_registry_matches_owner_history_and_simulation():
    farms, owners, events, panel = generate(seed=17, n_farms=120)
    changes = detect(owners)
    assert len(events) == len(changes)
    assert set(zip(events.farm_id, events.transfer_year)) == set(zip(changes.farm_id, changes.detected_transfer_year))
    assert events.family_transfer.isin([0, 1]).all()
    assert events.loc[events.transfer_mode.isin(["inheritance", "gift"]), "family_transfer"].eq(1).all()
    assert not events.duplicated(["farm_id", "transfer_year"]).any()


def test_reproducibility():
    _, owners1, events1, panel1 = generate(seed=99, n_farms=15)
    _, owners2, events2, panel2 = generate(seed=99, n_farms=15)
    import pandas as pd
    pd.testing.assert_frame_equal(owners1, owners2)
    pd.testing.assert_frame_equal(events1, events2)
    pd.testing.assert_frame_equal(panel1, panel2)
