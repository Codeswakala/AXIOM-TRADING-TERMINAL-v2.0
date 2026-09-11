"""Operator-scoped workspace preferences (W7-U02)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import utc_now
from app.db.models.operator_workspace_preference import OperatorWorkspacePreference
from app.repositories.audit_repository import AuditRepository

PREFERENCE_RESEARCH_STATUS = "research_only"

WORKSPACE_PREFERENCE_FORBIDDEN_FIELDS = {
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
}

WORKSPACE_PREFERENCE_SECRET_MARKERS = (
    "access_token",
    "refresh_token",
    "jwt",
    "password",
    "secret",
    "api_key",
    "private_key",
)

ALLOWED_VISIBLE_MODULES = {
    "operations",
    "live_market",
    "advisory_signals",
    "performance_analytics",
    "institutional_intelligence",
    "chart_workspace",
    "signal_investigation",
    "scenario_comparison",
    "trade_planning",
    "research_journal",
    "execution_research",
}


@dataclass(frozen=True, slots=True)
class WorkspacePreferenceDraft:
    workspace_key: str
    layout_config: Mapping[str, Any]
    visible_modules: tuple[str, ...]
    theme_config: Mapping[str, Any]
    metadata: Mapping[str, Any] = field(default_factory=dict)


class WorkspacePreferenceFactory:
    """Validates presentation-only preference payloads."""

    def draft_from_payload(self, payload: Mapping[str, Any]) -> WorkspacePreferenceDraft:
        self.validate_payload(payload)
        return WorkspacePreferenceDraft(
            workspace_key=str(payload.get("workspace_key", "default")).strip(),
            layout_config=dict(payload.get("layout_config", {})),
            visible_modules=tuple(payload.get("visible_modules", ())),
            theme_config=dict(payload.get("theme_config", {})),
            metadata=dict(payload.get("metadata", {})),
        )

    def validate_payload(self, payload: Mapping[str, Any]) -> None:
        allowed = {"workspace_key", "layout_config", "visible_modules", "theme_config", "metadata"}
        unknown = set(payload) - allowed
        if unknown:
            raise ValueError(f"WORKSPACE_PREFERENCE_UNKNOWN_FIELD:{','.join(sorted(unknown))}")
        workspace_key = str(payload.get("workspace_key", "default")).strip()
        if not workspace_key:
            raise ValueError("WORKSPACE_PREFERENCE_KEY_REQUIRED")
        self._assert_json_mapping(payload.get("layout_config", {}), field="layout_config")
        self._assert_json_mapping(payload.get("theme_config", {}), field="theme_config")
        self._assert_json_mapping(payload.get("metadata", {}), field="metadata")
        modules = payload.get("visible_modules", ())
        if not isinstance(modules, list | tuple):
            raise ValueError("WORKSPACE_PREFERENCE_VISIBLE_MODULES_INVALID")
        for module in modules:
            if not isinstance(module, str) or module not in ALLOWED_VISIBLE_MODULES:
                raise ValueError("WORKSPACE_PREFERENCE_VISIBLE_MODULE_INVALID")
        self._assert_safe(payload, path="workspace_preference")

    def _assert_json_mapping(self, value: Any, *, field: str) -> None:
        if not isinstance(value, Mapping):
            raise ValueError(f"WORKSPACE_PREFERENCE_MAPPING_REQUIRED:{field}")

    def _assert_safe(self, value: Any, *, path: str) -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                key_text = str(key)
                if key_text in WORKSPACE_PREFERENCE_FORBIDDEN_FIELDS:
                    raise ValueError(f"WORKSPACE_PREFERENCE_FORBIDDEN_FIELD:{path}.{key_text}")
                if any(
                    marker in key_text.lower()
                    for marker in WORKSPACE_PREFERENCE_SECRET_MARKERS
                ):
                    raise ValueError(f"WORKSPACE_PREFERENCE_SECRET_MARKER:{path}.{key_text}")
                self._assert_safe(nested, path=f"{path}.{key_text}")
        elif isinstance(value, list | tuple):
            for index, nested in enumerate(value):
                self._assert_safe(nested, path=f"{path}[{index}]")
        elif isinstance(value, str):
            lower = value.lower()
            if any(marker in lower for marker in WORKSPACE_PREFERENCE_SECRET_MARKERS):
                raise ValueError(f"WORKSPACE_PREFERENCE_SECRET_MARKER:{path}")


class WorkspacePreferenceRepository:
    """Repository for audited, operator-scoped workspace preferences."""

    method_version = "w7-u02.workspace_preferences.v1"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)
        self._factory = WorkspacePreferenceFactory()

    async def create_preference(
        self,
        *,
        payload: Mapping[str, Any],
        operator_id: str,
    ) -> OperatorWorkspacePreference:
        draft = self._factory.draft_from_payload(payload)
        existing = await self.get_by_workspace_key(
            operator_id=operator_id, workspace_key=draft.workspace_key
        )
        if existing is not None:
            raise ValueError("WORKSPACE_PREFERENCE_ALREADY_EXISTS")
        now = utc_now()
        preference = OperatorWorkspacePreference(
            preference_id=str(uuid4()),
            created_at=now,
            updated_at=now,
            operator_id=operator_id,
            workspace_key=draft.workspace_key,
            layout_config=dict(draft.layout_config),
            visible_modules=list(draft.visible_modules),
            theme_config=dict(draft.theme_config),
            research_status=PREFERENCE_RESEARCH_STATUS,
            metadata_json=dict(draft.metadata),
            audit_correlation_id=str(uuid4()),
        )
        self._session.add(preference)
        await self._session.flush()
        await self._append_audit(preference, action="operator_workspace_preference.created")
        return preference

    async def update_preference(
        self,
        *,
        preference_id: str,
        payload: Mapping[str, Any],
        operator_id: str,
    ) -> OperatorWorkspacePreference | None:
        preference = await self.get_preference(preference_id=preference_id, operator_id=operator_id)
        if preference is None:
            return None
        draft = self._factory.draft_from_payload(payload)
        if draft.workspace_key != preference.workspace_key:
            raise ValueError("WORKSPACE_PREFERENCE_KEY_IMMUTABLE")
        preference.layout_config = dict(draft.layout_config)
        preference.visible_modules = list(draft.visible_modules)
        preference.theme_config = dict(draft.theme_config)
        preference.metadata_json = dict(draft.metadata)
        preference.updated_at = utc_now()
        await self._session.flush()
        await self._append_audit(preference, action="operator_workspace_preference.updated")
        return preference

    async def list_preferences(
        self, *, operator_id: str, limit: int = 50
    ) -> Sequence[OperatorWorkspacePreference]:
        stmt = (
            select(OperatorWorkspacePreference)
            .where(OperatorWorkspacePreference.operator_id == operator_id)
            .order_by(OperatorWorkspacePreference.updated_at.desc())
            .limit(limit)
        )
        return list((await self._session.scalars(stmt)).all())

    async def get_preference(
        self, *, preference_id: str, operator_id: str
    ) -> OperatorWorkspacePreference | None:
        stmt = select(OperatorWorkspacePreference).where(
            OperatorWorkspacePreference.preference_id == preference_id,
            OperatorWorkspacePreference.operator_id == operator_id,
        )
        return (await self._session.scalars(stmt)).one_or_none()

    async def get_preference_by_id(
        self, *, preference_id: str
    ) -> OperatorWorkspacePreference | None:
        stmt = select(OperatorWorkspacePreference).where(
            OperatorWorkspacePreference.preference_id == preference_id
        )
        return (await self._session.scalars(stmt)).one_or_none()

    async def get_by_workspace_key(
        self, *, operator_id: str, workspace_key: str
    ) -> OperatorWorkspacePreference | None:
        stmt = select(OperatorWorkspacePreference).where(
            OperatorWorkspacePreference.operator_id == operator_id,
            OperatorWorkspacePreference.workspace_key == workspace_key,
        )
        return (await self._session.scalars(stmt)).one_or_none()

    async def _append_audit(self, preference: OperatorWorkspacePreference, *, action: str) -> None:
        event = await self._audit.append(
            category="GOVERNANCE",
            action=action,
            actor=preference.operator_id,
            resource_type="operator_workspace_preference",
            resource_id=preference.preference_id,
            message=f"Operator workspace preference audited action={action}",
            details={
                "operator_id": preference.operator_id,
                "workspace_key": preference.workspace_key,
                "research_status": preference.research_status,
                "method_version": self.method_version,
                "presentation_only": True,
                "visible_modules": preference.visible_modules,
            },
            correlation_id=preference.audit_correlation_id,
        )
        if event is None:
            raise RuntimeError("WORKSPACE_PREFERENCE_AUDIT_FAILED")
