# DELIVERY REPORT — AXIOM V2 BE-2: Market Data Abstraction and Historical Data Integrity

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-2-DR-002 (supersedes DR-001) |
| Build Order | BO-V2-BE-2-001 |
| Governing plan | AXIOM-V2-BE-2-DA-PLAN-001 v2.0.0 (ITRGA-DET-V2-BE-2-PLAN-001 — APPROVED WITH OBSERVATIONS) |
| Date | 2026-08-24 |
| Author | Development Authority (DA) |
| Status | **CORRECTED AND RESUBMITTED** (CA response AXIOM-V2-BE-2-CAR-001 for ITRGA-REV-V2-BE-2-DELIVERY-001) — Operator PostgreSQL rerun outstanding against corrected source |
| Parent baseline | BE-1 approved head `20260823_0038` (ITRGA-DET-V2-BE-1-001) |
| BE-2 Alembic head | `20260824_0039` |
| Seed manifest hash | `1fd40c04cf89b83cb131a11092f1f86f0a264d499261cba59a3b10c777d03037` |

---

## 1. Executive Summary

BE-2 is implemented as authorized: a truthful, provider-neutral V2 read
boundary over existing V1 simulated/synthetic market data with canonical
identity, mandatory provenance, historical-integrity controls, idempotent
derived metadata behind an explicit two-writer boundary, and tamper-evident
(non-reconstructive) As-Of Verification Records.

DA verification after DEL-001…003 corrections: **675 tests executed, 675
passed, 0 failed** — 552 V1 + 78 BE-1 + 45 BE-2 (distinct, non-duplicated). V2 lint scope clean. SQLite
migration lifecycle fully evidenced. This is a submission for review, not an
approval. **PostgreSQL verification is Operator-run and outstanding** (§6).

## 2. Scope Delivered

| Build Order item | State |
|---|---|
| V2 market-data modules (contracts/provenance/identity/integrity/verification/repositories/models/APIs) | Implemented — `backend/app/v2/marketdata/**` |
| Six additive tables only | Implemented — `v2_md_instrument`, `v2_md_symbol_map`, `v2_md_source`, `v2_md_series`, `v2_md_integrity_exception`, `v2_md_asof_verification` |
| Versioned deterministic seed + manifest hash | Implemented — `seed.py`; hash above; DB-matches-manifest test |
| GET read APIs (persistence-pure) | Implemented — instruments, sources, series, bars, integrity exceptions, verification (operator/all/detail) |
| W-1 `POST /catalog/refresh` | Implemented — admin/SAL-3; idempotent upsert; fingerprint-deduplicated exceptions; audited with correlation ID |
| W-2 verification create/re-verify | Implemented — operator+admin/SAL-3; audited + lineage (`md_asof_verification`); mismatch exceptions first-detection-deduplicated |
| Provenance mapping of V1 data | Implemented — `live:simulated` / `seed:synthetic` / honest `unknown`; unrecognized markers disclosed, never auto-registered |
| SQLite migration/trigger/drift verification | Complete with literal evidence |
| PostgreSQL verification | **Outstanding — Operator-run** (command pack supplied) |
| Unit/integration/security/failure-path/V1-regression testing | Complete — 42 BE-2 tests; full suite green |
| Audit/lineage/state/register/Delivery Report updates | Complete this cycle |

### Constraint compliance (BO §3, 1–11)

1. No provider connection/claim — no such code path exists. 2. Active
authority emission bounded by guard + DB CHECK + tests to
`seed:synthetic`/`live:simulated`/`unknown`. 3. V1 candles/services/APIs
untouched (read-only wrap). 4. No bar payload copied/written. 5.
`reconstructive: false` + `capability: "verification-only"` on every
verification response. 6. GETs persistence-pure (5× repetition test, zero
mutations); sole exception is BE-1-pattern sensitive-read audit on
`/verification/all`. 7. W-1/W-2 sole writers — authenticated, mode-gated,
audited, transaction-bounded, idempotent. 8. Fingerprint dedup proven at
DB-UNIQUE and API-re-run levels. 9. All V2 times aware-UTC; naive inputs
rejected; SQLite store-read normalization documented (dialect artifact, not
input coercion). 10. No excluded scope entered. 11. **No DA Git operation.**

## 3. Implementation Inventory

**New (15 files):** `app/db/models/v2_marketdata.py`; `app/v2/marketdata/`
(`provenance.py`, `seed.py`, `identity` logic folded into seed/provenance,
`integrity.py`, `verification.py`, `repositories.py`, `models.py`,
`api/reads.py`, `api/writers.py`, `api/router.py`, package inits);
`alembic/versions/20260824_0039_v2_be2_marketdata.py`;
`tests/test_v2_marketdata.py` (29 unit); `tests/test_v2_marketdata_integration.py` (13 integration).

**Modified (5 files):** `app/db/models/__init__.py` (Alembic metadata imports
— PG-002 lesson); `app/v2/rbac/permissions.py` + `dependencies.py` (4 new
permissions; vocabulary guard passes); `app/v2/api/router.py` (mount);
`tests/test_v2_integration.py` (BE-1 lifecycle assertions scoped to BE-1
objects — bounded, documented).

Full SHA-256 manifest + literal contents of **every** changed file (REM-001
policy): `docs/evidence/V2_BE-2_SOURCE_TRANSCRIPT.md`.

## 4. Verification

| Check | Result |
|---|---|
| Full suite `pytest tests/ -q` | **675 passed, 0 failed** (3:40, post-correction) |
| All V2 `pytest tests/test_v2_*.py -q` | **123 passed** (78 BE-1 + 45 BE-2) |
| BE-2 only | **45 passed** (30 unit + 15 integration) |
| V2 lint | All checks passed |
| SQLite lifecycle | upgrade→tables/triggers/seeds→CHECK refusal→mutation refusal (both tables, both verbs)→**zero v2_md drift**→downgrade (clean removal incl. permissions; BE-1 intact)→re-upgrade — all exit 0 |

Key security behaviors proven at API level: two-operator verification
isolation (404 without disclosure), admin `read_all` + persisted sensitive-read
audit, default-deny for unprivileged role on all endpoints, generic
`Permission denied` with no vocabulary leak, future-`as_of` refusal, honest
`empty`/`partial` availability with gaps disclosed and never filled, and the
tamper-detection lifecycle (V1 row mutated → hash mismatch detected → repeat
re-verification deduplicated to a single exception record).

## 5. Observations Compliance

- **OBS-V2-BE2-01:** retention values remain development design values; no
  production retention claim made.
- **OBS-V2-BE2-02:** verification-only limitation is visible in the schema
  docstring, response models (`reconstructive`/`capability` fields), tests,
  and this report. BE-2 provides no reproducible snapshot capability.
- **OBS-V2-BE1-03:** BE-2 changes migration/models/metadata → PostgreSQL
  rerun is mandatory (§6).

## 6. Known Limitations / Open Items

1. **Operator PostgreSQL verification outstanding** — fresh dedicated DB;
   command pack in `V2_BE-2_EVIDENCE.md` §4 (upgrade, 6 tables, 2 triggers +
   2 functions, seeds, native mutation refusal, CHECK refusal, drift,
   downgrade removal, re-upgrade). Final BE-2 closure blocks on this evidence.
2. App-level API tests ran on SQLite; PostgreSQL app-level pass optional per
   plan (registered debt V2-TD-07 pattern).
3. Freshness/gap computation is read-time; scheduled catalog verification
   remains deferred to the job band (registered).
4. Inherited V1 lint/drift debt unchanged.

## 7. Handover

| Item | State |
|---|---|
| Workspace | `/home/user/axiom` — implementation complete, suite green |
| Evidence | `docs/evidence/V2_BE-2_SOURCE_TRANSCRIPT.md`, `docs/evidence/V2_BE-2_EVIDENCE.md`, **`docs/evidence/V2_BE-2_CA_RESPONSE_DELIVERY-001.md`** (DEL-001…003 closures, corrected-file transcript, regenerated migration evidence) |
| State docs | `V2_CURRENT_STATE.md` v8.0.0; Risk/Debt registers updated |
| Git | No DA Git operation; publication remains Operator post-approval custody |
| Next actions | (1) Operator runs PostgreSQL pack → returns evidence; (2) ITRGA review; (3) BE-2 does not authorize BE-3 |

**We don't guess. We prove.**

**End of Delivery Report AXIOM-V2-BE-2-DR-001**
