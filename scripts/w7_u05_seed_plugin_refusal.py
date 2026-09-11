"""Seed W7-U05 hostile plugin-contract refusal evidence."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from sqlalchemy import func, select

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.models.audit import AuditEvent  # noqa: E402
from app.db.session import close_db, init_db, session_scope  # noqa: E402
from app.institutional_platform import (  # noqa: E402
    PLUGIN_CAPABILITY_ALLOWLIST,
    PluginContractRequest,
    PluginContractSafetyService,
)


async def main() -> None:
    init_db()
    async with session_scope() as session:
        service = PluginContractSafetyService(session)
        decision = await service.assess_request(
            operator_id="w7-u05-evidence-operator",
            request=PluginContractRequest(
                requested_contract_id="builtin.report_export.markdown.v1",
                requested_capability="report.export",
                requested_imports=(
                    "app.external_integration.broker",
                    "app.orders.dispatch",
                    "app.accounts.ledger",
                ),
                requested_data_scope="all_operators",
                writes_governed_artifact=True,
                reads_sensitive_material=True,
                network_access=True,
            ),
        )
        refusal_count = int(
            (
                await session.execute(
                    select(func.count())
                    .select_from(AuditEvent)
                    .where(
                        AuditEvent.resource_type == "plugin_contract_request",
                        AuditEvent.action == "plugin_contract_request.refused",
                        AuditEvent.correlation_id == decision.audit_correlation_id,
                    )
                )
            ).scalar_one()
        )
        print("W7_U05_PLUGIN_REFUSAL_SEED_COMPLETE")
        print(f"PLUGIN_REQUEST_ACCEPTED={decision.accepted}")
        print(f"PLUGIN_REFUSAL_REASON_CODE={decision.reason_code}")
        print(f"PLUGIN_REFUSAL_AUDIT_CORRELATION_ID={decision.audit_correlation_id}")
        print(f"PLUGIN_REFUSAL_AUDIT_COUNT={refusal_count}")
        print("PLUGIN_CAPABILITY_ALLOWLIST=" + ",".join(PLUGIN_CAPABILITY_ALLOWLIST))
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
