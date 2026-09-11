"""V2 BE-10 contract tests — BO-V2-BE-10-001 L5/L6 (enum closed, wording
law, refusal shapes). Socket guard on every test."""

from __future__ import annotations

import ast
import socket
from pathlib import Path

import pytest

from app.v2.account_context.contract import (
    ALIGNMENT_VERDICTS,
    LIVE_SIGNAL_STATES,
    REFUSAL_CLASSES,
    AccountContextRefused,
    AlignmentMatrix,
    AlignmentRow,
)

BACKEND = Path(__file__).resolve().parents[1]
BAND_DIR = BACKEND / "app/v2/account_context"

# The wording law: no ACTION verb may appear anywhere in the band's
# vocabulary or code identifiers — the band names STATES, never trades.
ACTION_VERBS = ("buy", "sell", "enter", "exit", "add_position",
                "reduce", "close_position", "open_position",
                "recommend", "should_", "advice", "order_send",
                "place_order", "submit")


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-10 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


def test_l5_verdict_enum_closed_and_sealed_order():
    assert ALIGNMENT_VERDICTS == (
        "aligned", "opposed", "unsignalled_holding",
        "signal_without_holding", "flat_no_signal", "indeterminate",
        "unmapped")
    assert len(set(ALIGNMENT_VERDICTS)) == 7


def test_r35_flat_and_no_signal_distinct_states():
    """FLAT basis and NO-SIGNAL are distinct, named states."""
    assert "flat_no_signal" in ALIGNMENT_VERDICTS
    assert "unsignalled_holding" in ALIGNMENT_VERDICTS
    assert "signal_without_holding" in ALIGNMENT_VERDICTS
    # and the enum carries no synonym collapse of the three


def test_l5_wording_law_state_nouns_only():
    """No action verb in any verdict, refusal class, or band identifier."""
    for verdict in ALIGNMENT_VERDICTS + REFUSAL_CLASSES:
        low = verdict.lower()
        for verb in ACTION_VERBS:
            assert verb not in low, f"{verb} in {verdict}"
    # code identifiers across the band (docstrings stripped)
    for f in BAND_DIR.rglob("*.py"):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef,
                                 ast.FunctionDef, ast.AsyncFunctionDef)):
                body = node.body
                if (body and isinstance(body[0], ast.Expr)
                        and isinstance(body[0].value, ast.Constant)
                        and isinstance(body[0].value.value, str)):
                    body[0].value.value = ""
        code = ast.unparse(tree).lower()
        for verb in ACTION_VERBS:
            assert verb not in code, f"{verb} in {f.name}"


def test_refusal_taxonomy_closed_and_typed():
    assert REFUSAL_CLASSES == ("account_context.no_basis",
                               "account_context.mapping_artifact_absent")
    exc = AccountContextRefused("account_context.no_basis",
                                [{"failing": "basis"}])
    assert exc.refusal_class == "account_context.no_basis"
    with pytest.raises(AssertionError):
        AccountContextRefused("account_context.invented_class", [])


def test_live_signal_states_subset_of_be5_vocabulary():
    from app.v2.research_governance.contracts import SIGNAL_STATES
    assert set(LIVE_SIGNAL_STATES) <= set(SIGNAL_STATES)
    assert LIVE_SIGNAL_STATES == ("emitted",)


def test_row_and_matrix_shapes_frozen():
    row = AlignmentRow(
        instrument_ext_id="EURUSDm", instrument_id="forex.eurusd",
        posture="long", units_long="1", units_short="0",
        signal_state="live", signal_direction="up", verdict="aligned",
        basis_sync_run_id="s1", basis_age_hours=0.5)
    with pytest.raises(AttributeError):
        row.verdict = "opposed"  # frozen dataclass
    m = AlignmentMatrix()
    assert m.unmapped_count == 0 and m.staleness == "fresh"
