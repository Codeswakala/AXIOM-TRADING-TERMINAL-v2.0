"""W5-U03 inert chart research annotation tests."""

from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.collaboration import (
    CHART_RESEARCH_ANNOTATION_DISCLAIMER,
    ChartResearchAnnotationDraft,
    ChartResearchAnnotationFactory,
    ChartResearchAnnotationRepository,
)
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.assistant_research_response import AssistantResearchResponse
from app.db.models.audit import AuditEvent
from app.db.models.chart_research_annotation import ChartResearchAnnotation
from app.db.models.monitoring_alert import MonitoringAlert
from app.db.session import session_scope


def _draft(**overrides: object) -> ChartResearchAnnotationDraft:
    values: dict[str, object] = {
        "artifact_type": "chart_research_annotation",
        "chart_context": {
            "market_class": "forex",
            "symbol": "EURUSD",
            "timeframe": "M1",
            "anchor": {"mode": "visible_window", "label": "recent context"},
        },
        "content": {
            "drawing_kind": "research_note",
            "text": "Guardrail context note for research review only.",
            "visual": {"x_percent": 24, "y_percent": 32},
        },
        "source_artifact_ids": ("signal-1", "report-1"),
        "provenance": {"operator_authored": True},
        "uncertainty": {"method": "not_applicable_operator_markup"},
        "research_status": "research_only",
    }
    values.update(overrides)
    return ChartResearchAnnotationDraft(**values)  # type: ignore[arg-type]


async def _annotation(session: AsyncSession, annotation_id: str) -> ChartResearchAnnotation:
    annotation = await session.get(ChartResearchAnnotation, annotation_id)
    assert annotation is not None
    return annotation


async def _assert_no_orphan_audit(session: AsyncSession) -> None:
    stmt = (
        select(ChartResearchAnnotation.id)
        .outerjoin(
            AuditEvent,
            and_(
                AuditEvent.resource_type == "chart_research_annotation",
                AuditEvent.resource_id == ChartResearchAnnotation.id,
                AuditEvent.correlation_id == ChartResearchAnnotation.audit_correlation_id,
                AuditEvent.action == "chart_research_annotation.created",
            ),
        )
        .where(AuditEvent.id.is_(None))
    )
    assert list((await session.scalars(stmt)).all()) == []


async def _count(session: AsyncSession, model: type[object]) -> int:
    return int((await session.execute(select(func.count()).select_from(model))).scalar_one())


def test_chart_annotation_contract_rejects_forbidden_fields() -> None:
    factory = ChartResearchAnnotationFactory()
    forbidden = [
        "order_payload",
        "order_intent",
        "side",
        "quantity",
        "position_size",
        "stop_loss",
        "take_profit",
        "broker_account_id",
        "account_id",
        "position_id",
        "execution_status",
        "signal_payload",
        "emit_signal",
        "raw_score",
        "guaranteed_outcome",
    ]
    for key in forbidden:
        with pytest.raises(ValueError, match="CHART_ANNOTATION_FORBIDDEN_FIELD"):
            factory.validate(
                _draft(content={"drawing_kind": "research_note", "nested": {key: "blocked"}})
            )


def test_chart_annotation_contract_rejects_raw_score_and_guarantee_text() -> None:
    factory = ChartResearchAnnotationFactory()
    with pytest.raises(ValueError, match="CHART_ANNOTATION_FORBIDDEN_TEXT"):
        factory.validate(
            _draft(content={"drawing_kind": "research_note", "text": "raw_score 0.9"})
        )
    with pytest.raises(ValueError, match="CHART_ANNOTATION_FORBIDDEN_TEXT"):
        factory.validate(
            _draft(content={"drawing_kind": "research_note", "text": "guaranteed profit"})
        )


def test_chart_annotation_schema_has_no_forbidden_fields() -> None:
    forbidden = {
        "order_payload",
        "order_intent",
        "side",
        "quantity",
        "lot_size",
        "order_size",
        "position_size",
        "entry_price_order",
        "stop_loss",
        "take_profit",
        "broker_account_id",
        "account_id",
        "position_id",
        "execution_status",
        "live_position",
        "signal_payload",
        "emit_signal",
        "raw_score",
        "predicted_outcome",
        "guaranteed_outcome",
    }
    column_names = {column.name for column in ChartResearchAnnotation.__table__.columns}
    assert column_names.isdisjoint(forbidden)


@pytest.mark.asyncio
async def test_chart_annotation_persists_and_audits_no_orphan(prepared_db: None) -> None:
    async with session_scope() as session:
        annotation = await ChartResearchAnnotationRepository(session).create_annotation(
            draft=_draft(), operator_id="pytest"
        )
        stored = await _annotation(session, annotation.id)
        assert stored.research_status == "research_only"
        assert stored.source_artifact_ids == ["signal-1", "report-1"]
        assert stored.disclaimer == CHART_RESEARCH_ANNOTATION_DISCLAIMER
        assert stored.provenance["presentation_only"] is True
        assert stored.provenance["ai_assisted"] is False
        assert "AXIOM does not act" in stored.disclaimer
        event = (
            await session.scalars(
                select(AuditEvent).where(
                    AuditEvent.resource_type == "chart_research_annotation",
                    AuditEvent.resource_id == stored.id,
                )
            )
        ).one()
        assert event.action == "chart_research_annotation.created"
        assert event.correlation_id == stored.audit_correlation_id
        await _assert_no_orphan_audit(session)


@pytest.mark.asyncio
async def test_chart_annotation_triggers_nothing_beyond_annotation_and_audit(
    prepared_db: None,
) -> None:
    async with session_scope() as session:
        before_signals = await _count(session, AdvisorySignal)
        before_assistant = await _count(session, AssistantResearchResponse)
        before_alerts = await _count(session, MonitoringAlert)
        await ChartResearchAnnotationRepository(session).create_annotation(
            draft=_draft(), operator_id="pytest"
        )
        assert await _count(session, AdvisorySignal) == before_signals
        assert await _count(session, AssistantResearchResponse) == before_assistant
        assert await _count(session, MonitoringAlert) == before_alerts


async def _auth_headers(async_client: AsyncClient) -> dict[str, str]:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


@pytest.mark.asyncio
async def test_chart_annotation_api_auth_create_list_detail(async_client: AsyncClient) -> None:
    unauth_list = await async_client.get("/api/v1/collaboration/chart-annotations")
    assert unauth_list.status_code == 401
    unauth_create = await async_client.post(
        "/api/v1/collaboration/chart-annotations",
        json={
            "chart_context": _draft().chart_context,
            "content": _draft().content,
            "source_artifact_ids": ["signal-1"],
        },
    )
    assert unauth_create.status_code == 401

    headers = await _auth_headers(async_client)
    create = await async_client.post(
        "/api/v1/collaboration/chart-annotations",
        headers=headers,
        json={
            "artifact_type": "chart_research_annotation",
            "chart_context": _draft().chart_context,
            "content": _draft().content,
            "source_artifact_ids": ["signal-1", "report-1"],
            "provenance": {"test": "api"},
            "uncertainty": {"method": "not_applicable_operator_markup"},
        },
    )
    assert create.status_code == 201, create.text
    payload = create.json()
    assert payload["research_status"] == "research_only"
    assert payload["disclaimer"] == CHART_RESEARCH_ANNOTATION_DISCLAIMER
    annotation_id = payload["id"]

    listing = await async_client.get(
        "/api/v1/collaboration/chart-annotations?symbol=EURUSD&timeframe=M1",
        headers=headers,
    )
    assert listing.status_code == 200, listing.text
    assert any(item["id"] == annotation_id for item in listing.json())

    detail = await async_client.get(
        f"/api/v1/collaboration/chart-annotations/{annotation_id}",
        headers=headers,
    )
    assert detail.status_code == 200, detail.text
    assert detail.json()["source_artifact_ids"] == ["signal-1", "report-1"]


@pytest.mark.asyncio
async def test_chart_annotation_api_rejects_forbidden_payload(async_client: AsyncClient) -> None:
    headers = await _auth_headers(async_client)
    forbidden_payload = dict(_draft().content)
    forbidden_payload["order_payload"] = {"blocked": True}
    response = await async_client.post(
        "/api/v1/collaboration/chart-annotations",
        headers=headers,
        json={
            "chart_context": _draft().chart_context,
            "content": forbidden_payload,
            "source_artifact_ids": ["signal-1"],
        },
    )
    assert response.status_code == 422
    assert "CHART_ANNOTATION_FORBIDDEN_FIELD" in response.text
