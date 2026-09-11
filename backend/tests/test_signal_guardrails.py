"""W3-U03 emit-time guardrails and staleness contract tests."""

from __future__ import annotations

from datetime import timedelta

import pytest
from httpx import AsyncClient

from app.core.time import utc_now
from app.db.models.audit import AuditEvent
from app.db.models.calibration_report import CalibrationReport
from app.db.models.economic_report import EconomicReport
from app.trading_intelligence.inference import GovernedModelEligibilityGate
from app.trading_intelligence.signals import AdvisorySignalService, SignalGuardrailConfig
from tests.test_live_inference_gate import _eligible_artifact, _input


def _fresh_input(**overrides):  # noqa: ANN003, ANN201
    return _input(as_of_time=utc_now() - timedelta(seconds=60), **overrides)


async def _mark_economically_usable(session, artifact) -> None:  # noqa: ANN001
    economic = await session.get(EconomicReport, artifact.economic_report_id)
    assert economic is not None
    economic.economic_conclusion = {"verdict": "economically_usable"}
    await session.flush()


async def _approved_artifact(session):  # noqa: ANN001, ANN201
    artifact = await _eligible_artifact(session)
    gate = GovernedModelEligibilityGate(session)
    await gate.promote_to_advisory_approved(
        artifact,
        approver="ITRGA-test",
        approval_reason="W3-U03 guardrail eligibility",
    )
    return artifact


@pytest.mark.asyncio
async def test_emit_time_provider_symbol_domain_guardrail_withheld_by_name(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _approved_artifact(session)
        await _mark_economically_usable(session, artifact)
        artifact.operating_domain = {
            "markets": ["forex"],
            "timeframes": ["M1"],
            "regimes": ["trend"],
            "providers": ["internal"],
            "symbols": ["EURUSD"],
            "sources": ["live:simulated"],
        }
        service = AdvisorySignalService(session)
        signal = await service.produce(
            model=artifact,
            inference_input=_fresh_input(provider="external"),
            rationale="Provider is outside the validated emit-time operating domain.",
            actor="pytest",
        )
        assert signal.signal_state == "withheld"
        assert signal.state_reason == "UNSUPPORTED_DOMAIN"
        assert signal.operating_domain_status == "unsupported"
        assert "UNSUPPORTED_DOMAIN" in signal.eligibility_reasons
        assert signal.raw_score is None


@pytest.mark.asyncio
async def test_poor_calibration_ece_withheld_by_threshold_gate(prepared_db: None) -> None:
    """BO-B-02 supersession: a post-promotion calibration degradation that
    breaches the substantive threshold (ECE > 0.10) is now HARD-WITHHELD at
    emit time with the explicit threshold reason — the W3-U03 warning tier no
    longer applies to threshold-failing models."""
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _approved_artifact(session)
        await _mark_economically_usable(session, artifact)
        calibration = await session.get(CalibrationReport, artifact.calibration_report_id)
        assert calibration is not None
        calibration.warnings = []
        calibration.expected_calibration_error = "0.30"
        service = AdvisorySignalService(
            session,
            guardrail_config=SignalGuardrailConfig(calibration_warning_ece_threshold=0.15),
        )
        signal = await service.produce(
            model=artifact,
            inference_input=_fresh_input(),
            rationale="Calibration ECE breaches the substantive threshold after promotion.",
            actor="pytest",
        )
        assert signal.signal_state == "withheld"
        assert "CALIBRATION_THRESHOLD_NOT_MET" in signal.state_reason
        assert "CALIBRATION_THRESHOLD_NOT_MET" in signal.eligibility_reasons
        assert signal.raw_score is None


@pytest.mark.asyncio
async def test_economically_unusable_withheld_by_threshold_gate(prepared_db: None) -> None:
    """BO-B-02 supersession: an economically-unusable verdict (post-promotion
    degradation) is now HARD-WITHHELD at emit time with the explicit threshold
    reason, while the verdict itself remains visible on the withheld record."""
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _approved_artifact(session)
        economic = await session.get(EconomicReport, artifact.economic_report_id)
        assert economic is not None
        economic.economic_conclusion = {"verdict": "economically_unusable"}
        economic.scenario_results = {"base": {"net_return_bps": -3.0}}
        await session.flush()
        service = AdvisorySignalService(session)
        signal = await service.produce(
            model=artifact,
            inference_input=_fresh_input(),
            rationale="The statistical signal exists but economic validation is unusable.",
            actor="pytest",
        )
        assert signal.signal_state == "withheld"
        assert "ECONOMIC_NOT_USABLE" in signal.state_reason
        assert signal.economic_verdict == "economically_unusable"
        assert signal.raw_score is None


@pytest.mark.asyncio
async def test_stale_input_withheld_stale_input_reason(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _approved_artifact(session)
        await _mark_economically_usable(session, artifact)
        service = AdvisorySignalService(
            session,
            guardrail_config=SignalGuardrailConfig(max_input_staleness_seconds=30),
        )
        signal = await service.produce(
            model=artifact,
            inference_input=_input(as_of_time=utc_now() - timedelta(minutes=10)),
            rationale="Input is too old to present as a current advisory signal.",
            actor="pytest",
        )
        assert signal.signal_state == "withheld"
        assert signal.state_reason == "STALE_INPUT"
        assert signal.freshness_status == "stale"
        assert signal.input_staleness_seconds is not None
        assert signal.input_staleness_seconds > 30
        assert signal.raw_score is None
        assert signal.explainability_summary["freshness"]["freshness_status"] == "stale"


@pytest.mark.asyncio
async def test_signal_past_validity_expired_and_not_returned_current(
    async_client: AsyncClient,
) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _approved_artifact(session)
        await _mark_economically_usable(session, artifact)
        service = AdvisorySignalService(
            session,
            guardrail_config=SignalGuardrailConfig(signal_validity_seconds=0),
        )
        signal = await service.produce(
            model=artifact,
            inference_input=_fresh_input(),
            rationale="This signal is configured to expire immediately for R-2 proof.",
            actor="pytest",
        )
        signal_id = signal.signal_id
        assert signal.signal_state == "expired"
        assert signal.state_reason == "SIGNAL_EXPIRED"
        assert signal.freshness_status == "expired"
        assert signal.state_transition_history == [
            "candidate",
            "eligible_checked",
            "emitted",
            "expired",
        ]
        audit_actions = await session.scalars(
            select(AuditEvent.action).where(AuditEvent.resource_id == signal.signal_id)
        )
        assert "advisory_signal.expired" in set(audit_actions.all())

    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}

    current = await async_client.get(
        "/api/v1/signals/history",
        params={"current_only": "true"},
        headers=headers,
    )
    assert current.status_code == 200, current.text
    assert all(row["signal_id"] != signal_id for row in current.json())

    expired = await async_client.get(
        "/api/v1/signals/history",
        params={"signal_state": "expired"},
        headers=headers,
    )
    assert expired.status_code == 200, expired.text
    assert any(row["signal_id"] == signal_id for row in expired.json())

    unauth = await async_client.get("/api/v1/signals/history", params={"current_only": "true"})
    assert unauth.status_code == 401

    post_attempt = await async_client.post("/api/v1/signals/history", headers=headers)
    assert post_attempt.status_code == 405


@pytest.mark.asyncio
async def test_guardrail_violating_case_cannot_be_forced_to_emitted(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        artifact = await _approved_artifact(session)
        economic = await session.get(EconomicReport, artifact.economic_report_id)
        assert economic is not None
        economic.economic_conclusion = {"verdict": "economically_unusable"}
        economic.scenario_results = {"base": {"net_return_bps": -3.0}}
        await session.flush()
        service = AdvisorySignalService(session)
        signal = await service.produce(
            model=artifact,
            inference_input=_fresh_input(),
            rationale="Operator wording cannot force a clean emitted signal past economics.",
            actor="pytest",
            risk_notes="force emitted requested in wording but guardrail must prevail",
        )
        assert signal.signal_state == "withheld"
        assert "ECONOMIC_NOT_USABLE" in signal.state_reason
        assert signal.signal_state != "emitted"
        assert signal.risk_notes is not None
        assert "force emitted" in signal.risk_notes
