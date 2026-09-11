# DELIVERY REPORT — AXIOM V2 BE-8: Paper Trading, Paper Account, and Risk Gateway

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-8-DR-001 |
| Version | 1.0.0 |
| Build Order | BO-V2-BE-8-001 |
| Governing design | AXIOM-V2-BE-8-DESIGN-001 v1.1.0 (ACCEPTED — ITRGA-ACC-V2-BE-8-DESIGN-001) incl. D-1/D-2 rulings + binding conditions |
| Date | 2026-09-04 |
| Author | Development Authority (DA) |
| Status | **SUBMITTED FOR ITRGA INT INTAKE + DEEP REVIEW** |
| Baseline in | head `20260903_0047` · 972 tests · triggers 42 · permissions 49 · compver 8 |
| Baseline out | migration `20260904_0048` (**DA test chains only** — working-DB application separate per §1 of the BO) · **1,026 tests** (972 + 54) · triggers **58** · permissions **57** · compver **10** — all T-13 pins hit exactly |

**Standing discipline: we don't guess. We prove.**

---

## 1. Executive summary

Band BE-8 implemented in full per the accepted design: eight `v2_paper_*`
tables under the **zero-UPDATE regime** (state = append-only event ledger;
current state derived from max event_index); the **S2.6/C-1 hold seam
exactly as accepted** (`may_execute` owned once; ledger-derived single-use
confirmation consumption; all four typed refusal classes; `risk_block`
structurally confirmation-proof); **N4 structural** (`fill_class` CHECK
single value `paper_simulated`); **N2 structural** (frozen single-entry
routing registry, no adapter interface/ABC anywhere, typed
`PaperOrderIntent`-only seam); **N1 structural** (zero credentials — scans
shipped); deterministic simulator over pinned content-hashed snapshots
with G-5-style re-verification. **1,026 / 1,026 passed** on the full
suite. ANNEX-P hand-computed values reproduced exactly through both the
engine and the API. Fail-first witness shipped (OBS-E statute honored —
implementation absent ⇒ ModuleNotFoundError, then restored and green).

Every fill, balance, and P&L surface carries the unconditional
disclaimer: paper-simulated on governed replayable snapshots, never
broker-confirmed, no live or future performance claim.

## 2. Terminal contracts T-1…T-18 (evidence map, §5-of-BO form)

| T | Evidence (executed) |
|---|---|
| T-1 | D-1 exemption = single literal prefix `v2.paper.` (permissions.py, contract comment carries the ruling citation); **both arms + boundary tested**: `test_d1_exemption_scoped_exactly_v2_paper_prefix`, `test_d1_markers_still_die_elsewhere` (`v2.research.order.*` dies), `test_d1_boundary_paperwork_dies` (`v2.paperwork.*` dies) |
| T-2 | `VALID_MODES == ("RESEARCH","SIMULATION","PAPER")`; `DEFERRED_MODES == ("LIVE",)`; paper writers demand `mode=="PAPER"` typed (`test_t2_paper_writers_refused_outside_paper_mode` — negative-mode arm on a RESEARCH app); `test_mode_law_t2` |
| T-3 | `test_import_scan_paper_domain_isolated` (banned tokens incl. credential/secret/vault/keyring + all network libs); `test_no_secret_or_credential_vocabulary` (code scan, docstrings stripped — the N1 declarations name the concept to forbid it) |
| T-4 | `test_sealed_registry_single_entry_frozen` (MappingProxyType, mutation raises); `test_no_adapter_abc_anywhere_in_domain` (no ABC/abstractmethod/adapter class); typed-seam refusal `test_untyped_seam_refused`; S6.4 attack-table rows executed across the isolation tests + schema refusals |
| T-5 | Intent DDL carries mode/actor_id/account_id/correlation_id/idempotency_key/snapshot_ref/time_basis (migration test asserts columns); risk decision by FK uq; event ledger + audit on every transition (E1 walk) |
| T-6 | `ck_v2_pfill_class IN ('paper_simulated')`; raw INSERT of `broker_confirmed`/`live`/`paper`/`confirmed` refused at DB (`test_0048_fill_class_schema_impossible`); disclaimer on every API response (envelope embeds it unconditionally; Level-I ASSERTs) |
| T-7 | 16 guard triggers; **all 16 messages byte-exact vs independent test-local literals** (`test_0048_guard_messages_verbatim`); zero UPDATE anywhere — state derived (`current_state` = max event_index) |
| T-8 | uq(intent_id) on decisions — second decision insert refused at schema; uq(account_id, idempotency_key); uq(intent_id, fill_index); uq(intent_id, event_index) — all probed behaviorally (`test_0048_behavioral_uniqueness_anchors`) |
| T-9 | Exhaustive `LEGAL_TRANSITIONS`; absence = typed refusal (`append_event`); hold seam: confirm/cancel row-exact (C-1c classes `hold.issued/confirmed/cancelled`, audits `paper.order.hold_confirmed/hold_cancelled/confirm_refused`); **four refusal classes each typed + durably audited** (`test_c1_four_refusal_classes`); **C-1d both arms** (`test_c1d_block_unreachable_by_confirmation`: not_confirmable + vocabulary content assertion + forged-append refusal) |
| T-10 | `test_deterministic_x3_byte_identical` (s1==s2==s3); ANNEX-P: engine tests + API walk both reproduce 2 fills @ 97.65, remainder 1 voided, cash 9,609.40 / equity 10,009.40 / unrealized 9.40 / margin 200/9,809.40; snapshot mismatch = typed refusal (`paper.snapshot.content_mismatch`) unit + API-quarantine arms |
| T-11 | Decimal end-to-end over TEXT-decimal columns; `presentation_round` half-even 2dp presentation-only; USD-only CHECK; average-cost realized P&L (`test_realized_pnl_average_cost`); no float anywhere in the money path |
| T-12 | `run_reconciliation`: genesis recompute over the full fill ledger, content comparison (PGF-012), immutable outcome row; discrepant = typed alarm never auto-corrected (`test_reconcile_content_based_and_alarm`); E1 walk ends `consistent` |
| T-13 | Censuses at 0048 head: **58 / 57 / 10** exact (`test_0048_seeds_and_totals` + live apply witnessed); compver components `paper_execution_simulator=pxs-1.0.0` over `{simulator,ledger}.py`, `paper_risk_gateway=prg-1.0.0` over `{risk,contracts}.py`, recipe identical to 0047; RPE/RJE rows byte-unchanged (append-only law asserted) |
| T-14 | `test_drift_gate_0048[both revs]` + direct runs in the API transcript §6: nonzero exit, **zero BE-8 tokens both heads**, inherited V1 baseline only |
| T-15 | `test_0048_no_touch_protected_state` (non-paper permission/compver rows byte-identical; trigger delta exactly the 16 names); `test_0048_downgrade_cycle_content_based` (symmetric teardown; compver delete-guard restored with count assertion) |
| T-16 | `test_api_surface_census_exact`: POST = exactly 6 governed writers, GET = 8 reads, **zero PUT/PATCH/DELETE** (C3); BE-1 envelope + disclaimer on every response; 403 generic `"Permission denied"`; 401 unauthenticated (`test_t16_rbac_denied_and_unauthenticated`) |
| T-17 | Full raw `-v`: **1,026 passed / 0 failed** = 972 + 54 (transcript shipped). Machine note §7.2 (dist-present law) |
| T-18 | `test_pgf021_no_filesystem_conditional_behavior`: no Path.exists/is_dir/is_file branching, no os.environ/os.getenv in any domain module (the mode gate reads `app.state.v2_mode`, set once at app startup — config-driven and explicit) |

## 3. Test accounting (fail-first; 972 + 54 = 1,026)

| Module | Count | Content |
|---|---|---|
| `test_v2_be8_simulator.py` | 15 | ANNEX-P Cases A+B exact; ledger derivation exact; determinism ×3; N4 fill-class; tamper refusal; typed seam; cost purity + unknown-unit; realized P&L; reconcile; money law — **authored first (fail-first witness shipped)** |
| `test_v2_be8_migration.py` | 10 | DDL/columns; totals 58/57/10; fill-class schema-impossible ×4 banned values; 16 guard messages verbatim; uniqueness anchors ×4 incl. the C-1b iff-CHECK both directions; no-touch; downgrade; drift ×2; state CHECKs |
| `test_v2_be8_orders.py` | 16 | E1 full lifecycle + partial-fill voided remainder; E2 idempotency (one decision row ever) + rerun convergence; E3 block/rejected/expired/quarantine; C-1 confirm/cancel + four refusal classes + C-1d both arms; cancel semantics; T-2 mode gate; T-16 RBAC/401 |
| `test_v2_be8_boundaries.py` | 13 | D-1 three arms; sealed registry; no-ABC scan; import scan; PGF-021 scan; credential-vocabulary scan; API census; vocabulary integrity; mode law; V1 pins re-hash; prior-band contract regression (incl. BE-7 result-class taxonomy + COST_UNITS_V1) |
| **Total** | **54** | Full suite **1,026 passed, 0 failed** (V1 552 intact) |

## 4. D-8 statements

- **ruff:** clean over the band + amended files.
- **Credential scan:** CLEAN — the only hits are the boundary test's own
  banned-token literals and the household synthetic test-auth constants
  (`admin/admin123`, `operator-pass-123` — BE-5 intake-law classification).
- **compver recipe restated:** SHA-256 over `ref‖0x00‖bytes‖0x00` per file
  in tuple order, hashed from disk at apply time (OBS-B lineage:
  correct-by-construction). Current DA-disk values, pre-declared for the
  future 0048 application act:
  PXS `c58a06a5402f30a3828012f91b4aeb564008a9bfa34685cc57558e1003d106c0` ·
  PRG `ed6434fa5ff00b937b71e1d76a8fef32bc019f134e56831ac9f74af525376b1b` ·
  RPE `1499343d…b178` unchanged · RJE `8f107d17…0598` unchanged.
- **OBS-E transcript:** `V2_BE-8_FAILFIRST_WITNESS.txt` — collection with
  implementation stashed: `ModuleNotFoundError: No module named
  'app.v2.paper_trading.orders'`; restored; suite green.
- **D-1/D-2 arm locations:** `test_v2_be8_boundaries.py` lines
  (`test_d1_*` ×3, `test_mode_law_t2`) + `test_v2_be8_orders.py`
  (`test_t2_paper_writers_refused_outside_paper_mode`).

## 5. Evidence package (full hashes; intake law)

| Artifact | Bytes | MD5 | SHA-256 |
|---|---|---|---|
| `docs/evidence/V2_BE-8_SOURCE_TRANSCRIPT.md` (REM-001; 15 new + 5 modified, literal bodies) | 202,230 | `593faf7798130cccd8474513845ac2ab` | `63815f8077642bc0a9a40b1e97f7287a14bc7ed561c34e9fa51d00bb872c098f` |
| `docs/evidence/V2_BE-8_API_TRANSCRIPT.txt` (Level I; **20/20 ASSERTs**; audit inventory; drift both heads) | 16,827 | `e046f4eabe33e3252eb9d19883f7aa71` | `8007ec34ade7258acd3dbb32121ce8adbf1fbafd2607b928a0106dfde08c0ea0` |
| `docs/evidence/V2_BE-8_TESTRUN_TRANSCRIPT.txt` (raw `-v`; **1,026/0**) | 100,616 | `5161ff2287cd1746a520ff85e27ffc74` | `5b6817821425316f9295f4c079c199cbdd4207b48b66d94c9929f97e646182e1` |
| `docs/evidence/V2_BE-8_FAILFIRST_WITNESS.txt` (OBS-E; implementation-absent collection failure) | 810 | `1b2586e834b74d0234d1f2cef5c88842` | `b2f7099c6f22e05adcdbef18fba6bc3cc728b0d43160df2a20c9837a136d49b5` |
| `docs/evidence/V2_BE-8_ANNEX_P_WORKED_SAMPLE.md` (D-5; hand-computed pins) | 2,448 | `505c8f20fc84caafc4faee911ced943c` | `78adfa81082661888a238570b5dea074d01e164c0455954ebb0f3d9a12c88fc3` |

Per-file SHA-256 of all 20 delivered files: SOURCE_TRANSCRIPT §1 manifest.

## 6. Register impacts (staged; applied at acceptance per household law)

Capability rows `Paper Trading Engine`, `Paper Account Model`, `Pre-Trade
Risk Gateway` → **IMPLEMENTED** (COMPLETE is the acceptance act's). Risk
+2: paper-fills-mistaken-for-real (mitigated: N4 schema wall + mandatory
disclaimer + zero broker vocabulary); risk-gateway bypass (mitigated:
default-deny derived rule + uq decision anchor + append-only ledger).
Debt +3: FIFO/multi-currency deferred (A-3/A-4); paper→portfolio
projection deferred (Q8); confirmation actor-segregation unenforceable in
single-operator reality (A-2, documented).

## 7. Known limitations & disclosures (honest)

1. **Naming churn inside the band (disclosed):** the domain constants
   `ORDER_SIDES`/`ORDER_TYPES` were renamed `INTENT_SIDES`/`INTENT_TYPES`
   during integration — the V1 broker-token guardrails
   (`test_broker_integration`, wave-6/7 closeouts) scan all non-V1 code
   for `ORDER_TYPE` as a broker-specific symbol. The rename preserves the
   V1 guards **unmodified at full force** rather than adding exemptions
   to three V1 test files. No semantic change; the API request fields are
   unaffected.
2. **BE-1-era mode-test churn (D-2-sanctioned, disclosed):**
   `tests/test_v2_mode.py` pinned PAPER-rejection; three pins superseded
   to the D-2 vocabulary (docstrings cite the ruling). Net module count
   unchanged.
3. **Operator paper grants deferred (disclosed):** design S7.1 lists
   operator-role reads; the BO T-13 census pin (57 = 49 + exactly 8 rows)
   binds. v1 ships the 8 admin rows only; operator paper reads are an
   acceptance-phase decision (one-line seed delta if granted).
4. `time_in_force = 'replay_window'` only; scheduler/tick source remains
   registered debt (V2-TD-24 family). Manual `/run` invocation only.
5. Fill liquidity is a snapshot-carried declared parameter (citation
   law); no liquidity model is invented. Bars without `liquidity` default
   to full-fill (declared).
6. Single account per operator operationally; schema supports more (Q2).
7. Working-DB application of 0048: **not performed** — separate
   sanctioned act (E-0046-DUP startup law; PGF-020…024 statute screening;
   compver expectations pre-declared in §4).
8. All evidence pipeline-validation tier on synthetic/simulated inputs;
   no market or performance conclusion claimed or claimable.

**We don't guess. We prove.**

**End of Delivery Report AXIOM-V2-BE-8-DR-001**
