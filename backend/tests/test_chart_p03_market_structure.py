"""CHART-P03 fail-first tests: Market Structure detections (geometric, M7/M8)
+ annotation update/delete verbs for drawing tools (S1).

Every test here MUST fail against the pre-CHART-P03 tree (the module, the
registry entries, the engine, the PATCH/DELETE endpoints do not exist) and
pass once the phase ships. Every numeric fixture is verifiable by inspection;
every declared rule is stated in the test docstring exactly as the
implementation declares it.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.services.indicator_registry import INDICATOR_REGISTRY
from app.services.market_structure import (
    STRUCTURE_DISCLOSURE,
    bos,
    choch,
    fvg,
    order_block_pattern,
    struct,
    swings,
)

EPS = 1e-9


def _bars(
    closes: list[float],
    highs: list[float] | None = None,
    lows: list[float] | None = None,
    opens: list[float] | None = None,
    start: datetime | None = None,
) -> list[dict]:
    base = start or datetime(2026, 8, 17, 9, 0, tzinfo=timezone.utc)
    highs = highs if highs is not None else [c + 0.5 for c in closes]
    lows = lows if lows is not None else [c - 0.5 for c in closes]
    opens = opens if opens is not None else list(closes)
    return [
        {
            "open_time": base + timedelta(minutes=i),
            "open": opens[i],
            "high": highs[i],
            "low": lows[i],
            "close": closes[i],
        }
        for i in range(len(closes))
    ]


def _line(out, name: str) -> list[float | None]:
    pts = (out.lines or {})[name]
    return [None if p.value is None else float(p.value) for p in pts]


# --- Swings ----------------------------------------------------------------

def test_chart_p03_swings_matches_hand_computed_values() -> None:
    """Rule declared: strict lookback/lookforward k=5 — bar i is a swing HIGH
    iff high[i] > high[j] for ALL j in [i-5, i+5], j != i (and symmetric for
    lows). The last k bars cannot be confirmed and emit nothing."""
    n = 15
    closes = [10.0] * n
    highs = [10.0] * n
    lows = [5.0] * n
    highs[7] = 20.0  # single peak, full 5/5 window (indices 2..12)
    bars = _bars(closes, highs=highs, lows=lows)
    out = swings(bars, k=5)
    assert out.kind == "computed"
    sh = _line(out, "swing_high")
    sl = _line(out, "swing_low")
    assert sh[7] == 20.0
    assert all(v is None for i, v in enumerate(sh) if i != 7)
    assert all(v is None for v in sl)  # flat lows: no swing low


def test_chart_p03_swing_required_bars() -> None:
    assert swings(_bars([1.0] * 10), k=5).kind == "insufficient"
    assert swings(_bars([1.0] * 10), k=5).required == 11


# --- HH/HL/LH/LL -----------------------------------------------------------

def test_chart_p03_struct_hh_lh_hl_ll_matches_hand_computed_values() -> None:
    """Rule declared: classify each confirmed swing against the previous swing
    of the SAME kind: swing high > previous swing high -> HH else LH; swing
    low > previous swing low -> HL else LL. First of each kind is unclassified
    (None). Required = 5k+4 (four confirmed swings at worst-case spacing)."""
    n = 40
    closes = [10.0] * n
    highs = [10.0] * n
    lows = [5.0] * n
    highs[5] = 12.0   # swing high 1 (window 0..10)
    highs[15] = 16.0  # swing high 2, higher -> HH (window 10..20)
    bars = _bars(closes, highs=highs, lows=lows)
    out = struct(bars, k=5)
    assert out.kind == "computed"
    hh = _line(out, "hh")
    assert hh[5] is None and hh[15] == 16.0
    lh = _line(out, "lh")
    assert lh[5] is None and lh[15] is None

    # Second case: falling peaks -> LH.
    highs2 = [10.0] * n
    highs2[5] = 16.0
    highs2[15] = 12.0
    out2 = struct(_bars(closes, highs=highs2, lows=lows), k=5)
    lh2 = _line(out2, "lh")
    assert lh2[15] == 12.0
    assert _line(out2, "hh")[15] is None


# --- BOS -------------------------------------------------------------------

def test_chart_p03_bos_matches_hand_computed_values() -> None:
    """Rule declared: BOS-up emits at bar i when close[i] STRICTLY exceeds the
    most recent confirmed swing-high level (the swing's own bar cannot break
    itself: close <= high there). BOS-down symmetric on swing lows. Value =
    the broken level. Required = 2k+2 (confirmed swing + one break bar)."""
    n = 14
    closes = [9.0] * n
    closes[11] = 13.0
    highs = [10.0] * n
    highs[5] = 12.0  # swing high, window 0..10, confirmed at bar 10
    lows = [5.0] * n
    bars = _bars(closes, highs=highs, lows=lows)
    out = bos(bars, k=5)
    assert out.kind == "computed"
    up = _line(out, "bos_up")
    assert up[11] == 12.0  # close 13 > 12 at bar 11
    assert all(v is None for i, v in enumerate(up) if i != 11)
    assert all(v is None for v in _line(out, "bos_down"))


# --- CHoCH -----------------------------------------------------------------

def test_chart_p03_choch_matches_hand_computed_values() -> None:
    """Rule declared: the FIRST BOS whose direction differs from the previous
    BOS is a CHoCH, emitted at that bar with the broken level. Required = 24
    (two BOS breaks)."""
    n = 24
    closes = [9.0] * n
    highs = [10.0] * n
    lows = [5.0] * n
    highs[5] = 12.0     # swing high (window 0..10)
    closes[11] = 13.0   # BOS UP at 11 (close 13 > 12)
    lows[13] = 4.0      # swing low (window 8..18), confirmed at 18
    closes[20] = 3.0    # BOS DOWN at 20 (close 3 < 4) -> first flip -> CHoCH
    bars = _bars(closes, highs=highs, lows=lows)
    out = choch(bars, k=5)
    assert out.kind == "computed"
    cd = _line(out, "choch_down")
    cu = _line(out, "choch_up")
    assert cd[20] == 4.0  # broken swing-low level
    assert cu[11] is None  # the first BOS (up) is NOT a CHoCH
    assert all(v is None for i, v in enumerate(cd) if i != 20)


# --- FVG -------------------------------------------------------------------

def test_chart_p03_fvg_matches_hand_computed_values() -> None:
    """Rule declared: bullish FVG at bar i (i>=2) iff low[i] > high[i-2];
    zone top = low[i], bottom = high[i-2] (bearish mirror). The zone lines
    carry their levels from the detection bar while unfilled: a later close
    that trades through the gap (close <= bottom for bullish) fills it; the
    lines then emit nothing. Max span 50 bars. Required = 3."""
    # bar 4 must fill the zone WITHOUT creating a second gap: its high stays
    # above bar 2's low (14.0 > 13.0 -> no bearish FVG at bar 4).
    bars = _bars(
        closes=[10.0, 12.0, 15.0, 14.0, 9.0],
        highs=[10.5, 13.0, 16.0, 15.0, 14.0],
        lows=[9.0, 11.5, 13.0, 12.0, 8.0],
    )
    out = fvg(bars)
    assert out.kind == "computed"
    top = _line(out, "fvg_top")
    bottom = _line(out, "fvg_bottom")
    # bar 2: low[2]=13.0 > high[0]=10.5 -> bullish FVG; top=13.0, bottom=10.5
    assert top[2] == 13.0
    assert bottom[2] == 10.5
    # unfilled through bars 2..3 (closes 15, 14 stay above 10.5)
    assert top[3] == 13.0 and bottom[3] == 10.5
    # bar 4 closes 9.0 <= 10.5 -> filled; nothing after
    assert top[4] is None and bottom[4] is None


# --- Order Blocks (pattern) ------------------------------------------------

def test_chart_p03_order_blocks_pattern_matches_hand_computed_values() -> None:
    """Rule declared (geometric, NOT institutional): a bullish OB pattern
    forms at bar i when bar[i-1] is bearish (close < open), close[i] >
    high[i-1], and range[i] >= 1.5 x the MEDIAN range of the previous 20
    bars. Zone = [low[i-1], high[i-1]]; unfilled until a close trades below
    the zone bottom; max span 50. Required = 21."""
    n = 22
    closes = [10.0] * n
    opens = [10.0] * n
    highs = [10.5] * n
    lows = [9.5] * n
    # bar 20: bearish (close 9.5 < open 10.0), range 0.9 (high 10.2, low 9.3)
    opens[20] = 10.0
    closes[20] = 9.5
    highs[20] = 10.2
    lows[20] = 9.3
    # bar 21: closes above high[20], range 1.6 >= 1.5 x median range 1.0
    opens[21] = 9.6
    closes[21] = 11.0
    highs[21] = 11.1
    lows[21] = 9.5
    bars = _bars(closes, highs=highs, lows=lows, opens=opens)
    out = order_block_pattern(bars)
    assert out.kind == "computed"
    top = _line(out, "ob_top")
    bottom = _line(out, "ob_bottom")
    assert top[21] == 10.2  # high of the bearish bar
    assert bottom[21] == 9.3  # low of the bearish bar
    assert all(v is None for i, v in enumerate(top) if i != 21)


# --- Full-definition required_bars -----------------------------------------

def test_chart_p03_market_structure_required_bars_full_definition() -> None:
    reg = INDICATOR_REGISTRY
    assert reg["SWINGS55"].required_bars == 11   # 2k+1
    assert reg["STRUCT55"].required_bars == 29   # 5k+4: four confirmed swings
    assert reg["BOS55"].required_bars == 12      # 2k+2
    assert reg["CHOCH55"].required_bars == 24    # two BOS breaks
    assert reg["FVG3"].required_bars == 3
    assert reg["OBPATTERN"].required_bars == 21  # 20-window + 1
    for def_id in ("SWINGS55", "STRUCT55", "BOS55", "CHOCH55", "FVG3", "OBPATTERN"):
        d = reg[def_id]
        assert d.engine == "MarketStructure"
        assert d.pane == "overlay"
        assert d.disclosure is not None and "simulated OHLC" in d.disclosure


# --- M8 naming -------------------------------------------------------------

def test_chart_p03_no_institutional_behaviour_claims() -> None:
    import pathlib

    source = pathlib.Path("app/services/market_structure.py").read_text()
    for term in (
        "institutional order",
        "institutional accumulation",
        "smart money",
        "accumulation zone",
        "distribution zone",
        "entry zone",
    ):
        assert term not in source, f"forbidden institutional term in source: {term}"
    assert "not evidence of institutional activity" in STRUCTURE_DISCLOSURE
    # Conventional labels are permitted only with the disclosure.
    for def_id in ("SWINGS55", "BOS55", "CHOCH55", "FVG3", "OBPATTERN"):
        assert INDICATOR_REGISTRY[def_id].disclosure


# --- Annotation update/delete verbs (S1) -----------------------------------

def test_chart_p03_annotation_verbs_require_auth(client: TestClient) -> None:
    assert client.patch("/api/v1/collaboration/chart-annotations/nope", json={}).status_code == 401
    assert client.delete("/api/v1/collaboration/chart-annotations/nope").status_code == 401


def test_chart_p03_annotation_update_and_delete_audited(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    created = client.post(
        "/api/v1/collaboration/chart-annotations",
        headers=auth_headers,
        json={
            "artifact_type": "chart_research_drawing",
            "chart_context": {"symbol": "EURUSD", "timeframe": "M1", "resolution": "native"},
            "content": {
                "geometry": {
                    "kind": "trendline",
                    "handles": [
                        {"price": "1.10000", "time_iso": "2026-08-17T10:00:00Z"},
                        {"price": "1.10100", "time_iso": "2026-08-17T10:05:00Z"},
                    ],
                }
            },
            "source_artifact_ids": ["signal-1"],
        },
    )
    assert created.status_code == 201, created.text
    annotation_id = created.json()["id"]

    updated = client.patch(
        f"/api/v1/collaboration/chart-annotations/{annotation_id}",
        headers=auth_headers,
        json={
            "content": {
                "geometry": {
                    "kind": "trendline",
                    "handles": [
                        {"price": "1.10200", "time_iso": "2026-08-17T10:00:00Z"},
                        {"price": "1.10300", "time_iso": "2026-08-17T10:05:00Z"},
                    ],
                }
            }
        },
    )
    assert updated.status_code == 200, updated.text
    assert updated.json()["content"]["geometry"]["handles"][0]["price"] == "1.10200"

    # The update must be audited.
    audits = client.get(
        "/api/v1/persistence/audit-events",
        params={"category": "GOVERNANCE", "limit": 50},
        headers=auth_headers,
    ).json()
    assert any(a["action"] == "chart_research_annotation.updated" for a in audits)

    deleted = client.delete(
        f"/api/v1/collaboration/chart-annotations/{annotation_id}",
        headers=auth_headers,
    )
    assert deleted.status_code == 200, deleted.text
    assert (
        client.get(
            f"/api/v1/collaboration/chart-annotations/{annotation_id}",
            headers=auth_headers,
        ).status_code
        == 404
    )
    audits = client.get(
        "/api/v1/persistence/audit-events",
        params={"category": "GOVERNANCE", "limit": 50},
        headers=auth_headers,
    ).json()
    assert any(a["action"] == "chart_research_annotation.deleted" for a in audits)
