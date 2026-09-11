"""W5-U04 signal investigation workspace safety tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select

from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.model_artifact import ModelArtifact
from app.db.session import session_scope
from app.trading_intelligence.inference import GovernedModelEligibilityGate
from app.trading_intelligence.signals import AdvisorySignalService
from tests.test_advisory_signals import _fresh_input, _mark_economically_usable
from tests.test_live_inference_gate import _eligible_artifact


async def _auth_headers(async_client: AsyncClient) -> dict[str, str]:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


async def _seed_signal() -> tuple[str, str, tuple[object, ...]]:
    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        gate = GovernedModelEligibilityGate(session)
        await gate.promote_to_advisory_approved(
            artifact,
            approver="ITRGA-test",
            approval_reason="W5-U04 read-only investigation fixture",
        )
        await _mark_economically_usable(session, artifact)
        signal = await AdvisorySignalService(session).produce(
            model=artifact,
            inference_input=_fresh_input(),
            rationale=(
                "Signal investigation fixture with calibrated confidence and governed lineage."
            ),
            actor="pytest",
            risk_notes="research investigation only",
        )
        snapshot = (
            signal.signal_id,
            signal.signal_state,
            signal.state_reason,
            signal.raw_score,
            signal.calibrated_confidence,
            signal.rationale,
            tuple(signal.state_transition_history),
            artifact.status,
            artifact.advisory_status,
        )
        return signal.signal_id, artifact.id, snapshot


@pytest.mark.asyncio
async def test_signal_investigation_reads_require_auth_and_return_persisted_context(
    async_client: AsyncClient,
) -> None:
    signal_id, _, _ = await _seed_signal()

    unauth = await async_client.get("/api/v1/signals/history")
    assert unauth.status_code == 401

    headers = await _auth_headers(async_client)
    listing = await async_client.get("/api/v1/signals/history", headers=headers)
    assert listing.status_code == 200, listing.text
    assert any(row["signal_id"] == signal_id for row in listing.json())

    detail = await async_client.get(f"/api/v1/signals/history/{signal_id}", headers=headers)
    assert detail.status_code == 200, detail.text
    payload = detail.json()
    assert payload["signal_id"] == signal_id
    assert payload["rationale"]
    assert payload["calibrated_confidence"] == 0.5
    assert payload["raw_score"] != payload["calibrated_confidence"]
    assert payload["state_transition_history"][-1] in {"emitted", "warning", "withheld"}


@pytest.mark.asyncio
async def test_signal_investigation_triggers_and_mutates_nothing(async_client: AsyncClient) -> None:
    signal_id, model_id, before_snapshot = await _seed_signal()

    headers = await _auth_headers(async_client)
    async with session_scope() as session:
        before_signal_count = int(
            (await session.execute(select(func.count()).select_from(AdvisorySignal))).scalar_one()
        )
        before_model_count = int(
            (await session.execute(select(func.count()).select_from(ModelArtifact))).scalar_one()
        )

    for _ in range(3):
        listed = await async_client.get("/api/v1/signals/history", headers=headers)
        assert listed.status_code == 200, listed.text
        detail = await async_client.get(f"/api/v1/signals/history/{signal_id}", headers=headers)
        assert detail.status_code == 200, detail.text

    async with session_scope() as session:
        after_signal_count = int(
            (await session.execute(select(func.count()).select_from(AdvisorySignal))).scalar_one()
        )
        after_model_count = int(
            (await session.execute(select(func.count()).select_from(ModelArtifact))).scalar_one()
        )
        signal = await session.get(AdvisorySignal, signal_id)
        model = await session.get(ModelArtifact, model_id)
        assert signal is not None
        assert model is not None
        after_snapshot = (
            signal.signal_id,
            signal.signal_state,
            signal.state_reason,
            signal.raw_score,
            signal.calibrated_confidence,
            signal.rationale,
            tuple(signal.state_transition_history),
            model.status,
            model.advisory_status,
        )

    assert after_signal_count == before_signal_count
    assert after_model_count == before_model_count
    assert after_snapshot == before_snapshot


@pytest.mark.asyncio
async def test_signal_investigation_has_no_signal_write_endpoint(async_client: AsyncClient) -> None:
    signal_id, _, _ = await _seed_signal()
    headers = await _auth_headers(async_client)
    forbidden_posts = [
        f"/api/v1/signals/history/{signal_id}",
        f"/api/v1/signals/history/{signal_id}/emit",
        f"/api/v1/signals/history/{signal_id}/override-guardrail",
        f"/api/v1/signals/history/{signal_id}/regrade",
        "/api/v1/signals/history",
    ]
    for path in forbidden_posts:
        response = await async_client.post(path, headers=headers, json={"blocked": True})
        assert response.status_code in {404, 405}


def test_signal_investigation_workspace_has_no_mutation_or_execution_path() -> None:
    root = Path(__file__).resolve().parents[2]
    # UI-CONV-P03 item 6 (M3): the investigation surface was absorbed into the
    # terminal signal drill-down. This guard must point at the module that
    # ACTUALLY renders the drill-down, or the T-1 assertion would pass vacuously.
    frontend_path = root / "frontend" / "src" / "components" / "terminal" / "TerminalSignalStream.tsx"
    route_path = (
        Path(__file__).resolve().parents[1] / "app" / "api" / "routes" / "advisory_signals.py"
    )
    texts = [frontend_path.read_text(encoding="utf-8"), route_path.read_text(encoding="utf-8")]
    forbidden = (
        "advisory_status =",
        "model.status =",
        "emit_signal",
        "place_order",
        "update_signal",
        "override_guardrail",
        "broker.",
        "allow_execution",
        "gate_open",
    )
    for text in texts:
        for needle in forbidden:
            assert needle not in text
