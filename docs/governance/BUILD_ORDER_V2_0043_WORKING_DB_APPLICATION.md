# BUILD ORDER — AXIOM V2: 0043 WORKING-DATABASE APPLICATION ACT

| Field | Value |
|---|---|
| Build Order ID | `BO-V2-0043-APPLY-001` |
| Date | 2026-09-02 |
| Authority | `AXIOM-V2-OD-BE-4-009` (Operator authorization, 2026-09-02); `ITRGA-PLAN-V2-0043-APPLY-001`; `ITRGA-ASS-V2-0043-APPLY-001` (scope; re-pins resolved); `ITRGA-DET-V2-BE-4-FINAL-001` §7 (residual B-1); `ITRGA-PTN-V2-PACK-001` (instrument discipline) |
| Executing authority | Operator console, under sanctioned ITRGA instruments (apply pack + verify pack) |
| Review authority | ITRGA (no self-approval; closure by determination) |
| Baseline | working DB head `20260829_0042`, byte-identical in force (sha256 `0483f9fe…`), 12 v2 triggers, 789-test baseline, drift = 9 inherited V1 tokens + expected BE-4 set |
| Status | **ISSUED — sanctioned apply + verify instruments to follow (full battery); no execution before issuance** |

## 1. Scope

Apply migration `20260831_0043_v2_be4_research_read_models` to the application's working SQLite database (`backend\axiom_dev.db`) as a **single sanctioned mutation**, with file-level backup anchor, guarded by pre/post checks, and close the act with a read-only verify run.

## 2. Terminal state (the verify act's contract — every item pinned)

| # | Item | Pinned value |
|---|---|---|
| T-1 | Current revision | `20260831_0043` |
| T-2 | v2 trigger count | **18** (12 inherited + 6 new) |
| T-3 | New guard triggers (exact names / exact messages, R-2 pins from `BO-V2-BE-4-001` §4) | `v2_computation_version_immutable_update/_delete` → `V2 computation version registry is immutable; UPDATE/DELETE prohibited` · `v2_market_context_report_immutable_update/_delete` → `V2 market context reports are immutable; UPDATE/DELETE prohibited` · `v2_chart_intelligence_report_immutable_update/_delete` → `V2 chart intelligence reports are immutable; UPDATE/DELETE prohibited` |
| T-4 | Tables | `v2_computation_version` (id/component/version/source_hash/evidence_ref/registered_at; `uq_v2_compver_component_version`) · `v2_market_context_report` (id/instrument_id/timeframe_set/as_of/mode/status/validation_tier/input_snapshot_id/input_content_hash/observations/engine_versions/engine_versions_hash/operator_id/created_at; `uq_v2_mcr_determinism_anchor`; `ix_v2_mcr_instrument`, `ix_v2_mcr_mode`) · `v2_chart_intelligence_report` (id/market_context_report_id/as_of/mode/status/annotations/interpretations/engine_versions/operator_id/created_at; `ix_v2_cir_mcr`) |
| T-5 | Permission seeds | exactly 5 additive rows (admin ×3, operator ×2; SAL-aligned per plan §7) |
| T-6 | Computation-version seeds | exactly 3 rows: `indicator_engine`, `market_context_engine`, `chart_intelligence_engine` |
| T-7 | Report-table content | empty (no rows; the governed writer is used in later acts) |
| T-8 | Integrity / journal / sidecars | `integrity_check` ok · journal delete · no `-wal`/`-shm` |
| T-9 | Drift (re-baselined) | exactly the 9 inherited V1 tokens: `audit_write_failure_records`, `ix_audit_write_failures_category_action`, `ix_audit_write_failures_created` (added) + `ix_advisory_signals_expires_at`, `ix_advisory_signals_freshness_status`, `ix_ingestion_runs_symbol_started`, `ix_model_artifacts_advisory_status`, `ix_model_artifacts_artifact_hash`, `ix_model_artifacts_experiment_id` (removed) — **no `v2_*`/`ix_v2_*` token** |
| T-10 | Authority variables | none exist for this act; the six TD/authority environment variables absent (as in all prior acts) |
| T-11 | Pre-image anchor | `operator-evidence\BE-4\axiom_dev.db.pre-0043-<ts>.bak` present, integrity ok, sha256 recorded (the byte-identical 0042-state file, sha256 `0483f9fe…` expected) |

## 3. Pre-conditions (all proven 2026-09-02; re-verified at runtime)

Baseline byte-identity (`0483f9fe…`, last write 2026-08-31 14:09:55 +03:00) · current revision exactly `20260829_0042` · on-disk hashes: 0043 = `ab905762…`, 0038 = `6e071157…`, 0039 = `bc11cae2…`, 0041 = `d775c34a…` (re-pins of `ITRGA-ASS-V2-0043-APPLY-001` §3) · application stopped.

## 4. Constraints

- Exactly one `alembic upgrade` invocation, targeting revision `20260831_0043` (not "head").
- Environment block as the verify packs (testing environment; pack-managed values; TD variables removed); **no credential of any kind; no network; no provider call**.
- The packs write only: the anchor, the transcript(s), and the throwaway helper (removed on exit).

## 5. Prohibitions (throughout the act)

No Git operation (custody deferred). No repository change beyond the sanctioned mutation. No modification of V1 objects, BE-1…BE-3 objects, the provider registry, or the status history. No other migration applied or downgraded. No actuation of any mode (RESEARCH/SIMULATION only context; this act introduces no runtime endpoint use). No credential in any artifact.

## 6. Rollback / containment

The pre-image anchor is a complete, integrity-checked copy of the 0042-state file. Containment options if the post-apply state is found wrong: restore the anchor (Operator action, ITRGA-instructed) or execute the symmetric `alembic downgrade` to `20260829_0042` (0043's downgrade drops only its three tables, six triggers, and seed rows). On SQLite the DDL is transactional — a failed upgrade rolls back fully. The band introduces no external effects.

## 7. Closure

Both transcripts (apply + verify) PASS, archived byte-identical, credential-scanned CLEAN → ITRGA act-closure determination `ITRGA-DET-V2-0043-APPLY-001`: residual B-1 of `ITRGA-DET-V2-BE-4-FINAL-001` §7 **closed**; drift re-baselined per T-9; 18 v2 triggers in force; the working database at head `20260831_0043`.

## 8. Issuance note

No pack is issued by this Build Order. The sanctioned apply pack and verify pack follow only after the `ITRGA-PLAN-V2-0043-APPLY-001` §4 battery (including the dry-run matrix W1/W2/N1–N4) is archived. Superseded instruments are not to be executed for this act (verify pack V3 remains the instrument of record for the *pre-apply* 0042-state verification only).

— ITRGA, 2026-09-02
