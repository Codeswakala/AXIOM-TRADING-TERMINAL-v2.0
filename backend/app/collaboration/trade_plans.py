"""Inert trade plan note contracts and persistence (W5-U06)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.collaboration.contracts import COLLABORATION_FORBIDDEN_FIELDS
from app.core.time import utc_now
from app.db.models.trade_plan_note import TradePlanNoteRecord
from app.repositories.audit_repository import AuditRepository

TRADE_PLAN_RESEARCH_DISCLAIMER = (
    "Trade plan research note only. Hypothetical research, not financial advice, "
    "not a trade instruction, not an order ticket. Operator judgment required. "
    "AXIOM does not act."
)

TRADE_PLAN_ALLOWED_FIELDS = {
    "title",
    "market_context",
    "hypothesis",
    "linked_signal_ids",
    "linked_report_ids",
    "scenario_notes",
    "risk_notes",
    "invalidating_conditions_text",
    "decision_status",
}

TRADE_PLAN_DECISION_STATUSES = {"draft", "archived", "reviewed"}

_TRADE_PLAN_FORBIDDEN_TEXT = (
    "guaranteed return",
    "guaranteed profit",
    "expected return guaranteed",
)


@dataclass(frozen=True, slots=True)
class PersistentTradePlanDraft:
    """Validated operator-authored trade plan research note draft."""

    title: str
    market_context: str
    hypothesis: str
    linked_signal_ids: tuple[str, ...] = ()
    linked_report_ids: tuple[str, ...] = ()
    scenario_notes: str | None = None
    risk_notes: str | None = None
    invalidating_conditions_text: str | None = None
    decision_status: str = "draft"


class TradePlanNoteFactory:
    """Validates trade plan note payloads as inert research artifacts."""

    def draft_from_payload(self, payload: Mapping[str, Any]) -> PersistentTradePlanDraft:
        self.validate_payload(payload)
        return PersistentTradePlanDraft(
            title=self._required_text(payload, "title"),
            market_context=self._required_text(payload, "market_context"),
            hypothesis=self._required_text(payload, "hypothesis"),
            linked_signal_ids=self._string_tuple(payload.get("linked_signal_ids", ())),
            linked_report_ids=self._string_tuple(payload.get("linked_report_ids", ())),
            scenario_notes=self._optional_text(payload.get("scenario_notes")),
            risk_notes=self._optional_text(payload.get("risk_notes")),
            invalidating_conditions_text=self._optional_text(
                payload.get("invalidating_conditions_text")
            ),
            decision_status=str(payload.get("decision_status", "draft")),
        )

    def validate_payload(self, payload: Mapping[str, Any]) -> None:
        self._assert_inert(payload, path="trade_plan")
        self._assert_no_forbidden_text(payload, path="trade_plan")
        unknown = set(payload) - TRADE_PLAN_ALLOWED_FIELDS
        if unknown:
            raise ValueError(f"TRADE_PLAN_UNKNOWN_FIELD:{','.join(sorted(unknown))}")
        for field in ("title", "market_context", "hypothesis"):
            self._required_text(payload, field)
        status = str(payload.get("decision_status", "draft"))
        if status not in TRADE_PLAN_DECISION_STATUSES:
            raise ValueError("TRADE_PLAN_DECISION_STATUS_INVALID")
        self._string_tuple(payload.get("linked_signal_ids", ()))
        self._string_tuple(payload.get("linked_report_ids", ()))

    def _assert_inert(self, value: Any, *, path: str) -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                key_text = str(key)
                if key_text in COLLABORATION_FORBIDDEN_FIELDS:
                    raise ValueError(f"TRADE_PLAN_FORBIDDEN_FIELD:{path}.{key_text}")
                self._assert_inert(nested, path=f"{path}.{key_text}")
        elif isinstance(value, list | tuple):
            for index, nested in enumerate(value):
                self._assert_inert(nested, path=f"{path}[{index}]")

    def _assert_no_forbidden_text(self, value: Any, *, path: str) -> None:
        if isinstance(value, str):
            lower = value.lower()
            for marker in _TRADE_PLAN_FORBIDDEN_TEXT:
                if marker in lower:
                    raise ValueError(f"TRADE_PLAN_FORBIDDEN_TEXT:{path}")
        elif isinstance(value, Mapping):
            for key, nested in value.items():
                self._assert_no_forbidden_text(nested, path=f"{path}.{key}")
        elif isinstance(value, list | tuple):
            for index, nested in enumerate(value):
                self._assert_no_forbidden_text(nested, path=f"{path}[{index}]")

    def _required_text(self, payload: Mapping[str, Any], field: str) -> str:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"TRADE_PLAN_REQUIRED_FIELD:{field}")
        return value.strip()

    def _optional_text(self, value: Any) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("TRADE_PLAN_TEXT_FIELD_INVALID")
        return value.strip() or None

    def _string_tuple(self, value: Any) -> tuple[str, ...]:
        if value is None:
            return ()
        if not isinstance(value, list | tuple):
            raise ValueError("TRADE_PLAN_LINKED_IDS_INVALID")
        output: list[str] = []
        for item in value:
            if not isinstance(item, str) or not item.strip():
                raise ValueError("TRADE_PLAN_LINKED_IDS_INVALID")
            output.append(item.strip())
        return tuple(output)


class TradePlanNoteRepository:
    """Repository for audited, inert trade plan research notes."""

    method_version = "w5-u06.trade_plan_note.v1"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        self._factory = TradePlanNoteFactory()

    async def create_plan(
        self,
        *,
        payload: Mapping[str, Any],
        operator_id: str,
    ) -> TradePlanNoteRecord:
        draft = self._factory.draft_from_payload(payload)
        now = utc_now()
        plan = TradePlanNoteRecord(
            plan_id=str(uuid4()),
            created_at=now,
            updated_at=now,
            operator_id=operator_id,
            title=draft.title,
            market_context=draft.market_context,
            hypothesis=draft.hypothesis,
            linked_signal_ids=list(draft.linked_signal_ids),
            linked_report_ids=list(draft.linked_report_ids),
            scenario_notes=draft.scenario_notes,
            risk_notes=draft.risk_notes,
            invalidating_conditions_text=draft.invalidating_conditions_text,
            decision_status=draft.decision_status,
            research_disclaimer=TRADE_PLAN_RESEARCH_DISCLAIMER,
            research_status="research_only",
            audit_correlation_id=str(uuid4()),
        )
        self._session.add(plan)
        await self._session.flush()
        await self._append_audit(plan, action="trade_plan_note.created")
        return plan

    async def update_plan(
        self,
        *,
        plan_id: str,
        payload: Mapping[str, Any],
        operator_id: str,
    ) -> TradePlanNoteRecord | None:
        plan = await self.get_plan(plan_id)
        if plan is None:
            return None
        draft = self._factory.draft_from_payload(payload)
        plan.title = draft.title
        plan.market_context = draft.market_context
        plan.hypothesis = draft.hypothesis
        plan.linked_signal_ids = list(draft.linked_signal_ids)
        plan.linked_report_ids = list(draft.linked_report_ids)
        plan.scenario_notes = draft.scenario_notes
        plan.risk_notes = draft.risk_notes
        plan.invalidating_conditions_text = draft.invalidating_conditions_text
        plan.decision_status = draft.decision_status
        plan.updated_at = utc_now()
        await self._session.flush()
        await self._append_audit(plan, action="trade_plan_note.updated", actor=operator_id)
        return plan

    async def list_plans(self, *, limit: int = 50) -> Sequence[TradePlanNoteRecord]:
        stmt = (
            select(TradePlanNoteRecord)
            .order_by(TradePlanNoteRecord.updated_at.desc())
            .limit(limit)
        )
        return list((await self._session.scalars(stmt)).all())

    async def get_plan(self, plan_id: str) -> TradePlanNoteRecord | None:
        return await self._session.get(TradePlanNoteRecord, plan_id)

    async def _append_audit(
        self,
        plan: TradePlanNoteRecord,
        *,
        action: str,
        actor: str | None = None,
    ) -> None:
        event = await self._audit.append(
            category="GOVERNANCE",
            action=action,
            actor=actor or plan.operator_id,
            resource_type="trade_plan_note",
            resource_id=plan.plan_id,
            message=f"Trade plan research note audited action={action}",
            details={
                "plan_id": plan.plan_id,
                "decision_status": plan.decision_status,
                "research_status": plan.research_status,
                "linked_signal_ids": plan.linked_signal_ids,
                "linked_report_ids": plan.linked_report_ids,
                "method_version": self.method_version,
                "operator_authored": True,
                "ai_assisted": False,
                "disclaimer": plan.research_disclaimer,
            },
            correlation_id=plan.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("TRADE_PLAN_NOTE_AUDIT_FAILED")
