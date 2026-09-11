"""W4-U06 Professional Signal Validation report tests."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pytest
from httpx import AsyncClient

from app.core.time import utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.audit import AuditEvent
from app.db.models.model_artifact import ModelArtifact
from app.db.models.signal_validation_report import SignalValidationReport
from app.institutional_intelligence import (
    SignalValidationReportService,
    SignalValidationScope,
)
from app.trading_intelligence.inference import GovernedModelEligibilityGate
from tests.test_live_inference_gate import _eligible_artifact


async def _signal(session, artifact, *, state: str, as_of_time, raw_score=0.987654):  # noqa: ANN001
    signal = AdvisorySignal(
        as_of_time=as_of_time,
        market_class="forex",
        provider="internal",
        symbol="EURUSD",
        timeframe="M1",
        model_artifact_id=artifact.id,
        model_version=artifact.version,
        feature_set_version=artifact.feature_set_version or "feature_set.v1",
        experiment_id=artifact.experiment_id or "exp",
        statistical_report_id=artifact.statistical_report_id,
        calibration_report_id=artifact.calibration_report_id,
        economic_report_id=artifact.economic_report_id,
        generalization_report_id=None,
        inference_input_hash=f"hash-{state}-{as_of_time.isoformat()}",
        raw_score=raw_score,
        calibrated_confidence=0.5 if state != "withheld" else None,
        input_staleness_seconds=60,
        signal_validity_seconds=300,
        expires_at=utc_now() + timedelta(minutes=5),
        freshness_status="fresh" if state != "expired" else "expired",
        signal_direction="positive_bias" if state != "withheld" else "withheld",
        signal_state=state,
        state_reason="ELIGIBLE" if state == "emitted" else state.upper(),
        eligibility_reasons=[] if state == "emitted" else [state.upper()],
        operating_domain_status="valid",
        calibration_status="calibrated" if state != "warning" else "warning:POORLY_CALIBRATED",
        economic_verdict="economically_usable",
        risk_notes=None,
        rationale="Signal validation fixture.",
        explainability_summary={"confidence": {"calibrated_confidence": 0.5}},
        state_transition_history=["candidate", "eligible_checked", state],
        audit_correlation_id=f"corr-{state}-{as_of_time.isoformat()}",
    )
    session.add(signal)
    await session.flush()
    return signal


async def _seed_scope(session):  # noqa: ANN001, ANN201
    artifact = await _eligible_artifact(session)
    await GovernedModelEligibilityGate(session).promote_to_advisory_approved(
        artifact,
        approver="pytest",
        approval_reason="signal validation fixture approval",
    )
    base = utc_now() - timedelta(minutes=10)
    signals = [
        await _signal(session, artifact, state="emitted", as_of_time=base),
        await _signal(session, artifact, state="warning", as_of_time=base + timedelta(minutes=1)),
        await _signal(session, artifact, state="withheld", as_of_time=base + timedelta(minutes=2)),
        await _signal(session, artifact, state="expired", as_of_time=base + timedelta(minutes=3)),
    ]
    future = await _signal(
        session,
        artifact,
        state="emitted",
        as_of_time=base + timedelta(minutes=5),
        raw_score=0.111111,
    )
    return artifact, base, base + timedelta(minutes=3), signals, future


@pytest.mark.asyncio
async def test_signal_validation_full_declared_scope_no_cherry_picking_deterministic(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, start, end, signals, _ = await _seed_scope(session)
        service = SignalValidationReportService(session)
        scope = SignalValidationScope(
            start, end, market_class="forex", symbol="EURUSD", timeframe="M1"
        )
        first = (await service.create_report(scope=scope, actor="pytest")).report
        second = (await service.create_report(scope=scope, actor="pytest")).report
        assert first.sample_count == len(signals) == 4
        assert first.source_signal_ids == [signal.signal_id for signal in signals]
        assert first.metrics == second.metrics
        assert first.validation_scope == second.validation_scope
        assert first.config["scope"]["include_states"] == [
            "emitted",
            "warning",
            "withheld",
            "expired",
        ]


@pytest.mark.asyncio
async def test_signal_validation_raw_score_present_upstream_absent_downstream(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, start, end, signals, _ = await _seed_scope(session)
        assert any(signal.raw_score is not None for signal in signals)
        report = (
            await SignalValidationReportService(session).create_report(
                scope=SignalValidationScope(
                    start, end, market_class="forex", symbol="EURUSD", timeframe="M1"
                ),
                actor="pytest",
            )
        ).report
        serialized = str(
            {
                "metrics": report.metrics,
                "results": report.results,
                "lineage": report.input_lineage,
            }
        )
        assert "raw_score" not in serialized
        assert "0.987654" not in serialized
        assert report.input_lineage["uncalibrated_model_score_excluded"] is True
        assert "uncalibrated_model_score_excluded" in report.limitations


@pytest.mark.asyncio
async def test_signal_validation_no_lookahead_future_signal_excluded(prepared_db: None) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, start, end, signals, future = await _seed_scope(session)
        result = await SignalValidationReportService(session).create_report(
            scope=SignalValidationScope(
                start, end, market_class="forex", symbol="EURUSD", timeframe="M1"
            ),
            actor="pytest",
        )
        assert result.excluded_future_signal_count == 1
        assert future.signal_id not in result.report.source_signal_ids
        assert result.report.source_signal_ids == [signal.signal_id for signal in signals]


@pytest.mark.asyncio
async def test_signal_validation_metrics_uncertainty_economic_and_outcome_status(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, start, end, _, _ = await _seed_scope(session)
        report = (
            await SignalValidationReportService(session).create_report(
                scope=SignalValidationScope(
                    start, end, market_class="forex", symbol="EURUSD", timeframe="M1"
                ),
                actor="pytest",
            )
        ).report
        for metric in report.metrics.values():
            assert metric["sample_count"] == report.sample_count
            assert metric["uncertainty"]["method"] == "wilson_score_interval"
        assert report.outcome_data_status["status"] == "not_available"
        assert report.economic_usefulness["verdict"] == "not_assessed"
        assert "not_a_guarantee" in report.limitations
        assert "no_governed_forward_outcomes_available" in report.limitations


@pytest.mark.asyncio
async def test_signal_validation_persisted_audited_no_signal_or_model_mutation(
    prepared_db: None,
) -> None:
    from sqlalchemy import select

    from app.db.session import session_scope

    async with session_scope() as session:
        artifact, start, end, _, _ = await _seed_scope(session)
        before_statuses = {artifact.id: artifact.status}
        before_signals = len(list((await session.scalars(select(AdvisorySignal))).all()))
        service = SignalValidationReportService(session)
        report = (
            await service.create_report(
                scope=SignalValidationScope(
                    start, end, market_class="forex", symbol="EURUSD", timeframe="M1"
                ),
                actor="pytest",
            )
        ).report
        assert await session.get(SignalValidationReport, report.id) is not None
        actions = list(
            (
                await session.scalars(
                    select(AuditEvent.action).where(AuditEvent.resource_id == report.id)
                )
            ).all()
        )
        assert "signal_validation_report.created" in actions
        await service.assert_no_side_effects(
            model_statuses=before_statuses,
            signal_count=before_signals,
        )
        refreshed = await session.get(ModelArtifact, artifact.id)
        assert refreshed is not None
        assert refreshed.status == before_statuses[artifact.id]


def test_signal_validation_schema_is_inert_no_raw_score_order_or_signal_payload() -> None:
    forbidden_columns = {
        "raw_score",
        "order_payload",
        "order_intent",
        "signal_payload",
        "execution_payload",
        "remediation_payload",
        "broker_account_id",
        "quantity",
        "position_size",
    }
    assert forbidden_columns.isdisjoint(set(SignalValidationReport.__table__.columns.keys()))


@pytest.mark.asyncio
async def test_signal_validation_api_auth_read_only_and_returns_scope(
    async_client: AsyncClient,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        _, start, end, _, _ = await _seed_scope(session)
        report = (
            await SignalValidationReportService(session).create_report(
                scope=SignalValidationScope(
                    start, end, market_class="forex", symbol="EURUSD", timeframe="M1"
                ),
                actor="pytest",
            )
        ).report
        report_id = report.id

    unauth = await async_client.get("/api/v1/intelligence/signal-validation-reports")
    assert unauth.status_code == 401
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}
    listed = await async_client.get(
        "/api/v1/intelligence/signal-validation-reports", headers=headers
    )
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert any(row["id"] == report_id for row in rows)
    detail = await async_client.get(
        f"/api/v1/intelligence/signal-validation-reports/{report_id}", headers=headers
    )
    assert detail.status_code == 200, detail.text
    body = detail.json()
    assert body["sample_count"] == 4
    assert body["outcome_data_status"]["status"] == "not_available"
    assert body["input_lineage"]["uncalibrated_model_score_excluded"] is True
    # BO-B-04 supersession: the POST generation endpoint now EXISTS.
    # A body-less POST fails request validation (422), no longer 405.
    post = await async_client.post(
        "/api/v1/intelligence/signal-validation-reports", headers=headers
    )
    assert post.status_code == 422


def test_signal_validation_modules_use_no_unspiked_dependencies_or_execution_path() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "institutional_intelligence"
    forbidden = (
        "import sklearn",
        "import statsmodels",
        "place_order",
        "cancel_order",
        "broker.",
        "emit_signal",
        "live_signal",
        "order_payload =",
        "execution_payload =",
        "advisory_status =",
        "model.status =",
    )
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text
