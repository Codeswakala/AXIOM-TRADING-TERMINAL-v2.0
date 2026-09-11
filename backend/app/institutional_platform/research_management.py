"""Operator-scoped research management collections and tags (W7-U03)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import utc_now
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.correlation_report import CorrelationReport
from app.db.models.execution_experiment import ExecutionResearchExperiment
from app.db.models.execution_risk_report import ExecutionRiskResearchReport
from app.db.models.manual_trade_journal_entry import ManualTradeJournalEntryRecord
from app.db.models.portfolio_risk_report import PortfolioRiskReport
from app.db.models.regime_report import RegimeReport
from app.db.models.research_management import (
    ResearchCollection,
    ResearchCollectionMember,
    ResearchTag,
)
from app.db.models.scenario_report import ScenarioReport
from app.db.models.signal_validation_report import SignalValidationReport
from app.db.models.simulated_execution import SimulatedExecutionRun, SimulatedFillEvent
from app.db.models.simulated_execution_analytics_report import SimulatedExecutionAnalyticsReport
from app.db.models.simulated_paper_ledger import SimulatedPaperLedgerEntry
from app.db.models.trade_plan_note import TradePlanNoteRecord
from app.repositories.audit_repository import AuditRepository

RESEARCH_MANAGEMENT_STATUS = "research_only"

RESEARCH_MANAGEMENT_FORBIDDEN_FIELDS = {
    "order_payload",
    "order_intent",
    "broker_account_id",
    "account_id",
    "position_id",
    "live_position_id",
    "execution_status",
    "real_pnl",
    "pnl",
    "balance",
    "margin",
    "capital",
    "gate_state",
    "open_gate",
    "allow_execution",
    "source_artifact_content",
    "materialized_source_content",
}

RESEARCH_MANAGEMENT_SECRET_OR_PII_MARKERS = (
    "access_token",
    "refresh_token",
    "jwt",
    "password",
    "secret",
    "api_key",
    "private_key",
    "ssn",
    "social_security",
    "email_address",
    "phone_number",
)

ARTIFACT_ID_COLUMNS = {
    "advisory_signal": AdvisorySignal.signal_id,
    "correlation_report": CorrelationReport.id,
    "regime_report": RegimeReport.id,
    "scenario_report": ScenarioReport.id,
    "portfolio_risk_report": PortfolioRiskReport.id,
    "signal_validation_report": SignalValidationReport.id,
    "simulated_execution_run": SimulatedExecutionRun.run_id,
    "simulated_fill_event": SimulatedFillEvent.simulated_fill_id,
    "simulated_paper_ledger_entry": SimulatedPaperLedgerEntry.ledger_entry_id,
    "execution_risk_research_report": ExecutionRiskResearchReport.report_id,
    "execution_research_experiment": ExecutionResearchExperiment.experiment_id,
    "simulated_execution_analytics_report": SimulatedExecutionAnalyticsReport.report_id,
    "trade_plan_note": TradePlanNoteRecord.plan_id,
    "manual_trade_journal_entry": ManualTradeJournalEntryRecord.journal_id,
}


@dataclass(frozen=True, slots=True)
class ResearchCollectionDraft:
    name: str
    description: str | None


@dataclass(frozen=True, slots=True)
class ResearchArtifactReference:
    artifact_type: str
    artifact_id: str


@dataclass(frozen=True, slots=True)
class ResearchTagDraft:
    artifact_type: str
    artifact_id: str
    tag: str


class ResearchManagementFactory:
    """Validates reference-only research management payloads."""

    def collection_from_payload(self, payload: Mapping[str, Any]) -> ResearchCollectionDraft:
        allowed = {"name", "description"}
        self._assert_allowed(payload, allowed=allowed)
        name = self._clean_required_text(payload.get("name"), field="name", max_length=128)
        description = self._clean_optional_text(
            payload.get("description"), field="description", max_length=2000
        )
        self._assert_safe(name, path="research_collection.name")
        self._assert_safe(description, path="research_collection.description")
        return ResearchCollectionDraft(name=name, description=description)

    def member_from_payload(self, payload: Mapping[str, Any]) -> ResearchArtifactReference:
        allowed = {"artifact_type", "artifact_id"}
        self._assert_allowed(payload, allowed=allowed)
        return self._artifact_reference(payload, path="research_collection_member")

    def tag_from_payload(self, payload: Mapping[str, Any]) -> ResearchTagDraft:
        allowed = {"artifact_type", "artifact_id", "tag"}
        self._assert_allowed(payload, allowed=allowed)
        reference = self._artifact_reference(payload, path="research_tag")
        tag = self._clean_required_text(payload.get("tag"), field="tag", max_length=96)
        self._assert_safe(tag, path="research_tag.tag")
        return ResearchTagDraft(
            artifact_type=reference.artifact_type,
            artifact_id=reference.artifact_id,
            tag=tag,
        )

    def _artifact_reference(
        self, payload: Mapping[str, Any], *, path: str
    ) -> ResearchArtifactReference:
        artifact_type = self._clean_required_text(
            payload.get("artifact_type"), field="artifact_type", max_length=96
        )
        artifact_id = self._clean_required_text(
            payload.get("artifact_id"), field="artifact_id", max_length=96
        )
        self._assert_safe(artifact_type, path=f"{path}.artifact_type")
        self._assert_safe(artifact_id, path=f"{path}.artifact_id")
        if artifact_type not in ARTIFACT_ID_COLUMNS:
            raise ValueError(f"RESEARCH_MANAGEMENT_UNSUPPORTED_ARTIFACT_TYPE:{artifact_type}")
        return ResearchArtifactReference(artifact_type=artifact_type, artifact_id=artifact_id)

    def _assert_allowed(self, payload: Mapping[str, Any], *, allowed: set[str]) -> None:
        unknown = set(payload) - allowed
        for key in set(payload):
            if key in RESEARCH_MANAGEMENT_FORBIDDEN_FIELDS:
                raise ValueError(f"RESEARCH_MANAGEMENT_FORBIDDEN_FIELD:{key}")
        if unknown:
            raise ValueError(f"RESEARCH_MANAGEMENT_UNKNOWN_FIELD:{','.join(sorted(unknown))}")
        self._assert_safe(payload, path="research_management")

    def _clean_required_text(self, value: Any, *, field: str, max_length: int) -> str:
        if not isinstance(value, str):
            raise ValueError(f"RESEARCH_MANAGEMENT_TEXT_REQUIRED:{field}")
        text = value.strip()
        if not text:
            raise ValueError(f"RESEARCH_MANAGEMENT_TEXT_REQUIRED:{field}")
        if len(text) > max_length:
            raise ValueError(f"RESEARCH_MANAGEMENT_TEXT_TOO_LONG:{field}")
        return text

    def _clean_optional_text(
        self, value: Any, *, field: str, max_length: int
    ) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"RESEARCH_MANAGEMENT_TEXT_INVALID:{field}")
        text = value.strip()
        if not text:
            return None
        if len(text) > max_length:
            raise ValueError(f"RESEARCH_MANAGEMENT_TEXT_TOO_LONG:{field}")
        return text

    def _assert_safe(self, value: Any, *, path: str) -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                key_text = str(key)
                if key_text in RESEARCH_MANAGEMENT_FORBIDDEN_FIELDS:
                    raise ValueError(f"RESEARCH_MANAGEMENT_FORBIDDEN_FIELD:{path}.{key_text}")
                if any(
                    marker in key_text.lower()
                    for marker in RESEARCH_MANAGEMENT_SECRET_OR_PII_MARKERS
                ):
                    raise ValueError(f"RESEARCH_MANAGEMENT_SECRET_OR_PII_MARKER:{path}.{key_text}")
                self._assert_safe(nested, path=f"{path}.{key_text}")
        elif isinstance(value, list | tuple):
            for index, nested in enumerate(value):
                self._assert_safe(nested, path=f"{path}[{index}]")
        elif isinstance(value, str):
            lower = value.lower()
            if any(marker in lower for marker in RESEARCH_MANAGEMENT_SECRET_OR_PII_MARKERS):
                raise ValueError(f"RESEARCH_MANAGEMENT_SECRET_OR_PII_MARKER:{path}")


class ResearchManagementRepository:
    """Audited repository for reference-only research organization metadata."""

    method_version = "w7-u03.research_management.v1"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        self._factory = ResearchManagementFactory()

    async def create_collection(
        self, *, operator_id: str, payload: Mapping[str, Any]
    ) -> ResearchCollection:
        draft = self._factory.collection_from_payload(payload)
        existing = await self.get_collection_by_name(operator_id=operator_id, name=draft.name)
        if existing is not None:
            raise ValueError("RESEARCH_COLLECTION_ALREADY_EXISTS")
        now = utc_now()
        collection = ResearchCollection(
            collection_id=str(uuid4()),
            created_at=now,
            updated_at=now,
            operator_id=operator_id,
            name=draft.name,
            description=draft.description,
            research_status=RESEARCH_MANAGEMENT_STATUS,
            audit_correlation_id=str(uuid4()),
        )
        self._session.add(collection)
        await self._session.flush()
        await self._append_collection_audit(collection, action="research_collection.created")
        return collection

    async def delete_collection(self, *, collection_id: str, operator_id: str) -> bool:
        collection = await self.get_collection(collection_id=collection_id, operator_id=operator_id)
        if collection is None:
            return False
        members = await self.list_members(
            collection_id=collection_id,
            operator_id=operator_id,
            limit=500,
        )
        if members:
            raise ValueError("RESEARCH_COLLECTION_DELETE_REQUIRES_NO_MEMBERS")
        await self._session.delete(collection)
        await self._session.flush()
        await self._append_collection_audit(collection, action="research_collection.deleted")
        return True

    async def list_collections(
        self, *, operator_id: str, limit: int = 50
    ) -> Sequence[ResearchCollection]:
        stmt = (
            select(ResearchCollection)
            .where(ResearchCollection.operator_id == operator_id)
            .order_by(ResearchCollection.updated_at.desc())
            .limit(limit)
        )
        return list((await self._session.scalars(stmt)).all())

    async def get_collection(
        self, *, collection_id: str, operator_id: str
    ) -> ResearchCollection | None:
        stmt = select(ResearchCollection).where(
            ResearchCollection.collection_id == collection_id,
            ResearchCollection.operator_id == operator_id,
        )
        return (await self._session.scalars(stmt)).one_or_none()

    async def get_collection_by_id(self, *, collection_id: str) -> ResearchCollection | None:
        stmt = select(ResearchCollection).where(ResearchCollection.collection_id == collection_id)
        return (await self._session.scalars(stmt)).one_or_none()

    async def get_collection_by_name(
        self, *, operator_id: str, name: str
    ) -> ResearchCollection | None:
        stmt = select(ResearchCollection).where(
            ResearchCollection.operator_id == operator_id,
            ResearchCollection.name == name,
        )
        return (await self._session.scalars(stmt)).one_or_none()

    async def add_member(
        self, *, collection_id: str, operator_id: str, payload: Mapping[str, Any]
    ) -> ResearchCollectionMember:
        collection = await self.get_collection(collection_id=collection_id, operator_id=operator_id)
        if collection is None:
            raise ValueError("RESEARCH_COLLECTION_NOT_FOUND")
        reference = self._factory.member_from_payload(payload)
        if not await self.artifact_exists(
            artifact_type=reference.artifact_type, artifact_id=reference.artifact_id
        ):
            raise ValueError("RESEARCH_ARTIFACT_REFERENCE_NOT_FOUND")
        existing = await self.get_member_by_reference(
            collection_id=collection_id,
            operator_id=operator_id,
            artifact_type=reference.artifact_type,
            artifact_id=reference.artifact_id,
        )
        if existing is not None:
            raise ValueError("RESEARCH_COLLECTION_MEMBER_ALREADY_EXISTS")
        member = ResearchCollectionMember(
            member_id=str(uuid4()),
            created_at=utc_now(),
            operator_id=operator_id,
            collection_id=collection_id,
            artifact_type=reference.artifact_type,
            artifact_id=reference.artifact_id,
            audit_correlation_id=str(uuid4()),
        )
        self._session.add(member)
        await self._session.flush()
        await self._append_member_audit(member, action="research_collection_member.created")
        return member

    async def remove_member(
        self, *, collection_id: str, member_id: str, operator_id: str
    ) -> bool:
        member = await self.get_member(
            collection_id=collection_id, member_id=member_id, operator_id=operator_id
        )
        if member is None:
            return False
        await self._session.delete(member)
        await self._session.flush()
        await self._append_member_audit(member, action="research_collection_member.deleted")
        return True

    async def list_members(
        self, *, collection_id: str, operator_id: str, limit: int = 100
    ) -> Sequence[ResearchCollectionMember]:
        stmt = (
            select(ResearchCollectionMember)
            .where(
                ResearchCollectionMember.collection_id == collection_id,
                ResearchCollectionMember.operator_id == operator_id,
            )
            .order_by(ResearchCollectionMember.created_at.desc())
            .limit(limit)
        )
        return list((await self._session.scalars(stmt)).all())

    async def get_member(
        self, *, collection_id: str, member_id: str, operator_id: str
    ) -> ResearchCollectionMember | None:
        stmt = select(ResearchCollectionMember).where(
            ResearchCollectionMember.collection_id == collection_id,
            ResearchCollectionMember.member_id == member_id,
            ResearchCollectionMember.operator_id == operator_id,
        )
        return (await self._session.scalars(stmt)).one_or_none()

    async def get_member_by_reference(
        self,
        *,
        collection_id: str,
        operator_id: str,
        artifact_type: str,
        artifact_id: str,
    ) -> ResearchCollectionMember | None:
        stmt = select(ResearchCollectionMember).where(
            ResearchCollectionMember.collection_id == collection_id,
            ResearchCollectionMember.operator_id == operator_id,
            ResearchCollectionMember.artifact_type == artifact_type,
            ResearchCollectionMember.artifact_id == artifact_id,
        )
        return (await self._session.scalars(stmt)).one_or_none()

    async def create_tag(
        self, *, operator_id: str, payload: Mapping[str, Any]
    ) -> ResearchTag:
        draft = self._factory.tag_from_payload(payload)
        if not await self.artifact_exists(
            artifact_type=draft.artifact_type, artifact_id=draft.artifact_id
        ):
            raise ValueError("RESEARCH_ARTIFACT_REFERENCE_NOT_FOUND")
        existing = await self.get_tag_by_value(
            operator_id=operator_id,
            artifact_type=draft.artifact_type,
            artifact_id=draft.artifact_id,
            tag=draft.tag,
        )
        if existing is not None:
            raise ValueError("RESEARCH_TAG_ALREADY_EXISTS")
        tag = ResearchTag(
            tag_id=str(uuid4()),
            created_at=utc_now(),
            operator_id=operator_id,
            artifact_type=draft.artifact_type,
            artifact_id=draft.artifact_id,
            tag=draft.tag,
            audit_correlation_id=str(uuid4()),
        )
        self._session.add(tag)
        await self._session.flush()
        await self._append_tag_audit(tag, action="research_tag.created")
        return tag

    async def delete_tag(self, *, tag_id: str, operator_id: str) -> bool:
        tag = await self.get_tag(tag_id=tag_id, operator_id=operator_id)
        if tag is None:
            return False
        await self._session.delete(tag)
        await self._session.flush()
        await self._append_tag_audit(tag, action="research_tag.deleted")
        return True

    async def list_tags(
        self,
        *,
        operator_id: str,
        artifact_type: str | None = None,
        artifact_id: str | None = None,
        limit: int = 100,
    ) -> Sequence[ResearchTag]:
        stmt = select(ResearchTag).where(ResearchTag.operator_id == operator_id)
        if artifact_type is not None:
            stmt = stmt.where(ResearchTag.artifact_type == artifact_type)
        if artifact_id is not None:
            stmt = stmt.where(ResearchTag.artifact_id == artifact_id)
        stmt = stmt.order_by(ResearchTag.created_at.desc()).limit(limit)
        return list((await self._session.scalars(stmt)).all())

    async def get_tag(self, *, tag_id: str, operator_id: str) -> ResearchTag | None:
        stmt = select(ResearchTag).where(
            ResearchTag.tag_id == tag_id,
            ResearchTag.operator_id == operator_id,
        )
        return (await self._session.scalars(stmt)).one_or_none()

    async def get_tag_by_id(self, *, tag_id: str) -> ResearchTag | None:
        stmt = select(ResearchTag).where(ResearchTag.tag_id == tag_id)
        return (await self._session.scalars(stmt)).one_or_none()

    async def get_tag_by_value(
        self, *, operator_id: str, artifact_type: str, artifact_id: str, tag: str
    ) -> ResearchTag | None:
        stmt = select(ResearchTag).where(
            ResearchTag.operator_id == operator_id,
            ResearchTag.artifact_type == artifact_type,
            ResearchTag.artifact_id == artifact_id,
            ResearchTag.tag == tag,
        )
        return (await self._session.scalars(stmt)).one_or_none()

    async def artifact_exists(self, *, artifact_type: str, artifact_id: str) -> bool:
        id_column = ARTIFACT_ID_COLUMNS.get(artifact_type)
        if id_column is None:
            return False
        stmt = select(id_column).where(id_column == artifact_id).limit(1)
        return (await self._session.scalar(stmt)) is not None

    async def _append_collection_audit(
        self, collection: ResearchCollection, *, action: str
    ) -> None:
        event = await self._audit.append(
            category="GOVERNANCE",
            action=action,
            actor=collection.operator_id,
            resource_type="research_collection",
            resource_id=collection.collection_id,
            message=f"Research collection audited action={action}",
            details={
                "operator_id": collection.operator_id,
                "name": collection.name,
                "research_status": collection.research_status,
                "method_version": self.method_version,
                "reference_only": True,
                "source_artifact_mutated": False,
            },
            correlation_id=collection.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("RESEARCH_COLLECTION_AUDIT_FAILED")

    async def _append_member_audit(
        self, member: ResearchCollectionMember, *, action: str
    ) -> None:
        event = await self._audit.append(
            category="GOVERNANCE",
            action=action,
            actor=member.operator_id,
            resource_type="research_collection_member",
            resource_id=member.member_id,
            message=f"Research collection member audited action={action}",
            details={
                "operator_id": member.operator_id,
                "collection_id": member.collection_id,
                "artifact_type": member.artifact_type,
                "artifact_id": member.artifact_id,
                "method_version": self.method_version,
                "reference_only": True,
                "source_artifact_mutated": False,
            },
            correlation_id=member.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("RESEARCH_COLLECTION_MEMBER_AUDIT_FAILED")

    async def _append_tag_audit(self, tag: ResearchTag, *, action: str) -> None:
        event = await self._audit.append(
            category="GOVERNANCE",
            action=action,
            actor=tag.operator_id,
            resource_type="research_tag",
            resource_id=tag.tag_id,
            message=f"Research tag audited action={action}",
            details={
                "operator_id": tag.operator_id,
                "artifact_type": tag.artifact_type,
                "artifact_id": tag.artifact_id,
                "tag": tag.tag,
                "method_version": self.method_version,
                "reference_only": True,
                "source_artifact_mutated": False,
            },
            correlation_id=tag.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("RESEARCH_TAG_AUDIT_FAILED")
