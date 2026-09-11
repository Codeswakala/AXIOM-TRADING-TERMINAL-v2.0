# BUILD ORDER BO-V2-BE-7-001 — Band BE-7: Backtesting, Simulation, Replay, and Governed Research Jobs

| Field | Value |
|---|---|
| Document ID | **BO-V2-BE-7-001** |
| Issued by | ITRGA |
| Date | 2026-09-03 |
| Authority | Operator BE-7 authorization of 2026-09-03 (`ITRGA-CN-V2-BE-7-001`); plan fully verified: `ITRGA-PRV-V2-BE-7-PLAN-001`, verdict **ACCEPTED, zero corrections**; Operator confirmation to issue this Build Order received 2026-09-03 |
| Governing plan | `AXIOM-V2-BE-7-DA-PLAN-001` v1.0.0 (2026-09-03) — the authoritative content reference for all DDL, file sets, contracts, and budgets cited below |
| Review contract | `ITRGA-REQ-V2-BE-7-PLAN-001` REQ §1.1–§1.13; Pins **P-1…P-10**; PRV conditions **C1–C4** and the scan-token condition (§3 below) are bindings of this order |
| Roadmap basis | `AXIOM-V2-BE-ROADMAP-001`, Band BE-7 (contract verbatim in REQ §0) |
| Executed by | Development Authority (DA), via Operator custody; **all commits belong strictly to the Operator** |

## 1. Scope authorized

**Single package, six units** (per-operator choice preserved to split per unit before work begins if desired):

- **U-1** — Migration `2026MMDD_0047_v2_be7_research_jobs` (date prefix at issuance; `down_revision = "20260903_0046"`) + models — **six physical tables** (normative clarification: plan §1.1's "5 tables" counts the five *guarded* tables; §1.2 enumerates six CREATE TABLEs — this order pins the enumeration): `v2_backtest_input` (versioned-immutable; `UNIQUE(input_id, record_seq)` = `uq_v2_btin_id_seq`; `UNIQUE(content_hash)` = `uq_v2_btin_content`) · `v2_cost_model` (`uq_v2_cost_id_seq`) · `v2_strategy_version` (`uq_v2_strat_id_seq`) · `v2_research_job` (the band's sole mutable row set — FP-1 conditions §3) · `v2_research_job_attempt` (append-only ledger; `UNIQUE(job_id, attempt_index)` = `uq_v2_jobatt_idx`) · `v2_research_result` (`UNIQUE(strategy_version_id, inputs_hash, engine_versions_hash)` = `uq_v2_result_determinism_anchor`) — all columns/types/CHECKs/BE-1 columns/6-class `data_class` exactly per plan §1.2, incl. the closed CHECK sets (`registration_outcome`, `lifecycle_state`, `job_state`, attempt `outcome`, and `result_class ∈ ('backtest','simulation')` **only**) — plus **10 guard triggers** (five pairs on the five guarded tables; exact messages quoted in §2 T-3) + **8 permission grants** (per plan §1.2, SAL-aligned) + **2 compver seeds** (`replay_engine = rpe-1.0.0` over the U-2 files; `research_job_engine = rje-1.0.0` over the U-4 files; hashed from disk at migration time; C-2 disclosure: the 0047 application-act instrument re-pins both file sets) — all exactly per plan §1.2. Models: `app/db/models/v2_research_jobs.py` + one additive registration in `app/db/models/__init__.py` (PG-002 law).
- **U-2** — `app/v2/research_jobs/{__init__,leakage,replay}.py`: structural leakage guards G-1…G-5 at the plan-named code paths (P-8) + deterministic replay engine (pure function of registered inputs × strategy parameters × cost model × engine versions; pinned-seed rule for stochastic parameters).
- **U-3** — `app/v2/research_jobs/{registry,costs,strategy}.py`: versioned-immutable input registration with content-addressed dedupe and durable C-1-law refusals; cost-model configuration with per-parameter `{value, unit, citation}`; strategy lifecycle (`draft → registered → retired` generations; only registered-current jobable).
- **U-4** — `app/v2/research_jobs/{queue,runner}.py`: database-backed governed queue (architecture row 89 decision) with attempt-idempotent runner (`UNIQUE(job_id, attempt_index)` + result determinism anchor ⇒ provably no double-apply; P-10); manual invocation only (`schedule.kind = "manual"`; C4); typed cancel with terminal-refusal.
- **U-5** — `app/v2/research_jobs/api.py` + one additive mount in `app/v2/api/router.py` + additive additions to `app/v2/rbac/permissions.py`: read surface (GET-only save the enumerated governed writers) + governed submit/cancel/registry writers under the v2 API prefix; RESEARCH-mode writers; six BE-1 states incl. `denied`; **no generic job-update endpoint** (C3); submit refuses `schedule.kind != "manual"` typed+audited (C4).
- **U-6** — Evidence: Delivery Report with the requirement map (REQ §1.1–§1.13 item-for-item + roadmap §0 + Pins P-1…P-10 + C1–C4), REM-001-class source transcript with full MD5+SHA-256 per file, raw `pytest -v` transcript, Level I API transcript, **worked-sample replay annex** (P-7), credential scans, register-sync entries.

**Explicitly NOT authorized:** any working-DB application of 0047 (separate sanctioned act with its own instrument, inheriting the E-0046-DUP startup rule); any scheduler/tick-source implementation (manual invocation only; scheduler is registered debt); any `paper`/`live` construction; any BE-8…BE-11 surface; arbitrary user-code strategies (registered deterministic rule functions only, per plan Part 15); FE surfaces; report preview/export; any use of real/historical data classes; any modification of V1 files (the six §1.0-pinned files are read-only lineage); any commit/push.

## 2. Terminal state (T-1…T-14) — required, evidence-backed

1. **T-1** — Chain at `…_0047 (head)`, single head, exactly one new revision; upgrade reproducible from `20260903_0046`; symmetric downgrade proven.
2. **T-2** — All six tables exist with exact DDL per plan §1.2: column sets, types, CHECKs (incl. `result_class` closed set and the 6-class `data_class` literal identical to 0044–0046), UNIQUE/index names per §1 above; nothing beyond the enumerated columns.
3. **T-3** — The 10 guard triggers exist and **refuse live** with the exact messages: `V2 backtest inputs are immutable; UPDATE prohibited` / `…DELETE prohibited`; `V2 cost models are immutable; …`; `V2 strategy versions are immutable; …`; `V2 research job attempts are immutable; …`; `V2 research results are immutable; …` (each pair); v2 trigger census = **42** (32 + 10), enumerated by name; `v2_research_job` **unguarded by design** (FP-1, §3).
4. **T-4** — 8 new permission rows with the exact tokens and SAL/role alignment per plan §1.2 (`v2.research.jobs.read/submit/cancel`, `v2.research.registry.read/write`, `v2.research.results.read`; operator: jobs.read + results.read); global total **49**; forbidden-permission-marker guard green.
5. **T-5** — compver total **8**; `replay_engine = rpe-1.0.0` and `research_job_engine = rje-1.0.0` with source hashes over the declared file sets, recomputed equal to the stored rows.
6. **T-6** — Post-migration `alembic check` drift at the new head = **exactly the 9 inherited V1 tokens, zero BE-7 tokens**, itemized, format-independent census (PGF-014 law), direct runs at both heads.
7. **T-7** — No-touch across 0047: BE-2…BE-6 protected state content-identical (tables/rows/pins enumerated); the six V1 files of plan §1.0 re-hashed unchanged at delivery.
8. **T-8** — Typed-outcome law executed: six states demonstrable incl. `denied`-by-RBAC; typed refusals live-proven — `paper`/`live` construction (schema-impossible + writer-typed), `schedule.kind ≠ "manual"` (C4), horizon-past-embargo (G-3), non-registered-current strategy in a job, missing `authorization_ref`, content-hash mismatch at replay (G-5); `performance_disclaimer` present on every result response.
9. **T-9** — Determinism + leakage evidence: the five future-leakage tests G-1…G-5 PASS (exit-evidence item i, transcript-visible); deterministic replay ×3 (byte-identical summaries; anchor idempotency — re-run returns the existing artifact; seed-pinned stochastic parameter) — exit item ii; cost-application purity; **worked-sample annex recomputed by the ITRGA and equal to engine output** (P-7 execution; 10-bar pinned series, pinned strategy/parameters, pinned cost model with citations, hand-computed outputs to stated precision).
10. **T-10** — Queue evidence (exit item iii): retry idempotency (double-apply collision → existing artifact returned; ledger row recorded); duplicate-submit race; typed cancel incl. terminal-refusal; failure typed; attempt ledger append-only; every transition mirrored by ledger + audit.
11. **T-11** — Job-silence + no-live-effect (exit items iv–v): writable-table allow-list asserted by test; import/dependency scan clean **with the token predicate including `trading_intelligence` and any `*adapter*` module** alongside execution/broker/order (Part 10.2 extended per PRV §5.4); API surface enumeration (every route GET except the enumerated governed writers; no execution vocabulary in paths/fields); construction-token scan clean; result classification + lineage walk tests PASS.
12. **T-12** — Evidence package: Level I API transcript with endpoint path pinned and inline ASSERTs true; raw `pytest -v`: floor **≥ 971, 0 failed** (911 + 60 declared budget: U-1 12 / U-2 15 / U-3 10 / U-4 15 / U-5 6 / regression 2; sum proven) with V1 552 intact; fail-first evidence per unit; no network in tests (socket guard); REM-001 transcripts with full hashes; credential scans CLEAN.
13. **T-13** — Register impacts staged honestly: capability rows `Backtesting Engine`, `Historical Replay`, `Research Job Queue` → IMPLEMENTED at delivery (COMPLETE only via acceptance); debt rows (scheduler tick source v2 scope; arbitrary-strategy sandboxing; open_time-as-of / ingest-lag disclosure per PRV §5.4); risk rows as declared; serialization per the register conventions.
14. **T-14** — Custody/oversight: no credentials anywhere (the band prompts for none — stated); no Git operations by DA or ITRGA; review authority is **full-depth**: errors are issued as corrections and the DA answers by corrected plan/report; **anything contrary to the roadmap or overall design is ruled out** until a sufficient corrected plan/report is presented.

## 3. Pins in force

**P-1…P-10** as carried and declared in the REQ (versioned-immutable lineage; determinism anchors on immutable artifacts; typed permanent outcomes + six-class honesty; computation provenance via compver; structural proof over vocabulary; hypothetical-only guarantee; independent recomputation; plus BE-7's **P-8** temporal-leakage structural guarantee, **P-9** result-class separation, **P-10** job idempotency/auditability), with the PRV conditions encoded as bindings:

- **C1** submission-time job fields (`owner`, `authorization_ref`, `inputs`, `schedule`) write-once; test-asserted.
- **C2** mutable column set on `v2_research_job` exactly `{job_state, attempt_count, output_ref, failure}`; the Part 10.1 allow-list constant names exactly this set; test-asserted.
- **C3** no generic job-update endpoint; transitions only via governed submit/cancel/runner surfaces; every transition mints ledger row + audit event.
- **C4** submit writer refuses `schedule.kind != "manual"`, typed + durably audited.
- **Scan-token condition** (`trading_intelligence`, `*adapter*` in the import-scan predicate) per PRV §5.4.

## 4. Delivery-report obligations (map)

Every REQ §1.1–§1.13 item, every roadmap §0 contract element, every Pin P-1…P-10, and every condition C1–C4/scan-token → evidence citation; the normative clarifications of this order (six physical tables; unguarded job table by design) answered explicitly; honest disclosures preserved (pipeline-validation tier; open_time-as-of model; rule-function-only strategies; manual scheduling); known-limitations and debt rows registered.

**INSCRIBED as BUILD ORDER BO-V2-BE-7-001, Band BE-7 — Backtesting, Simulation, Replay, and Governed Research Jobs. We don't guess. We prove.**
