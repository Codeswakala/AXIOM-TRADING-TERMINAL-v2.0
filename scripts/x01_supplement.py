"""BO-X-01 supplement probe (DA evidence tooling, untracked).

Corrects three probe-execution defects discovered while reviewing the X-01
evidence logs — the platform behavior itself was not at fault:

  1. The main runner called GET /api/v1/observability/metrics (404). The
     observability router carries no `/observability` prefix; the correct
     path is GET /api/v1/metrics. Re-probed here (Level I).
  2. The main runner's "unauthenticated" assistant-respond call accidentally
     included the auth header (probe defect). Re-probed here with NO auth
     header — must be HTTP 401 (Level I).
  3. The main runner printed FeatureQualityReport objects as reprs. Re-queried
     here and printed as structured JSON (Level II), plus a feature-record
     sample and census.

Output: docs/evidence/x01/x01_supplement.log
"""

from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx
from sqlalchemy import func, select

BACKEND = Path(__file__).resolve().parents[1] / "backend"
EVIDENCE = BACKEND.parent / "docs" / "evidence" / "x01"
DB_URL = f"sqlite+aiosqlite:///{BACKEND / 'axiom_dev.db'}"
BASE = "http://127.0.0.1:8000"
API = "/api/v1"

sys.path.insert(0, str(BACKEND))

from app.core.config import Settings  # noqa: E402
from app.db.models.feature import FeatureRecord  # noqa: E402
from app.db.models.feature_definition import FeatureQualityReport  # noqa: E402
from app.db.session import get_session_factory, init_db  # noqa: E402

LINES: list[str] = []


def out(line: str = "") -> None:
    print(line)
    LINES.append(line)


def outj(label: str, obj) -> None:
    out(f"{label}: {json.dumps(obj, indent=2, default=str, sort_keys=True)}")


async def main() -> None:
    out(f"=== X-01 SUPPLEMENT PROBE (run start {datetime.now(timezone.utc).isoformat()}) ===")

    async with httpx.AsyncClient(timeout=120.0) as client:
        login = await client.post(f"{BASE}{API}/auth/login",
                                  json={"username": "admin",
                                        "password": "AxiomSecurePass2026!"})
        token = login.json()["tokens"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        out("---- correction 1: GET /api/v1/metrics (correct mount path) ----")
        resp = await client.get(f"{BASE}{API}/metrics", headers=headers)
        out(f"GET {API}/metrics: HTTP {resp.status_code}")
        body = resp.json()
        obs = body.get("observability", {})
        out(f"observability keys: {sorted(obs.keys()) if isinstance(obs, dict) else 'n/a'}")
        outj("pipelines-snapshot", obs.get("pipelines") if isinstance(obs, dict) else None)
        outj("resources-snapshot", obs.get("resources") if isinstance(obs, dict) else None)

        out("---- correction 2: assistant-respond WITHOUT auth header ----")
        resp = await client.post(
            f"{BASE}{API}/collaboration/assistant-respond",
            json={"prompt": "hi", "grounding_source_ids": []},
        )
        out(f"POST assistant-respond unauthenticated (no header): HTTP {resp.status_code} "
            f"body={resp.text[:200]}")

    init_db(Settings(database_url=DB_URL))
    factory = get_session_factory()
    async with factory() as session:
        out("---- correction 3: feature quality reports (structured) ----")
        rows = (await session.scalars(select(FeatureQualityReport))).all()
        out(f"feature_quality_reports: {len(rows)}")
        for r in rows:
            outj(f"quality-report[{r.id[:8]}]", {
                "id": r.id,
                "feature_set_version": r.feature_set_version,
                "source_dataset_hash": r.source_dataset_hash,
                "missing_rate": r.missing_rate,
                "drift_summary": r.drift_summary,
                "leakage_checks": r.leakage_checks,
                "stationarity_notes": r.stationarity_notes,
                "cross_market_compatibility": r.cross_market_compatibility,
                "content_hash": r.content_hash,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            })

        out("---- correction 3b: feature record sample + census ----")
        total = int((await session.execute(
            select(func.count()).select_from(FeatureRecord))).scalar_one())
        out(f"feature_records total: {total}")
        sample = (await session.scalars(
            select(FeatureRecord).order_by(FeatureRecord.recorded_at.desc()).limit(1))).first()
        if sample is not None:
            outj("sample feature record", {
                "id": sample.id,
                "feature_set_version": sample.feature_set_version,
                "market_class": sample.market_class,
                "provider": sample.provider,
                "symbol": sample.symbol,
                "timeframe": sample.timeframe,
                "as_of": sample.as_of.isoformat() if sample.as_of else None,
                "quality_score": sample.quality_score,
                "source": sample.source,
                "source_dataset_hash": sample.source_dataset_hash,
                "feature_names": sorted((sample.features or {}).keys()),
                "feature_values_excerpt": {
                    k: str(v) for k, v in list((sample.features or {}).items())[:6]},
            })

    out(f"=== supplement finished at {datetime.now(timezone.utc).isoformat()} ===")
    (EVIDENCE / "x01_supplement.log").write_text("\n".join(LINES) + "\n")
    print(f"supplement written to {EVIDENCE / 'x01_supplement.log'}")


if __name__ == "__main__":
    asyncio.run(main())
