"""Repository integration tests against isolated in-memory SQLite."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.db.models.candle import Candle
from app.db.models.feature import FeatureRecord
from app.db.models.model_artifact import ModelArtifact
from app.db.session import session_scope
from app.repositories.audit_repository import AuditRepository
from app.repositories.candle_repository import CandleRepository
from app.repositories.feature_repository import FeatureRepository
from app.repositories.model_artifact_repository import ModelArtifactRepository


@pytest.mark.asyncio
async def test_candle_repository_crud(prepared_db: None) -> None:
    open_time = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    async with session_scope() as session:
        repo = CandleRepository(session)
        created = await repo.add(
            Candle(
                market_class="forex",
                symbol="EURUSD",
                timeframe="H1",
                open_time=open_time,
                open=Decimal("1.1000"),
                high=Decimal("1.1050"),
                low=Decimal("1.0950"),
                close=Decimal("1.1020"),
                volume=Decimal("1000"),
                source="test",
            )
        )
        assert created.id

    async with session_scope() as session:
        repo = CandleRepository(session)
        found = await repo.get_by_natural_key(
            market_class="forex",
            symbol="EURUSD",
            timeframe="H1",
            open_time=open_time,
        )
        assert found is not None
        assert found.close == Decimal("1.1020")
        listed = await repo.list_for_symbol(symbol="EURUSD", timeframe="H1")
        assert len(listed) == 1


@pytest.mark.asyncio
async def test_feature_and_model_placeholders(prepared_db: None) -> None:
    as_of = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    async with session_scope() as session:
        features = FeatureRepository(session)
        models = ModelArtifactRepository(session)
        await features.add(
            FeatureRecord(
                feature_set_version="fs-v0",
                market_class="forex",
                symbol="EURUSD",
                timeframe="H1",
                as_of=as_of,
                features={"ret_1": 0.01, "atr": 0.002},
            )
        )
        await models.add(
            ModelArtifact(
                name="baseline-gbm",
                version="0.0.1",
                status="registered",
                framework="lightgbm",
                supported_markets=["forex"],
                metrics={"auc": 0.55},
                artifact_uri="file://models/baseline-gbm-0.0.1",
            )
        )

    async with session_scope() as session:
        features = FeatureRepository(session)
        models = ModelArtifactRepository(session)
        rows = await features.list_for_symbol(symbol="EURUSD")
        assert len(rows) == 1
        model = await models.get_by_name_version("baseline-gbm", "0.0.1")
        assert model is not None
        assert model.status == "registered"


@pytest.mark.asyncio
async def test_audit_append(prepared_db: None) -> None:
    async with session_scope() as session:
        audit = AuditRepository(session)
        event = await audit.append(
            category="GOVERNANCE",
            action="test.event",
            message="repository integration audit",
            details={"unit": "W0-U02"},
        )
        assert event.id

    async with session_scope() as session:
        audit = AuditRepository(session)
        recent = await audit.list_recent(category="GOVERNANCE", limit=10)
        assert any(e.action == "test.event" for e in recent)
