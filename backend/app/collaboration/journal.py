"""Inert manual research journal contracts and persistence (W5-U07)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.collaboration.contracts import COLLABORATION_FORBIDDEN_FIELDS
from app.core.time import utc_now
from app.db.models.manual_trade_journal_entry import ManualTradeJournalEntryRecord
from app.repositories.audit_repository import AuditRepository

JOURNAL_RESEARCH_DISCLAIMER = (
    "Manual research journal entry only. Not financial advice, not a trade record, "
    "not a trade instruction. Operator judgment required. AXIOM does not act."
)

JOURNAL_ALLOWED_FIELDS = {
    "title",
    "reflection_text",
    "linked_plan_id",
    "linked_signal_ids",
    "linked_report_ids",
    "emotion_tags",
    "process_tags",
    "lesson_notes",
}

JOURNAL_FORBIDDEN_FIELDS = COLLABORATION_FORBIDDEN_FIELDS | {
    "broker_import",
    "broker_trade_id",
    "broker_order_id",
    "execution_id",
    "fill_id",
    "fill_price",
    "fill_quantity",
    "fill_timestamp",
    "pnl",
    "p_and_l",
    "profit_loss",
    "realized_pnl",
    "realized_return",
    "account_balance",
}

_JOURNAL_FORBIDDEN_TEXT = (
    "broker import",
    "execution id",
    "fill price",
    "realized return",
    "realized pnl",
    "p&l",
    "profit and loss",
    "guaranteed return",
    "guaranteed profit",
)


@dataclass(frozen=True, slots=True)
class ManualJournalEntryDraft:
    """Validated operator-authored manual research journal draft."""

    title: str
    reflection_text: str
    linked_plan_id: str | None = None
    linked_signal_ids: tuple[str, ...] = ()
    linked_report_ids: tuple[str, ...] = ()
    emotion_tags: tuple[str, ...] = ()
    process_tags: tuple[str, ...] = ()
    lesson_notes: str | None = None


class ManualJournalEntryFactory:
    """Validates manual journal payloads as inert research logs."""

    def draft_from_payload(self, payload: Mapping[str, Any]) -> ManualJournalEntryDraft:
        self.validate_payload(payload)
        return ManualJournalEntryDraft(
            title=self._required_text(payload, "title"),
            reflection_text=self._required_text(payload, "reflection_text"),
            linked_plan_id=self._optional_text(payload.get("linked_plan_id")),
            linked_signal_ids=self._string_tuple(payload.get("linked_signal_ids", ())),
            linked_report_ids=self._string_tuple(payload.get("linked_report_ids", ())),
            emotion_tags=self._string_tuple(payload.get("emotion_tags", ())),
            process_tags=self._string_tuple(payload.get("process_tags", ())),
            lesson_notes=self._optional_text(payload.get("lesson_notes")),
        )

    def validate_payload(self, payload: Mapping[str, Any]) -> None:
        self._assert_inert(payload, path="journal")
        self._assert_no_forbidden_text(payload, path="journal")
        unknown = set(payload) - JOURNAL_ALLOWED_FIELDS
        if unknown:
            raise ValueError(f"JOURNAL_UNKNOWN_FIELD:{','.join(sorted(unknown))}")
        for field in ("title", "reflection_text"):
            self._required_text(payload, field)
        self._optional_text(payload.get("linked_plan_id"))
        for field in ("linked_signal_ids", "linked_report_ids", "emotion_tags", "process_tags"):
            self._string_tuple(payload.get(field, ()))
        self._optional_text(payload.get("lesson_notes"))

    def _assert_inert(self, value: Any, *, path: str) -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                key_text = str(key)
                if key_text in JOURNAL_FORBIDDEN_FIELDS:
                    raise ValueError(f"JOURNAL_FORBIDDEN_FIELD:{path}.{key_text}")
                self._assert_inert(nested, path=f"{path}.{key_text}")
        elif isinstance(value, list | tuple):
            for index, nested in enumerate(value):
                self._assert_inert(nested, path=f"{path}[{index}]")

    def _assert_no_forbidden_text(self, value: Any, *, path: str) -> None:
        if isinstance(value, str):
            lower = value.lower()
            for marker in _JOURNAL_FORBIDDEN_TEXT:
                if marker in lower:
                    raise ValueError(f"JOURNAL_FORBIDDEN_TEXT:{path}")
        elif isinstance(value, Mapping):
            for key, nested in value.items():
                self._assert_no_forbidden_text(nested, path=f"{path}.{key}")
        elif isinstance(value, list | tuple):
            for index, nested in enumerate(value):
                self._assert_no_forbidden_text(nested, path=f"{path}[{index}]")

    def _required_text(self, payload: Mapping[str, Any], field: str) -> str:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"JOURNAL_REQUIRED_FIELD:{field}")
        return value.strip()

    def _optional_text(self, value: Any) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("JOURNAL_TEXT_FIELD_INVALID")
        return value.strip() or None

    def _string_tuple(self, value: Any) -> tuple[str, ...]:
        if value is None:
            return ()
        if not isinstance(value, list | tuple):
            raise ValueError("JOURNAL_TAG_OR_LINK_FIELD_INVALID")
        output: list[str] = []
        for item in value:
            if not isinstance(item, str) or not item.strip():
                raise ValueError("JOURNAL_TAG_OR_LINK_FIELD_INVALID")
            output.append(item.strip())
        return tuple(output)


class ManualJournalEntryRepository:
    """Repository for audited, inert manual research journal entries."""

    method_version = "w5-u07.manual_journal_entry.v1"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        self._factory = ManualJournalEntryFactory()

    async def create_entry(
        self,
        *,
        payload: Mapping[str, Any],
        operator_id: str,
    ) -> ManualTradeJournalEntryRecord:
        draft = self._factory.draft_from_payload(payload)
        entry = ManualTradeJournalEntryRecord(
            journal_id=str(uuid4()),
            created_at=utc_now(),
            operator_id=operator_id,
            title=draft.title,
            reflection_text=draft.reflection_text,
            linked_plan_id=draft.linked_plan_id,
            linked_signal_ids=list(draft.linked_signal_ids),
            linked_report_ids=list(draft.linked_report_ids),
            emotion_tags=list(draft.emotion_tags),
            process_tags=list(draft.process_tags),
            lesson_notes=draft.lesson_notes,
            research_disclaimer=JOURNAL_RESEARCH_DISCLAIMER,
            research_status="research_only",
            audit_correlation_id=str(uuid4()),
        )
        self._session.add(entry)
        await self._session.flush()
        await self._append_audit(entry, action="manual_trade_journal_entry.created")
        return entry

    async def update_entry(
        self,
        *,
        journal_id: str,
        payload: Mapping[str, Any],
        operator_id: str,
    ) -> ManualTradeJournalEntryRecord | None:
        entry = await self.get_entry(journal_id)
        if entry is None:
            return None
        draft = self._factory.draft_from_payload(payload)
        entry.title = draft.title
        entry.reflection_text = draft.reflection_text
        entry.linked_plan_id = draft.linked_plan_id
        entry.linked_signal_ids = list(draft.linked_signal_ids)
        entry.linked_report_ids = list(draft.linked_report_ids)
        entry.emotion_tags = list(draft.emotion_tags)
        entry.process_tags = list(draft.process_tags)
        entry.lesson_notes = draft.lesson_notes
        await self._session.flush()
        await self._append_audit(
            entry,
            action="manual_trade_journal_entry.updated",
            actor=operator_id,
        )
        return entry

    async def list_entries(self, *, limit: int = 50) -> Sequence[ManualTradeJournalEntryRecord]:
        stmt = (
            select(ManualTradeJournalEntryRecord)
            .order_by(ManualTradeJournalEntryRecord.created_at.desc())
            .limit(limit)
        )
        return list((await self._session.scalars(stmt)).all())

    async def get_entry(self, journal_id: str) -> ManualTradeJournalEntryRecord | None:
        return await self._session.get(ManualTradeJournalEntryRecord, journal_id)

    async def _append_audit(
        self,
        entry: ManualTradeJournalEntryRecord,
        *,
        action: str,
        actor: str | None = None,
    ) -> None:
        event = await self._audit.append(
            category="GOVERNANCE",
            action=action,
            actor=actor or entry.operator_id,
            resource_type="manual_trade_journal_entry",
            resource_id=entry.journal_id,
            message=f"Manual research journal entry audited action={action}",
            details={
                "journal_id": entry.journal_id,
                "linked_plan_id": entry.linked_plan_id,
                "linked_signal_ids": entry.linked_signal_ids,
                "linked_report_ids": entry.linked_report_ids,
                "research_status": entry.research_status,
                "method_version": self.method_version,
                "operator_authored": True,
                "ai_assisted": False,
                "disclaimer": entry.research_disclaimer,
            },
            correlation_id=entry.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("MANUAL_JOURNAL_ENTRY_AUDIT_FAILED")
