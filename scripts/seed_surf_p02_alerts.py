"""Seed script for SURF-P02 Level-I served evidence data.

Creates three monitoring alerts across the three severity Literals via the
existing MonitoringAlertService.create_alert seam — the same service the
backend uses for real alert records. One alert is acknowledged, two are not,
so the rail badge renders a genuine unread count of 2.

This is an EVIDENCE FIXTURE (deviation register row
TD-UI-CONV-P03-EVIDENCE-FIXTURE family): it writes read-only alert records
and their audit rows into the development database only. No schema, endpoint
or model change.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.db.session import init_db, session_scope
from app.trading_intelligence.monitoring import MonitoringAlertService


async def seed_data() -> None:
    init_db()
    async with session_scope() as session:
        service = MonitoringAlertService(session)

        critical = await service.create_alert(
            alert_type="LIVE_DATA_STALE",
            severity="critical",
            subject_type="market",
            subject_id="EURUSD",
            market_class="forex",
            symbol="EURUSD",
            summary="Market data feed gap detected during the observed window.",
            evidence={"stale_seconds": 30, "observed_window": "w3-u06-fixture"},
            lineage={"source": "surf_p02_evidence_fixture"},
            actor="surf-p02-seed",
            audit_correlation_id="surf-p02-seed-critical",
        )

        warning = await service.create_alert(
            alert_type="DRIFT_DETECTED",
            severity="warning",
            subject_type="model_artifact",
            subject_id="model.eurusd.classifier",
            model_artifact_id="model.eurusd.classifier",
            summary="Drift monitoring evidence requires operator review.",
            evidence={"drift_detected": True, "ks_statistic": 0.31},
            lineage={"source": "surf_p02_evidence_fixture"},
            actor="surf-p02-seed",
            audit_correlation_id="surf-p02-seed-warning",
        )

        info = await service.create_alert(
            alert_type="INFERENCE_HEALTH_DEGRADED",
            severity="info",
            subject_type="advisory_signal",
            subject_id="sig-fixture",
            summary="Inference health note recorded for operator visibility.",
            evidence={"health_note": "fixture"},
            lineage={"source": "surf_p02_evidence_fixture"},
            actor="surf-p02-seed",
            audit_correlation_id="surf-p02-seed-info",
        )

        acknowledged = await service.acknowledge_alert(critical.alert_id, actor="surf-p02-seed")

        print("critical:", critical.alert_id, "acknowledged:", acknowledged.acknowledged)
        print("warning:", warning.alert_id)
        print("info:", info.alert_id)


if __name__ == "__main__":
    asyncio.run(seed_data())
