"""W3-U02 advisory signal contract and persistence tests."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pytest
from httpx import AsyncClient

from app.core.time import utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.audit import AuditEvent
from app.db.models.calibration_report import CalibrationReport
from app.db.models.economic_report import EconomicReport
from app.trading_intelligence.inference import GovernedModelEligibilityGate
from app.trading_intelligence.signals import AdvisorySignalService
from tests.test_live_inference_gate import _eligible_artifact, _input


def _fresh_input(**overrides):  # noqa: ANN003, ANN201
    return _input(as_of_time=utc_now() - timedelta(seconds=60), **overrides)


async def _mark_economically_usable(session, artifact) -> None:  # noqa: ANN001
    economic = await session.get(EconomicReport, artifact.economic_report_id)
    assert economic is not None
    economic.economic_conclusion = {"verdict": "economically_usable"}
    await session.flush()


@pytest.mark.asyncio
async def test_emitted_signal_governed_lineage_rationale_calibrated_confidence(
    prepared_db: None,
) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        gate = GovernedModelEligibilityGate(session)
        await gate.promote_to_advisory_approved(
            artifact, approver="ITRGA-test", approval_reason="signal eligibility"
        )
        await _mark_economically_usable(session, artifact)
        service = AdvisorySignalService(session)
        signal = await service.produce(
            model=artifact,
            inference_input=_fresh_input(),
            rationale="Model score is in-domain; confidence is calibrated and lineage is complete.",
            actor="pytest",
            risk_notes="research advisory only",
        )
        assert signal.signal_state == "emitted"
        assert signal.state_reason == "ELIGIBLE"
        assert signal.raw_score is not None
        assert signal.calibrated_confidence == 0.5
        assert signal.calibrated_confidence != signal.raw_score
        assert signal.statistical_report_id == artifact.statistical_report_id
        assert signal.calibration_report_id == artifact.calibration_report_id
        assert signal.economic_report_id == artifact.economic_report_id
        assert signal.generalization_report_id is not None
        assert signal.rationale
        assert signal.explainability_summary["confidence"]["confidence_source"] == (
            "calibration_report_bins_or_base_rate"
        )
        assert signal.explainability_summary["limitations"] == [
            "advisory_record_only",
            "no_order_payload",
            "no_automatic_action",
            "human_governed_review_required",
        ]
        assert signal.state_transition_history == ["candidate", "eligible_checked", "emitted"]
        audit_actions = await session.scalars(
            select(AuditEvent.action).where(AuditEvent.resource_id == signal.signal_id)
        )
        assert "advisory_signal.emitted" in set(audit_actions.all())


@pytest.mark.asyncio
async def test_research_only_ineligible_signal_withheld_by_name(prepared_db: None) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        service = AdvisorySignalService(session)
        signal = await service.produce(
            model=artifact,
            inference_input=_fresh_input(),
            rationale="Should not emit before advisory approval.",
            actor="pytest",
        )
        assert signal.signal_state == "withheld"
        assert "NOT_ADVISORY_APPROVED" in signal.state_reason
        assert "NOT_ADVISORY_APPROVED" in signal.eligibility_reasons
        assert signal.raw_score is None
        assert signal.calibrated_confidence is None
        audit_actions = await session.scalars(
            select(AuditEvent.action).where(AuditEvent.resource_id == signal.signal_id)
        )
        assert "advisory_signal.withheld" in set(audit_actions.all())


@pytest.mark.asyncio
async def test_out_of_domain_signal_withheld_by_name(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        gate = GovernedModelEligibilityGate(session)
        await gate.promote_to_advisory_approved(
            artifact, approver="ITRGA-test", approval_reason="signal eligibility"
        )
        service = AdvisorySignalService(session)
        signal = await service.produce(
            model=artifact,
            inference_input=_fresh_input(market_class="crypto"),
            rationale="Out-of-domain should be withheld.",
            actor="pytest",
        )
        assert signal.signal_state == "withheld"
        assert signal.operating_domain_status == "unsupported"
        assert "UNSUPPORTED_DOMAIN" in signal.eligibility_reasons


@pytest.mark.asyncio
async def test_poor_calibration_signal_warning_with_reason(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        calibration = await session.get(CalibrationReport, artifact.calibration_report_id)
        assert calibration is not None
        calibration.warnings = ["POORLY_CALIBRATED"]
        gate = GovernedModelEligibilityGate(session)
        await gate.promote_to_advisory_approved(
            artifact, approver="ITRGA-test", approval_reason="signal eligibility"
        )
        await _mark_economically_usable(session, artifact)
        service = AdvisorySignalService(session)
        signal = await service.produce(
            model=artifact,
            inference_input=_fresh_input(),
            rationale="Eligible but calibration report warns about probability quality.",
            actor="pytest",
        )
        assert signal.signal_state == "warning"
        assert signal.state_reason == "POORLY_CALIBRATED"
        assert signal.calibration_status == "warning:POORLY_CALIBRATED"
        assert signal.calibrated_confidence == 0.5
        assert signal.raw_score != signal.calibrated_confidence
        assert signal.risk_notes is not None
        assert "Calibration warning" in signal.risk_notes


@pytest.mark.asyncio
async def test_no_rationale_signal_withheld(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        gate = GovernedModelEligibilityGate(session)
        await gate.promote_to_advisory_approved(
            artifact, approver="ITRGA-test", approval_reason="signal eligibility"
        )
        service = AdvisorySignalService(session)
        signal = await service.produce(
            model=artifact,
            inference_input=_fresh_input(),
            rationale=" ",
            actor="pytest",
        )
        assert signal.signal_state == "withheld"
        assert signal.state_reason == "RATIONALE_REQUIRED"
        assert signal.raw_score is None
        assert signal.calibrated_confidence is None
        assert "RATIONALE_REQUIRED" in signal.eligibility_reasons


def test_signal_is_inert_no_order_payload_or_broker_path() -> None:
    forbidden_columns = {
        "order_id",
        "order_payload",
        "order_intent",
        "quantity",
        "volume_lots",
        "stop_loss",
        "take_profit",
        "broker_account_id",
    }
    assert forbidden_columns.isdisjoint(set(AdvisorySignal.__table__.columns.keys()))

    signal_root = Path(__file__).resolve().parents[1] / "app" / "trading_intelligence" / "signals"
    route_path = (
        Path(__file__).resolve().parents[1] / "app" / "api" / "routes" / "advisory_signals.py"
    )
    forbidden = ("place_order", "cancel_order", "broker.", "execute", "order_intent dispatch")
    for path in [*signal_root.rglob("*.py"), route_path]:
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text


@pytest.mark.asyncio
async def test_signal_history_api_auth_required_and_returns_persisted_signals(
    async_client: AsyncClient,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _eligible_artifact(session)
        gate = GovernedModelEligibilityGate(session)
        await gate.promote_to_advisory_approved(
            artifact, approver="ITRGA-test", approval_reason="history api eligibility"
        )
        await _mark_economically_usable(session, artifact)
        service = AdvisorySignalService(session)
        signal = await service.produce(
            model=artifact,
            inference_input=_fresh_input(),
            rationale="Persisted signal for read-only history API.",
            actor="pytest",
        )
        signal_id = signal.signal_id

    unauth = await async_client.get("/api/v1/signals/history")
    assert unauth.status_code == 401

    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    access = login.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {access}"}

    listed = await async_client.get(
        "/api/v1/signals/history",
        params={"signal_state": "emitted"},
        headers=headers,
    )
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert any(row["signal_id"] == signal_id for row in rows)
    row = next(row for row in rows if row["signal_id"] == signal_id)
    assert row["signal_state"] == "emitted"
    assert row["rationale"]
    assert row["calibrated_confidence"] == 0.5

    one = await async_client.get(f"/api/v1/signals/history/{signal_id}", headers=headers)
    assert one.status_code == 200, one.text
    assert one.json()["signal_id"] == signal_id
