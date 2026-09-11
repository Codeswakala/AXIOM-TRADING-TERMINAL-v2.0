# DOC12 — X-01 END-TO-END PLATFORM VERIFICATION (BACKEND TIER)

| Item | Value |
|------|-------|
| Build Order | `BO-X-01` (Operator-authorized 2026-08-20, "review and final backend build order") |
| Tier executed | **X-01 Backend Tier** — the complete operator workflow at the API/data level (BO §0) |
| Tier deferred | X-01 Terminal Tier — the full UI click-through, after frontend units F-01 → F-06 |
| Executor | Development Authority (DA) |
| Date of execution | 2026-08-21 |
| Platform state | AXIOM v0.62.0, dev environment, sqlite dev DB, baseline `34f4c62` + 28-element patch chain |
| Corpus | B-DATA real corpus — 12 files, 109,326 bars (6× OKX H1 17,520 bars + 6× Kraken D1 701 bars) |
| Code changes | **None.** This was a verification order (BO §3, §6). No platform file was modified. |
| Evidence | `docs/evidence/x01/` — per-hop Level-I/II logs, all captured mechanically |
| Posture | Gate CLOSED · Production NOT CERTIFIED (unchanged; X-01 evidences, it does not certify) |

---

## 1. Scope claimed vs. the Build Order

BO-X-01 §2 defines eight workflow hops; §3 exclusions were honored; §4 deliverables
produced; §6 "no code changes" held; §8 acceptance criteria addressed below; §9
evidence classes produced. The only repo-file delta of the entire unit is three
documentary files (this report, the Doc 11 inventory section, the technical-debt
register rows) — carried in `x01.patch.txt`, which contains **zero code files**.

## 2. The eight-hop walk — per-hop evidence

### Hop 1 — Market data
- Corpus integrity: all 12 CSV files sha256-verified against the B-DATA `MANIFEST.json`
  (MANIFEST sha256 `2a2c09217e2bc450885ee9dfebc6943083caabfb0193a3684706c23dfa8bed4b`), 12/12 OK,
  109,326 declared bars.
- Ingestion through the operator API: `POST /api/v1/ingestion/csv` × 12
  (`source=historical:real`) — every run `status=completed`, zero invalid rows,
  **109,326 bars inserted** (`x01_hop1.log`).
- `GET /api/v1/ingestion/runs` (12 runs), `GET /api/v1/ingestion/stats`, `/candle-counts` — non-zero.
- `market_series_metadata` (Level-II read): **12 rows, 12/12 `source_authority=AUTHORITATIVE`**,
  role `governance_evaluation_only` — authority granted only for `historical:real` (B-DATA rule).
- Security-headers continuity observed on the first authenticated response
  (`nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy`, restrictive CSP).

### Hop 2 — Chart / structural analysis
- `GET /api/v1/persistence/indicator-series?symbol=BTCUSDT&timeframe=H1` with the
  SMC/ICT structural set — **SWINGS55, STRUCT55, BOS55, CHOCH55, FVG3** (plus SMA20
  control) — all `shape=multi`/`line`, computed server-side over the real series
  (`seriesKind=native`, 17,520-bar source).
- **Determinism:** two consecutive identical requests produced **byte-identical JSON**.
- Unknown registry id → HTTP 422 (`Unknown indicator(s): NOTREAL`) — never silently dropped.
- No ML dependency: static scan of `app/services/indicators.py` + `market_structure.py`
  finds **zero** ML-framework imports (`x01_nonetwork_scan.log`).

### Hop 3 — Research artifacts
- Dataset snapshot `ds-x01-okx-h1` v1 over all 6 OKX H1 series (105,120 canonical records,
  `source=historical:real`): **status=frozen, tier=`research_validation`,
  authoritative_only=True** (persisted in `source_policy`), content_hash `c379f0e9…`.
- Temporal split manifest `split-x01-okx-h1`: train 63,072 / validation 21,024 /
  test 21,024 (60/20/20, label_horizon 1, embargo 1), split_hash `30355f4f…`.
- Feature store: **105,120 feature records** computed at tier `research_validation`
  (v1+v2 builtin set), 6 feature-quality reports (missing rates, leakage checks,
  drift summaries) and 11 feature definitions persisted (`x01_hop3.log`,
  `x01_supplement.log` correction 3/3b).
- No model training invoked (BO §3): zero `experiments`/`validation_reports`/
  `calibration_reports` rows written (hop-8 census).

### Hop 4 — Intelligence (five B-04 families)
Over the real OKX H1 window (2024-08-01 … 2026-07-31):
| Family | POST | Result |
|---|---|---|
| correlation | 201 | id `3ad23eb4…`, r=0.7321, n=17,520, fisher-z CI [0.7252, 0.7389], notes carry `data-class: historical:real`, economic_usefulness `not_assessed` |
| regime | 201 | id `cc48b8e3…`, label `calm`, confidence 0.605, threshold-margin uncertainty band, `data-class: historical:real` |
| scenario | 201 | id `46c656cd…`, hypothetical-shock research, `data-class: historical:real` |
| portfolio-risk | 201 | id `c81e1f75…`, hypothetical market-series risk, `data-class: historical:real` |
| signal-validation | 201 | id `43b4fee3…`, n=1 over the persisted withheld advisory signal, Wilson-95% uncertainty, `outcome_data_status=not_available` (honest), data-class declared per validation_scope |

- Honest insufficient-data path: correlation against an absent series → structured
  422 `{"error_code":"CORRELATION_REQUIRES_THREE_ALIGNED_POINTS","insufficient_data":true}`.
- GET read-back for all five families (rows present, notes carry the data-class label).
- Full responses in `x01_hop4.log` (6.6 MB; per-bar payloads), transmission digest in
  `x01_hop4_digest.log` (mechanical filter, disclosed in its header).

### Hop 5 — Alerts
- Conditions seeded and disclosed: a `live:simulated` candle 3h stale (via the
  operator `POST /api/v1/persistence/candles` API), a persisted drift record
  (`drift_detected=True`), a persisted withheld advisory signal (the same fixture
  validated in hop 4). Seeding constructors are byte-identical to the B-05
  test-proven fixtures.
- `POST /api/v1/alerts/check` #1: **stale 1 / drift 1 / withheld 1** emitted
  (11 symbols checked, threshold 3600s, cooldown 86400s).
- `POST /api/v1/alerts/check` #2 inside the cooldown: **0 / 0 / 0 — dedup proven**.
- `POST /api/v1/alerts/inference-health` (degraded) → 200 + `audit_correlation_id`;
  immediate repeat → **409** (cooldown); `status=ok` → **422** (schema boundary).
- Ack read-state-only: full row captured before/after `POST /alerts/{id}/ack` —
  the **only** changed fields are `{acknowledged, acknowledged_at, acknowledged_by}`.
- `GET /api/v1/alerts` read-back: 4 inert alerts, exactly one acknowledged.

### Hop 6 — Assistant
- **Grounded ask** over the real-corpus correlation report (id `3ad23eb4…`):
  `refused=false`, `grounding_summary="Correlation BTCUSDT/ETHUSDT r=0.7321 n=17520"`,
  persisted with `provenance.external_llm_used=false`, `raw_request_text_stored=false`,
  `provider_name=local_rule_based` (`rule_based_grounded_assistant.v1`).
- **All four refusal classes exercised and persisted:** `ORDER_INSTRUCTION_REFUSED`,
  `GATE_OPEN_INSTRUCTION_REFUSED`, `SECRET_EXFILTRATION_REFUSED`,
  `UNBOUNDED_TOOL_REQUEST_REFUSED`.
- **Empty grounding** (no ids) → `GROUNDING_REQUIRED`; **unknown ids only** →
  `GROUNDING_REQUIRED` with `source_artifact_ids: []` (nothing invented).
- Unauthenticated ask → **HTTP 401** (`x01_supplement.log` correction 2 — the main
  runner's first attempt had accidentally attached the auth header; the platform
  was always correct).
- GET read-back: 8 persisted rows, `external_llm_used=False` on every row (Level-II).

### Hop 7 — Governance & evidence
- `GET /api/v1/persistence/audit-events`: 38 rows — SECURITY 7 / GOVERNANCE 18 /
  DATABASE 1 / MARKET 12; **18 rows carry correlation ids** (Level-II query).
- `GET /api/v1/metrics` (correction 1): `observability.pipelines` counters match the
  run exactly — `market.ingestion_requested=12`, `intelligence.*_report_generated`
  per family, `monitoring.alert_check_executed=2`, `inference_health_reported=3`,
  `assistant.ask_responded=8` — plus `resources` rusage (CPU/maxrss).
- Server log (`x01_server_log.log`): every request line carries a `cid=…`;
  `Pipeline event category=… action=… cid=…` lines present for assistant/monitoring.
- `GET /api/v1/system/info` — AXIOM 0.62.0, Wave 7 closeout identity.
- `GET /api/v1/institutional-platform/route-inventory` —
  **`actuation_surface_present: false`**, `governance_gate_capability_present: false`.
- `GET /api/v1/institutional-platform/rbac/permissions` — policy `default_deny`,
  **`forbidden_capabilities_present: false`**.
- Doc 11 evidence inventory updated to reflect this executed evidence (patch file),
  closing statement unchanged: Gate CLOSED · Production NOT CERTIFIED.

### Hop 8 — Non-actuation, end-to-end
- Table census diff across the executed hop window (baseline captured after
  ingestion + disclosed fixture seeding, before any hop): **17 of 43 tables
  changed — every one inert or research** (audit_events, intelligence reports,
  dataset/split/feature/quality tables, monitoring_alerts, assistant_research_
  responses, candles +1 stale fixture, refresh_tokens from logins).
- Every actuation-adjacent table **zero delta**: `simulated_execution_runs`,
  `simulated_fill_events`, `simulated_paper_ledger_entries`,
  `execution_research_experiments`, `execution_risk_research_reports`,
  `simulated_execution_analytics_reports`, `trade_plan_notes`,
  `manual_trade_journal_entries` — all 0 → 0. No orders/brokers/accounts tables exist.
- Readiness dispositions (test-pinned): `RATE_GUARD_DISPOSITION.status=implemented`;
  admin-default-credential disposition `rejected_when_insecure_dev_off`.
- **No external network calls:** static scan across every module exercised by the
  hops (indicator/market-structure, institutional intelligence, monitoring,
  collaboration, ml/dataset, ml/features) finds **zero** outbound network-client
  imports; a platform-wide control scan of `app/` finds zero `httpx`/`aiohttp`/
  `requests`/`socket` imports in platform code at all (`x01_nonetwork_scan.log`).
  Assistant rows carry `external_llm_used=false`; no ML harness was invoked.

## 3. Non-actuation + no-external-calls summary

| Control | Evidence | Result |
|---|---|---|
| No order/broker/account/execution mutation | Hop-8 table delta census (all actuation-adjacent 0 → 0); route-inventory `actuation_surface_present: false` | **Held** |
| No gate/governance mutation | RBAC vocabulary `forbidden_capabilities_present: false`; no governance-capability route exists; register posture unchanged | **Held** |
| No external LLM | `external_llm_used: false` persisted on every assistant row; provider `local_rule_based` | **Held** |
| No ML training | No experiment/validation/calibration/model rows written in the hop window | **Held** |
| No outbound network clients | Static scan of exercised modules + platform-wide control scan: zero matches | **Held** |
| Research-only tiers respected | Snapshot/features persisted at `research_validation`, authoritative-only | **Held** |

## 4. Gap list (honest, per BO §4.3)

1. **Terminal Tier dependency** — a terminal-level UI click-through cannot be
   honestly passed; it depends on frontend units **F-01 → F-06** (BO §0 sequencing
   fact, verified by ITRGA against the code). Named here as the remaining step.
2. **Predictive-track deferral** — no promoted model exists (B-ML/B-ML2 honest
   negatives; Operator Decision Record DEFERRED); predictive signals remain gated.
3. **Residual deferrals** — per-process rate-limit store (multi-instance needs a
   shared store); multi-instance deployment unexercised; no load/soak measurements
   beyond the B-07 burst tests.
4. **Probe-execution defects (disclosed, corrected)** — the runner called
   `/api/v1/observability/metrics` (404; correct path is `/api/v1/metrics`), and its
   "unauthenticated" assistant call accidentally carried the auth header. Both were
   re-probed correctly in `x01_supplement.log`; the platform behaved correctly in
   both cases (metrics 200; unauthenticated 401). These are probe defects, not
   platform findings; disclosed because evidence must not paper over its own mistakes.

## 5. Defects found (as findings, not fixes)

**None.** No platform defect surfaced during the eight-hop execution. Per BO §6,
any defect would be reported here and a corrective Build Order issued separately —
nothing met that bar.

## 6. Test evidence (executed)

Full backend suite re-executed during this unit, in-memory DB, same command as the
B-series deliveries: **546 passed, 1 warning, exit 0, 172.55s**
(`docs/evidence/x01/x01_pytest_fullsuite.log`). The floor held unchanged.

## 7. Known limitations

- Evidence is dev-environment Level-I/II; no production-shaped deployment was
  exercised (multi-instance, shared rate-limit store — named in §4).
- Hop 4's raw response log is 6.6 MB (per-bar series payloads); the transmission
  set carries the disclosed mechanical digest; the raw log remains in the DA
  workspace.
- The corpus is crypto-only (carried observation OBS-BDATA-2).

---

**Posture unchanged:** Gate CLOSED · Production NOT CERTIFIED · research-only ·
non-actuating. **We don't guess. We prove.**
