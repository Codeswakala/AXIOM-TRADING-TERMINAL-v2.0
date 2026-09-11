# AXIOM V2 — Technical Debt Register

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-GOV-TD-001 |
| Status | Active |
| Date | 2026-08-24 (updated by replacement DA — BE-1 remediation, DR-004) |
| Author | Development Authority (DA) |
| Build Order | BO-V2-BE-0-001; updated under BO-V2-BE-1-001 correction cycle |

---

## Debt Classification

| Severity | Definition |
|----------|------------|
| Critical | Blocks production certification or security |
| High | Significant maintainability/quality impact |
| Medium | Moderate impact; should be addressed |
| Low | Minor; awareness sufficient |

---

## Inherited V1 Debt

| ID | Description | Severity | Source | Impact on V2 | Planned Resolution |
|----|-------------|----------|--------|--------------|-------------------|
| V2-TD-01 | Frontend legacy CSS in global.css (~2,388 lines of dead styles) | Medium | V1 | None for BE-0; frontend cleanup in FE bands | FE-1 |
| V2-TD-02 | TerminalChartStage god component (1,281 lines) | Medium | V1 | None for BE-0; decomposition in FE bands | FE-2/3 |
| V2-TD-03 | Monolithic API client (client.ts, 1,881 lines) | Medium | V1 | None for BE-0; split in FE bands | FE-1 |
| V2-TD-04 | V1 production not certified | High | V1 | V2 cannot claim production status | Separate certification |
| V2-TD-05 | V1 governance gate CLOSED | High | V1 | V2 must maintain gate closure | V2 certification process |

---

## V2 Debt

| ID | Description | Severity | Source | Planned Resolution |
|----|-------------|----------|--------|-------------------|
| V2-TD-06 | PostgreSQL residual runtime evidence (PG-002 §4): post-downgrade trigger/function absence query and PostgreSQL-native UPDATE/DELETE refusal output not yet captured; SQLite equivalents proven | Medium | BE-1 (Operator-environment dependency) | Operator runs existing PostgreSQL command pack; close on evidence supply |
| V2-TD-07 | V2 integration tests run app-level paths on SQLite only in DA workspace; PostgreSQL app-level test pass not executed (dialect parity assumed from migration/trigger evidence) | Low | BE-1 | Optional PostgreSQL-URL test run in Operator environment or CI PostgreSQL service in a future band |
| V2-TD-08 | Inherited `app/main.py` lint findings (I001 import sort at line 3, E501 at line ~250) predate BE-1 and were not remediated to avoid out-of-scope churn in a governed V1 file | Low | V1 (surfaced during BE-1 lint pass) | Fold into V1 Ruff baseline cleanup |
| V2-TD-09 | BE-2 PostgreSQL runtime evidence outstanding (Operator-run command pack; app-level API tests SQLite-only in DA workspace) | Medium | BE-2 (Operator-environment dependency) | Close on Operator PostgreSQL rerun evidence |
| V2-TD-10 | SQLite store-read datetime normalization helper (`_utc_from_store`) compensates for SQLite discarding tz on DateTime(timezone=True); PostgreSQL path returns aware values natively | Low | BE-2 | Revisit if/when PostgreSQL becomes the dev/test dialect |
| V2-TD-11 | Read-time gap disclosure capped at 50 periods per bars response; full gap inventory available via W-1 exception records | Low | BE-2 | Documented display bound; revisit with FE consumption band |
| V2-TD-12 | BE-3 P1 PostgreSQL runtime evidence | — (resolved) | BE-3 P1 | **Closed** — Operator evidence accepted in ITRGA-DET-V2-BE-3-P1-FINAL-001 |
| V2-TD-13 | Credential/vault service design deferred to P2 plan (mandatory revisit per ITRGA decision §3.3); P1 holds no credential | Low | BE-3 P1 | P2 design plan |
| V2-TD-14 | Provider WebSocket/streaming transport excluded from P1/P2 initial scope | Low | BE-3 plan | Future separately authorized order |
| V2-TD-15 | BE-4 `structure_nesting` relationship class pinned (rule + refusal boundary tested) but has no v1 emitter | Low | BE-4 DR §6.5 | Future MCE version bump (governed) |
| V2-TD-16 | BE-4 `stale` bound is a band-level declared constant (3 timeframe periods) | Low | BE-4 DR §6.3 | Future governed bound; disclosure carries the bound used |
| V2-TD-17 | BE-4 family statement vocabularies are v1-scope deterministic reductions | Low | BE-4 DR §6.4 | Richer vocabularies via versioned MCE evolution |
| V2-TD-18 | BE-5 historical_real/live data classes structurally present but writer-refused (corpus-gated by design) | Low | BE-5 DR §8.4 | Unlock via governed act after the corpus track |
| V2-TD-19 | BE-5 freshness bounds are band-declared constants (no V1 config exists); disclosed in every outcome | Low | BE-5 DR §5 | Future governed bound |
| V2-TD-20 | BE-5 `withheld` state structurally complete but no v1 emitter path | Low | BE-5 DR §8.3 | Future evaluator integration (naming item resolved by C-1) |
| V2-TD-21 | C-2: engine-file pinning at the application act | — | **CLOSED** (ITRGA-DET-V2-0045-APPLY-001 §1/§3: compver hashes == runtime recomputation == transcript literals — closed loop) | Done |

### Resolved this cycle (BE-1 remediation, DR-004)

| ID | Description | Resolution |
|----|-------------|-----------|
| — | Static checks mislabeled as integration tests (DEF-BE1-02) | Replaced with 18 genuine async DB/API/migration tests; accurate non-duplicated accounting (78 distinct V2 tests) |
| — | V2-scope lint debt (unused imports/import sort in `app/v2/**`, V2 tests) | `ruff --fix` mechanical cleanup; V2 scope lint-clean |

---

| V2-TD-22 | BE-6 long-only v1 allocations (weights sum to 1, each ≥ 0; short/leveraged out of scope) | Low | BE-6 DR §7.1 | Future governed extension band |
| V2-TD-23 | BE-6 factor decomposition is market-class grouping, not regression | Low | BE-6 DR §7.2 | Regression factors in a future band; declared in every output's limitations |
| V2-TD-24 | BE-7 scheduler tick source out of v1 scope (manual invocation only) | Low | BE-7 DR §7.1 | Future separately-authorized act |
| V2-TD-25 | BE-7 strategies are registered deterministic rule functions; arbitrary-code sandboxing out of scope | Low | BE-7 DR §7.2 | Future band |
| V2-TD-26 | BE-7 leakage law is open_time-based; ingest/publication lag controlled by G-5 content re-verification (refusal), revisited at the corpus track | Low | PRV §5.4 / DR §7.3 | Corpus track |
| V2-TD-27 | BE-8 realized P&L is average-cost; FIFO lot accounting + multi-currency deferred (A-3/A-4) | Low | BE-8 DR §6 | Future band/act |
| V2-TD-28 | BE-8 paper positions have no portfolio-research projection (Q8 parallel-domain law); read-only projection = future separately-authorized act | Low | Design S5/Q8 | Future act |
| V2-TD-29 | BE-8 confirmation actor-segregation (`confirmed_by != initiated_by`) documented but unenforceable in single-operator reality (A-2) | Low | Design S7.2 | Revisit at multi-operator |
| V2-TD-30 | BE-11 mode remains RESEARCH on the deployment — bridge writers 403 by D-B11-MODE; flip-to-PAPER is a separate operator register act, separately elected | Low | OV-002 §3 / closeout posture | **DISCHARGED 2026-09-07** — closeout ed-2 addendum: flip to PAPER executed + first armed intent sworn live (gateway `accept_with_notes`, exposure-deferred + stale-banner notes; `duplicate_refused` arm; ledger 1 row, operator citation EURUSD 1.16233 MT5 Exness panel; digest `0095a16d…a8bd`; drift ARMED). Flip is per-boot env, not mutation — fielded deploy reverts per operator election |
| V2-TD-31 | N-O18 credential hygiene: admin credential crossed the console transcript during BE-11 first-read; rotation ADVISED (band-neutral, operator-side, non-gating) | Medium | Closeout correction ledger | **CLOSED 2026-09-08** (closeout ed-3): rotation 1 + rotation 2 executed; THE CREDENTIAL LAW standing (keyboard→file; consoles read files, never Read-Host secrets; act cards assume file-fed env; file-fed login witnessed 200) |
| V2-TD-32 | Socket transport anomaly under uvicorn on the console box (sockets severed pre-ASGI, server log silent) — registered environmental; first-read witnessed via in-process ASGI door (fielded-file-direct) | Low | Closeout correction ledger | Environmental — revisit if it recurs on a gating path |

**End of Technical Debt Register**
