# DELIVERY REPORT — BO-B-04
## Institutional Intelligence Generation

| Item | Value |
|---|---|
| Build Order | `BO-B-04` (Operator directive of 2026-08-20: "authorized"; predictive track deferred per Operator Decision Record) |
| Predecessors | B-00 → B-ML2 (all APPROVED WITH OBSERVATIONS) · Reconciliation Determination · Operator predictive-deferral decision |
| Implementer | AXIOM Development Authority (DA) |
| Reviewer | ITRGA — determination pending |
| Date | 2026-08-20 |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

**Standing discipline applied:** CA-TRANSMIT-1 (relay-accurate manifest, every declared hash verified against the transmitted set) · OBS-BML-1 (figures transcribed mechanically from the executed logs) · OBS-BML2-1 (the fail-first probe log IS in this transmission set, hash-verified).

---

## 1. Claimed scope vs. this Build Order

| BO requirement | Delivered | Where |
|---|---|---|
| B-04.1–B-04.5 five generation endpoints | ✓ 5 × POST, operator-authenticated, as-of-bounded | §3 |
| B-04.6 shared contract: auth + RBAC | ✓ `CurrentOperatorDep` on every generation endpoint (the intelligence-family RBAC pattern); no unauth generation | §3, §6 |
| persist with as-of bounds, source/data-class label, uncertainty, sample counts, audit lineage | ✓ services persist their own reports (uncertainty/sample/lineage/audit); endpoints persist the **data-class label** into `notes` (distinct candle `source` values in the window) | §4 |
| fail honestly on insufficient data | ✓ structured 422 `{error_code, detail, insufficient_data: true}` — no fabricated report | §5 |
| never mutate broker/account/trading/execution/gate state; never emit a signal | ✓ pinned by tests + the API probe's audit-row breakdown (only report rows + ingestion/operator events) | §6 |
| read surfaces unchanged | ✓ list/get contracts untouched; generated rows read back through them | §4 |
| §3 exclusions | No ML model/prediction/promotion; no signal/alert emission; no broker/account/position linkage; no scheduled generation; **no changes to the five services' math**; no guard/tier/gate weakening; no frontend; no governance-document changes; no repo publication | — |
| §9 CA-TRANSMIT-1 | ✓ relay-accurate manifest §9 | §9 |

## 2. What changed (files + SHAs + chain position)

Patch artifact: **`b04.patch.txt`** — sha256 `2704a8a2f264747f4f3ad539ce469f1404dc0f6362d5f7a854f2481ba98cbdc3`
- Applies clean (`git apply --check` exit 0) onto the verified 24-element chain over baseline `34f4c62`, in a pristine clone, as the **25th chain element**; post-apply, all 9 files byte-identical to the DA workspace (cmp-verified); clone-side B-04 + family sets 48/48, ruff clean.

| File | Content SHA-256 |
|---|---|
| `backend/app/api/routes/intelligence.py` | `3192f7bb775ae03b5db2e8c04b4f5eb43d44788587e845eb6059fb5c78366d00` |
| `backend/app/models/intelligence_generation.py` (new) | `90f94a1bfd7f47f6b024495e663636884cb64de15cd373aa54ba29e6c866bc0e` |
| `backend/tests/test_b04_intelligence_generation.py` (new) | `107ae10010ecd72bc0f6a3769ee68038610fdf8c231a43bb544ccb61e3a9539e` |
| `backend/tests/test_correlation_reports.py` (churn) | `b2669d14d860e287d2009abc8634110e0b74d299242c49a1257d5e80058f6c26` |
| `backend/tests/test_regime_reports.py` (churn) | `f9980bea5f98bbc79c6810cb972978ccbc682ade076d2ad67a94312ca9793e80` |
| `backend/tests/test_scenario_reports.py` (churn) | `8ab797870eacc0af68a253c1a405311b52d6a1736b374d875d61be3fa8902681` |
| `backend/tests/test_portfolio_risk_reports.py` (churn) | `7d34a1b8abb8d83409d68b396966833f5fbb541901c016fe0abb402d7293aaf8` |
| `backend/tests/test_signal_validation_reports.py` (churn) | `2a110795ba9c3c73221da9a9aa7d91fb22e846d332f81a17c1e0ba8880e1e461` |
| `backend/tests/test_scenario_comparison_workspace.py` (churn) | `3ee01a81e343a5e57f39f0032c4ac4d1e31c3dfaa6615703d26ddfb585f509e6` |

## 3. Per-family generation description

| Endpoint | Input | Output (persisted) |
|---|---|---|
| `POST /intelligence/correlation-reports` | left/right `SeriesSpecIn` + as-of window | Pearson r + Fisher interval + sample count + uncertainty + lineage |
| `POST /intelligence/regime-reports` | series + window | regime label + confidence + normalized features + evidence |
| `POST /intelligence/scenario-reports` | series + `ScenarioAssumptionsIn` + window | hypothetical result + assumptions + uncertainty + economic-usefulness |
| `POST /intelligence/portfolio-risk-reports` | series + `PortfolioRiskAssumptionsIn` + window | hypothetical market-series risk + uncertainty + sample count (no account/broker linkage) |
| `POST /intelligence/signal-validation-reports` | `SignalValidationScope` + actor | validation metrics + Wilson intervals + honest `outcome_data_status` |

All five return 201 with the existing Read models; the data-class label is appended to `notes`; the services' audit rows carry actor + correlation id. Request validation: bounds (`horizon_bars ≥ 1`, `stress_multiplier > 0`, `0 < tail_quantile < 0.5`) + UTC coercion at the schema boundary.

## 4. Generation evidence (POST → persisted rows, over the REAL corpus)

`b04_api_generation.log` (dev DB; 2 × 17,520 real OKX H1 bars ingested with `historical:real`):

```
POST correlation-reports:  id=3a33ae02… sample_count=17520 correlation_value=0.7321476734694274
                           notes="Research-only correlation context; not a signal and not causation.; data-class: historical:real"
POST regime-reports:       id=41a9a15e… sample_count=17520 regime_label="calm" confidence=0.6051…
                           notes="…; data-class: historical:real"
POST scenario-reports:     id=16e3ba1a… sample_count=17520 notes="Hypothetical research scenario; …; data-class: historical:real"
POST portfolio-risk-reports: id=25b29110… sample_count=17520 notes="Hypothetical market-series risk research; …; data-class: historical:real"
POST signal-validation-reports: id=123725d7… sample_count=1 (evidence fixture) outcome_data_status="not_available" (honest)
GET correlation-reports:   read-back returns the generated rows (unchanged contract)
Audit rows:                correlation_report 1 · regime_report 1 · scenario_report 1 · portfolio_risk_report 1 · signal_validation_report 1 (+ ingestion/operator events only)
```

## 5. Insufficient-data handling evidence

```
POST correlation-reports (right symbol absent):
  HTTP 422 {"detail":{"error_code":"CORRELATION_REQUIRES_THREE_ALIGNED_POINTS","detail":"…","insufficient_data":true}}
POST signal-validation-reports (empty scope):
  HTTP 422 {"detail":{"error_code":"SIGNAL_VALIDATION_EMPTY_SCOPE","detail":"…","insufficient_data":true}}
POST regime-reports (future as-of, test-pinned):
  HTTP 422 {"detail":{"error_code":"REGIME_FUTURE_AS_OF_REFUSED","…","insufficient_data":false}}
```

Pinned by tests: insufficient data produces the structured result and **zero fabricated report rows** (count asserted unchanged).

## 6. Non-actuation invariant evidence

- `test_b04_generation_mutates_nothing_but_the_report`: correlation generation changes the correlation table only — advisory-signal and model-artifact counts unchanged.
- `test_b04_router_has_no_execution_or_broker_surface`: no order/broker/execution/account/signal-emission code surface in the router.
- The dev-DB audit breakdown (§4) shows exactly five report rows and no actuation events.

## 7. Test evidence (executed)

| Run | Result | Log |
|---|---|---|
| B-04 fail-first probe (against the 24-element chain) | **8/8 failed** — POSTs returned 405; the static surface check failed (the FIND-2 gap, pinned) | `b04_probe_prefix.log` |
| B-04 generation suite (post-fix) | 8 passed | in `pytest_b04_postfix.log` |
| Affected W4 family sets (correlation/regime/scenario/portfolio/signal-validation/comparison) | 43 passed | in `pytest_b04_postfix.log` |
| **Full backend suite** | **522 passed, 1 warning, 152.93s** (514 + 8 new; 0 failed/skipped) | `pytest_b04_postfix.log` |
| Clone-side (applied patch content) | 48 passed, ruff clean, apply-check exit 0 | `b04_applycheck_transcript.txt` |

## 8. Deviations register

- **D1 — Six spec-driven test churns (fully disclosed).** Five W4 API tests pinned `POST → 405` ("read-only"); the BO authorizes the generation POSTs, so the superseded pins now assert `422` on a body-less/invalid POST (route exists, validation fires) — each file carries an inline "BO-B-04 supersession" comment. The scenario-comparison workspace test's "no generate endpoint" pin likewise: the collection POST now asserts 422 (validated body) while the three nonexistent paths (`/{id}`, `/generate`, `/compare`) keep their 404/405 assertions; the test name was updated to `…_and_generate_requires_valid_body`. No assertion weakened; every change is stricter.
- **D2 — RBAC depth.** Generation endpoints use `CurrentOperatorDep` — the intelligence-family pattern (the read surfaces' own dependency). Permission-granular RBAC on these routes is a B-07.2 concern per the roadmap; disclosed rather than silently approximated.
- **D3 — Data-class label mechanics.** The five services persist their own reports without a data-class field; the endpoints add the honest label to `notes` (distinct candle `source` values in the requested window) post-generation. Service math untouched per BO §3.
- **D4 — Signal-validation evidence fixture.** The dev DB had zero advisory signals (no inference — correct per the predictive deferral); one synthetic evidence row (explicitly labeled `B-04 signal-validation evidence fixture (synthetic; disclosed)`) was inserted to power the happy-path probe — precedent TD-UI-CONV-P02-SIG004-EVIDENCE-FIXTURE. Local gitignored DB only; no schema/service change.
- **D5 — No schema migration, no service-math change, no new dependency.**

## 9. Transmission manifest (CA-TRANSMIT-1 — relay-accurate, all hashes verified on the transmitted files)

| # | Declared artifact | Transmitted filename | sha256 |
|---|---|---|---|
| 1 | B-04 patch (chain position 25) | `b04.patch.txt` | `2704a8a2f264747f4f3ad539ce469f1404dc0f6362d5f7a854f2481ba98cbdc3` |
| 2 | Apply-check transcript (pristine clone, 24-chain) | `b04_applycheck_transcript.txt` | `1eb09e0d43ba74f119fb605d6fb1114cf9cc2a4e1aa63f3827dc5d951aaef279` |
| 3 | Fail-first probe log | `b04_probe_prefix.log.txt` | `df738d26c0f9d180424e00e394781b4f6c1aa9261628302f9b1dcdd83770473a` |
| 4 | Generation API probe log (Level I) | `b04_api_generation.log.txt` | `fbb18bba5e7def9d0d226cc8ded35e808b9a70d02f149ab4b05b6b2fc5ed7faf` |
| 5 | Full-suite log (522 passed) | `pytest_b04_postfix.log.txt` | `88ad86fac5ed6556c1681abdc73cbf90e1a914a5fb335443edd2cc76fbf67755` |
| 6 | Delivery report | `DELIVERY_REPORT_B-04.txt` | (declared in the DA closing message) |

The B-DATA corpus is already in ITRGA custody (reconstructed byte-identical in BO-B-DATA FINAL) — not re-transmitted. Every hash above resolves to a file in `/home/user/b04_transmission/` (sha256sum -c exit 0 this session).

## 10. Known limitations / technical debt

- Generation is **on-request only** (no scheduled/background hooks) — per BO §3, scheduled generation needs separate justification.
- The signal-validation family depends on persisted advisory signals; with the predictive track deferred, its real-data population awaits a future promoted model (the honest `outcome_data_status` field carries this).
- Carried: PROJECT_STATE.md inventory staleness; W3-U03 semantic-narrowing record; fingerprint-determinism hardening; CA-TRANSMIT-1 (relay discipline, applied this delivery).
- Register: TD-B04-UNIT added; TD-BML2-UNIT updated to CLOSED (APPROVED WITH OBSERVATIONS).

---

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
