# ITRGA INDEPENDENT TECHNICAL REVIEW — W2-U02

## ML Research: Market-Agnostic Data Access + Multi-Market Metadata Layer

**Review ID:** ITRGA-REVIEW-W2-U02
**Unit:** W2-U02 · **Wave:** 2 — ML Research Framework · **Unit:** 02
**Reviewer:** ITRGA (Independent Technical Review & Governance Authority)
**Date:** 2026-07-13
**Inputs reviewed:** `DELIVERY_REPORT_W2-U02.md`; operator console transcript (`operator results.md`,
Windows/PowerShell + PostgreSQL 18, Python 3.14.6); cross-checked against `BUILD_ORDER_W2-U02.md`,
`ITRGA_REVIEW_W2-U01.md` (G-1/G-2/R-CI-01), `07_ML_SPEC`, D-W2-001.
**Motto:** *We don't guess. We prove.*

---

## 0. VERDICT

> ## ✅ **APPROVED WITH OBSERVATIONS** — Platform **v0.14.0**
>
> W2-U02 delivers the market-agnostic data-access seam and multi-market metadata layer on **operator-run,
> target-platform Level-I evidence**: clean PostgreSQL migrate to head `20260713_0006`, **pytest 105
> passed** (97→105, +8 new), ruff clean, frontend 16 + build, and a green parity smoke. The two highest-risk
> guarantees are **proven, not asserted** — the canonical market set is exactly the §5 eight classes with
> **no new "deriv" top-level market**, **Deriv is a provider under Synthetic**, and **all three isolation
> greps (provider terms / symbol identity / ML ORM reach-around) were shown with command + empty output**
> (R7 satisfied). **The W2-U01 residual G-2 is fully CLOSED** with the exact persisted-PostgreSQL
> quarantine-row proof I required. **No CRITICAL, no HIGH.**
>
> Two LOW residuals remain owed: **G-1** (the `-vv` per-test *names* were **again** not captured — second
> occurrence, see §4) and **R-CI-01** (no CI run in this transcript). Both are visibility/capture items, not
> behaviour gaps.

**Why not withheld:** the core function is Level-I proven, and the anti-corruption / no-new-market /
D-W2-001 guarantees — the whole point of this unit — are demonstrated by shown greps and passing structural
tests. **Why not clean APPROVED:** G-1 is now owed for the **second consecutive unit**, and R-CI-01 remains
outstanding since Wave 1; I do not waive evidence I asked to see (§5), so both are tracked as required
re-captures with a sharper note on the G-1 pattern.

---

## 1. Evidence Hierarchy Assessment (R2)

**Level-I (operator-run, Windows + PostgreSQL)** for every material claim, plus the DA's own structural
negative evidence. Fourth consecutive first-submission target-proven unit.

| Tier | Present? | Notes |
|------|----------|-------|
| Level-I — operator-run on Windows + PostgreSQL | ✅ | PG migrate to `0006`, pytest 105, greps, Deriv/market proof, persisted PG quarantine row, parity smoke |
| Level-II — DA sandbox (SQLite) | ✅ | 105/16 + SQLite migrate — corroborating |
| Level-III — source/ADR excerpts | ✅ | Files enumerated; ADR-022 added |
| Level-IV — report claims | ✅ | Present; not the basis for approval (R1) |

---

## 2. Mandatory §5 Evidence — Line-by-Line Verification

| # | Required (Build Order §5) | Verdict | Proof in operator console |
|---|---------------------------|---------|---------------------------|
| 1 | Operator test console: pytest ≥97+new, 0 failed; vitest 16; ruff; tsc/build | ✅ **PROVEN** | `105 passed, 191 warnings in 86.23s` (run under the PG env after migrate); `ruff … All checks passed!`; `Tests 16 passed (16)`; `vite build ✓ built`. Backend 97→105 (+8 = the 8 named tests). |
| 2 | Migration on PostgreSQL, new head shown | ✅ **PROVEN** | `Running upgrade 20260713_0005 -> 20260713_0006, W2-U02 market series metadata table`; `alembic current → 20260713_0006 (head)` on `PostgresqlImpl`; only one new revision. |
| 3 | Multi-market evidence; **no new top-level market** (structural + shown class listing) | ✅ **PROVEN** | `CANONICAL_MARKET_CLASSES: ['commodities','crypto','etfs','forex','futures','indices','stocks','synthetic']` — exactly the canonical §5 set, **no "deriv"**; `DERIV_PROVIDER: deriv / DERIV_MARKET_CLASS: synthetic / DERIV_SOURCE_AUTHORITY: synthetic`; `test_market_series_key_rejects_new_top_level_market` in the +8. |
| 4 | Provider-isolation grep (R7: cmd+output) + D-W2-001 no-symbol-identity | ✅ **PROVEN** | Three shown greps over `app\ml` — provider-native terms (`DERIV…PLACEHOLDER\|Deriv`), symbol identity (`symbol_id\|one_hot_symbol\|symbol_identity`), and ORM reach-around (`app.db.models.candle\|CandleRepository`) — **all returned empty** under their labelled headers (command + output shown ⇒ R7 satisfied). |
| 5 | **G-1 (owed): `-vv` named-test recapture** | ⚠️ **NOT SHOWN (again)** | No dedicated `-vv \| Tee-Object` run with per-test PASSED lines in the transcript; only the summary `105 passed`. The command pack documents it but its output was not captured. **Second occurrence** — see §4. |
| 6 | **G-2 (owed): persisted PostgreSQL quarantine row** | ✅ **CLOSED** | Committing script → `PERSISTED_QUARANTINE_ROWS_IN_SESSION: 1`, then raw `psql … SELECT … FROM dataset_quarantine_records` → **`FUTURE_OPEN_TIME \| dataset_construction \| sample:operator.csv \| EURUSD \| M1 (1 row)`**. Exactly the required proof. |
| 7 | **R-CI-01 (owed): CI run** | ⚠️ **NOT SHOWN** | No CI run (remote or local) in this transcript. Still carried since Wave 1 (local-orchestration was proven green in W1-U04). |
| 8 | Parity smoke (no regression) | ✅ **PROVEN** | `LOGIN OK … True`; `WS-TICKET status: 200 ticket_present: True`; seed 80/80; candles returned; `/market/live/status` `persist_errors: 0`, `last_error: null`. |
| 9 | Confidence HIGH/MODERATE/LIMITED, no fabricated % | ✅ **COMPLIANT** | Per-dimension with justification; "No percentage confidence is asserted." |

**Independently verified:** the +8 test delta matches the 8 named tests in Delivery Report §6 (incl.
`..._rejects_new_top_level_market`, `..._deriv_adapter_is_provider_under_synthetic_no_live_connection`,
`..._canonical_ohlcv_mapping_and_authority_across_markets`, `..._duplicate_and_ordering_validation_across_markets_and_providers`,
`..._provider_terms_do_not_leak…`, `..._use_query_port_not_scattered_candle_orm`,
`..._no_symbol_identity_learned_feature_pattern`). The 105-passed run is on the PG-configured environment
(env set + migrate immediately prior).

---

## 3. Governance Envelope — Compliance

| Constraint (Build-Order §2) | Verdict | Basis |
|-----------------------------|---------|-------|
| ❌ No model / features-for-training / execution | ✅ Upheld | §9 out-of-scope confirmed; no model/feature code; suite has none. |
| ❌ No broker/provider live connection or credentials; gate CLOSED | ✅ Upheld | `DerivSyntheticIndicesAdapter` is a **skeleton, no live connection / no network I/O / no credentials**; External Integration untouched; broker tests still green in the 105. |
| ❌ No new top-level market | ✅ Upheld | market-class listing = §5 set; `market_class='deriv'` rejected; structural test. |
| ❌ No symbol identity as learned field (D-W2-001) | ✅ Upheld | shown grep empty + structural test; metadata role `governance_evaluation_only`. |
| ❌ No DB reach-around | ✅ Upheld | ORM-reach-around grep empty; only `market_data_query.py` adapter touches candle ORM. |
| ❌ No provider vocabulary leaking inward (anti-corruption) | ✅ Upheld | provider-term grep empty; provider mapping isolated in `provider_adapters.py`. |
| ❌ No secrets in code/logs | ✅ Upheld | no token in transcript; redaction seam intact. |
| ❌ No regression (Wave-0/1 + W2-U01) | ✅ Upheld | 105 passed incl. prior suites + W2-U01 chronology guard; parity smoke green; frontend 16 + build. |
| ✅ Preserve advisory-first, tz-UTC, observability, dataset+guard | ✅ Upheld | confirmed by suite + smoke + persisted quarantine proof. |

---

## 4. Findings (classified — R8)

**No CRITICAL. No HIGH. No MEDIUM.**

- **G-1 (OBSERVATION, LOW — but now a RECURRING pattern, 2nd unit).** The `-vv` per-test *names* were again
  not captured; only the `105 passed` summary. The behaviour is proven (count + green, twice), so this stays
  LOW — **but this is the second consecutive unit** where the DA documents the `Tee-Object` command in the
  pack yet the operator's transcript doesn't show its output. **A documented command is not captured
  evidence.** Required: in W2-U03, actually **run and capture** `pytest <ml test files> -vv | Tee-Object -FilePath <evidence>` (or `-rA`) so each named test line is in the transcript. I will keep tracking this
  until it is shown once; if it recurs a third time it escalates to a MEDIUM process finding.
- **R-CI-01 (OBSERVATION, LOW, carried).** No CI run this unit. Local-orchestration was proven green in
  W1-U04; a run (remote preferred) is the standing preference. Capture opportunistically.
- **OBSERVATION (informational) — deferrals recorded correctly.** TD-042 (live Deriv/provider connection
  deferred) and TD-043 (metadata not yet consumed by features/evaluation) are legitimate, well-scoped
  deferrals to later Wave-2 units. No action.
- **RECOMMENDATION:** when W2-U03 introduces features, add a test that the `market_series_metadata`
  (session/tick/timezone/authority) is **readable by evaluation code but structurally excluded from the
  feature vector** — turning the "metadata not learned" promise into an enforced boundary at the moment it
  first becomes temptable.

No finding withholds approval: **G-2 (the substantive W2-U01 residual) is closed**, and the two remaining
items are visibility re-captures with unambiguous underlying behaviour.

---

## 5. Required Actions (tracked, non-blocking to THIS approval)

1. **G-1 (escalation watch):** in W2-U03 evidence, **run and capture** the ML dataset/market `-vv` output
   with per-test names visible (`| Tee-Object` / `-rA`). Third miss → MEDIUM process finding.
2. **R-CI-01:** capture one CI run (remote preferred; local-orchestration acceptable), fail-closed.
3. **(Recommendation)** W2-U03: enforce "metadata is evaluation-readable, feature-excluded" by test.

---

## 6. Evidence Confidence Statement (R6 — no fabricated percentages)

**Confidence in this APPROVAL: HIGH (with two LOW capture caveats).** Justification: the market-agnostic
access seam, multi-market metadata, provider-under-class model, and anti-corruption boundary are backed by
**operator-run Windows + PostgreSQL Level-I evidence** I verified directly — clean PG migrate to
`20260713_0006`, `pytest 105 passed` under PG, three shown-and-empty isolation greps (R7), the exact
canonical §5 market listing with no new "deriv" market, the Deriv-as-Synthetic-provider proof, and a
green parity smoke. **G-2 is closed with a persisted PostgreSQL quarantine row** — the strongest possible
proof of that behaviour. Confidence is **HIGH rather than absolute** only because the `-vv` per-test names
(G-1) and a CI run (R-CI-01) remain uncaptured — visibility items, not behaviour — with G-1 now on an
escalation watch.

---

## 7. Commendation (earned — does not soften the G-1 pattern note)

Fourth consecutive first-submission target-proven unit, and the strongest anti-corruption evidence yet: the
DA proved the two hardest guarantees (**no new market**, **provider dialect stays at the door**) with shown
greps + structural tests rather than assurances, modelled **Deriv exactly as directed** (provider under
Synthetic, skeleton-only, no connection/credentials), and **closed G-2 with a live-PostgreSQL quarantine
row** — precisely the persisted proof requested. Metadata was correctly fenced as governance/evaluation
only. This is disciplined, reviewer-aware work. The single soft spot is a repeated *capture* habit (G-1),
called out so it is fixed, not repeated.

---

## 8. Disposition

- **W2-U02: APPROVED WITH OBSERVATIONS.** Platform **v0.14.0**.
- **Residuals:** G-1 (`-vv` names — escalation watch), R-CI-01 (CI run) — both into W2-U03 evidence.
  **G-2 CLOSED.**
- **Hard gate reminder:** no model unit (W2-U06+) is reviewable until W2-U01–U05 are Level-I proven. U01 +
  U02 proven; **U03–U05 remain.**
- **Next:** ITRGA recommends authorizing **W2-U03 = Feature Definition Framework + Feature Store v1** (per
  the accepted plan §10) — normalized, causal, versioned, **no symbol identity**, with the "metadata is
  evaluation-readable/feature-excluded" boundary enforced by test, and carrying the G-1/R-CI-01 re-captures.
  The DA does not self-authorize the next unit and does not open the broker gate. Await operator direction +
  a new Build Order.

---

*ITRGA — One doorway, common tongue, and it holds: eight canonical markets and not a ninth, Deriv living
under Synthetic rather than beside it, the provider's dialect stopped at the door, and a quarantine row now
proven alive on PostgreSQL. Two things still to simply show us next time — each test line, and a pipeline
run. We don't guess. We prove.*
