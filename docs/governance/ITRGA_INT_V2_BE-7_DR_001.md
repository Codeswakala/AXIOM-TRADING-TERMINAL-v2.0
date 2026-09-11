# ITRGA INTAKE VERIFICATION RECORD — BE-7 DELIVERY PACKAGE
# ITRGA-INT-V2-BE-7-DR-001 · v1.0.0 · 2026-09-04 · AXIOM Trading Terminal v2.0
# Band: BE-7 (Backtesting, Simulation, Replay, and Governed Research Jobs)
# Reviewed package: AXIOM-V2-BE-7-DR-001 (+source/API/testrun transcripts)
# Chain: CN-V2-BE-7-001 → REQ-V2-BE-7-PLAN-001 → PRV (ACCEPTED) → BO-V2-BE-7-001 → DR → THIS RECORD
# Office: ITRGA (independent technical review & governance audit authority)
# Reading rule: this record verifies only *intake-stage evidence integrity*.
# It is NOT the FINAL determination; full-depth source review follows.

---

## §1 — Package identity (recomputed by ITRGA on receipt, 2026-09-04)

| Artifact | Bytes | Lines | MD5 (recomputed) | SHA-256 (recomputed) |
|---|---|---|---|---|
| DELIVERY_REPORT_V2_BE-7.md | 9,737 | 123 | `67e84a6e1915e2d374916d4a547d51da` | `d707697c15a9c2b30e762dbade87c0acddef79cfc94887b6d7825553577feb59` |
| V2_BE-7_SOURCE_TRANSCRIPT.md | 161,210 | 3,898 | `8156c081367c95925b53f82940ba46bf` | `2d496225…f5d` (full on record) |
| V2_BE-7_API_TRANSCRIPT.txt | 4,870 | 155 | `8c8e0084c8e1b33c88d9f7fe8a8c64a7` | `4f73511b…752` (full on record) |
| V2_BE-7_TESTRUN_TRANSCRIPT.txt | 96,636 | 1,007 | `69294b316fdcc625c9e97fb0d9daa2ca` | `1da03bce…177` (full on record) |

All four recomputations byte-match the DR §5 hash table. **Package collision/doctamper check: PASS.**

## §2 — Intake verification ledger (each check executed by ITRGA against the transcripts)

### INT-1 · Source-transcript self-consistency (17/17) — PASS
The transcript's §2 manifest declares 14 new + 3 modified files, each with a full 64-char SHA-256. ITRGA extracted all 17 literal bodies from §3 (fence-delimited, `## File:` sections) and re-hashed each with both trailing conventions: **17/17 literal bodies byte-match their declared SHA-256 (convention: body + trailing `\n`)**. The delivered code in the transcript is exactly what the manifest pledges.

### INT-2 · V1 preservation attestation vs repository floor (6/6) — PASS
The delivery pins six V1 lineage files by full SHA-256. Recomputed against HEAD `fd8d649`: **6/6 byte-exact** — `app/ml/dataset/{chronology_guard,split_engine,snapshot_builder,service}.py`, `app/execution_research/simulation.py`, `app/ml/economic/service.py`. The declared attestations are verbatim-full-length hashes (supersets of the plan's sha-16 pins). V1 floor untouched in substance, pinned in evidence.

### INT-3 · Testrun summary vs declared budgets — PASS
Transcript footer: **`test session: collected 971 items; 971 passed, 2 warnings in 499.11s`**, zero failures, zero errors, zero skips. BE-7 module totals inside the run: replay 17 + migration 11 + jobs 25 + boundaries 7 = **60 new tests**; 911 (BE-6 floor) + 60 = 971 ✓ matches BO T-1 floor `≥971` and DR §4's per-module map arithmetic exactly.

### INT-4 · API transcript evidence — PASS (9/9)
All nine Level-I ASSERTs evaluate True: input registered; re-registration reused + same id (write-once constitution, C1); job succeeded + computed; retry reused the SAME artifact with result count 1 (retry idempotency); `performance_disclaimer` present on every result surface; C4 manual-only refusal (scheduler-triggered submit refused, typed + audible); P-9 `live` construction-point refusal message *verbatim* (`result class 'live' is not constructible in band BE-7 — constructible set: ('backtest', 'simulation')`); terminal-cancel refused; 403 generic RBAC denial. Additional surface evidence: 401 unauthenticated; audit inventory of 13 event names incl. durable refusal events (`job.submit.refused`, `job.cancel.refused`, `input.reused`, `result.reused`); `alembic current → 20260903_0047 (head)`; drift direct runs on **both heads** (PGF-014 discipline): non-head run clean with no BE-7 tokens, head run **9 distinct inherited V1 tokens / zero BE-7 tokens — DRIFT GATE PASS** per BO T-6.

### INT-5 · ANNEX-R worked sample — independent recomputation (P-7) — PASS
ITRGA recomputed the worked sample **from the pins alone** (no execution of the delivered engine): closes {100,99,97,96,99,102,104,103,101,100}; threshold strategy buy<97.5 / sell>103.5 / qty 1 / cash 10,000; costs spread 0.10 + commission 0.05 + slippage 0 (price units). Buys at closes 97, 96 ⇒ effective 97.15, 96.15; sell at 104 ⇒ effective 103.85; fills = 3; final position 1; cash = 10,000 − 97.15 − 96.15 + 103.85 = **9,910.55**; equity = 9,910.55 + 1×mark(100) = **10,010.55**. Every value reproduces the pinned DR expectations **exactly**. The annex is arithmetically sound and its expected values are independently derivable — the fail-first property is genuine (any engine/cost error moves these numbers).

### INT-6 · Computation-version seed recipe — REPLICATED (P-6 support) — PASS
Migration 0047 declares `_RPE_FILES = {__init__.py, leakage.py, replay.py}` and `_RJE_FILES = {queue.py, runner.py}` with recipe `_rolling_hash` = SHA-256 over `ref‖0x00‖bytes‖0x00` per file in tuple order, seeded into `v2_computation_version` at migration time with `evidence_ref = BO-V2-BE-7-001`. ITRGA replicated the recipe against the transcript literals without divergence (RPE `1499343d…`, RJE `f01e3041…`). Migration tests assert presence of both rows with version `rpe-1.0.0`/`rje-1.0.0` and 64-char hashes (literal hash values are apply-time-computed — correct-by-construction; noted OBS-B). Guard discipline verified static-side: `_verify_triggers_present` fail-closed raise; compver delete-guard drop/recreate/verify with count-assertion on postgresql and sqlite; non-deleted-reinsertion via existing-set filter for permission seeds.

### INT-7 · Forbidden-surface scans over delivered modules — PASS
Across the 8 delivered package modules + `v2_research_jobs.py` model module: **zero** occurrences of broker/order/account/credential/network construction tokens; **zero** network libraries (`requests/httpx/urllib/socket/aiohttp/websocket`); the socket guard in tests pins deny-by-default. All `app.*` imports are authorized V2 contracts/repositories only (`v2.audit`, `v2.lineage`, `v2.marketdata.repositories` (allow-listed md-repo), `v2.rbac`, `v2.identifiers`, `v2.temporal.validation`, `research_governance.contracts`, `db.*`). The single `broker` token in `registry.py` is inside a **refusal predicate** (parameter keys containing credential/api_key/broker/account/adapter are rejected — "pure c rule functions only"). `permissions.py` `V2_FORBIDDEN_PERMISSION_MARKERS` guard present. The import-scan test (`test_import_scan_no_execution_adapter_reachable`) binds banned tokens `("execution","broker","order","adapter","trading_intelligence","market.live","app.market","paper","live_service")` with the single declared exception `("execution_research",)` scoped as *V1 read-only lineage **name*** — precisely matching the DR's §7 disclosed caveat.

### INT-8 · API surface census — PASS
`api.py` route enumeration: exactly **6 governed writers** (`POST /registry/inputs, /registry/cost-models, /registry/strategies, /jobs/submit, /jobs/run, /jobs/cancel`) + 3 reads (`GET /jobs, /jobs/{job_id}/attempts, /results`); **zero PUT/PATCH/DELETE** — C3 (no generic job-update endpoint) holds structurally at the router. Matches DR surface claim and BO T-8 exactly.

## §3 — Intake issue register

| ID | Class | Description | Disposition |
|---|---|---|---|
| OBS-A | Disclosure completeness (non-blocking) | Plan U-3 named modules `{registry, costs, strategy}.py`; the delivery merges all three scopes into a single `registry.py`. The divergence is not disclosed in DR §7. Compver engine file-sets unaffected (RPE/RJE scope intact); functionality claimed via tests (cost-model citation law, strategy lifecycle). | Registered. Full-depth review will verify cost-model + strategy semantics inside `registry.py`. DR-disclosure-completeness note to be carried into FINAL as a process observation, not a defect. |
| OBS-B | Informational (non-blocking) | `_RPE_FILES` includes `__init__.py` (plan pinned {leakage, replay} only) — broader, deterministic, harmless. Migration-test compver assertion checks component/version/hash-length rather than the literal hash (hash is apply-time-computed — deterministic by construction). | Registered; no action. |

**No blocking findings. No corrections issued at intake.**

## §4 — Intake verdict and next act

**INTAKE VERDICT: PASS — package admitted to full-depth source review.** All eight intake checks corroborated directly from the transcripts by independent ITRGA recomputation; nothing was taken on DR assertion alone where an independent check was possible.

Next act: **full-depth source review** — line-by-line read of all 17 delivered files against BO-V2-BE-7-001 terminal-state items T-1…T-14 (guard trigger messages verbatim vs SQLite/PostgreSQL forms; content-hash law; G-1…G-5 leakage refusal order; replay determinism ×3-byte-identical attestation path; C1–C4 write-law enforcement; audit/lineage wiring on every transition; boundary taxonomy tests), then the **FINAL determination** (accept / corrections). The `0047` working-DB application remains a separate sanctioned act at chain end and is **NOT authorized by this record**.

— ITRGA-INT-V2-BE-7-DR-001 · v1.0.0 · 2026-09-04 (Africa/Nairobi)
