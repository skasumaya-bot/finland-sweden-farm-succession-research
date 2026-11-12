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
