# AXIOM BUILD ORDER — W2-U09

## ML Research: Economic Validation Framework

**Build Order ID:** W2-U09
**Wave:** 2 — Machine Learning Research Framework · **Unit:** 09
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-15
**Authorized By:** ITRGA, following **W2-U08 APPROVED** (Platform v0.20.0; calibration) + operator
authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this Build Order (Tier 8).
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001, market-agnostic).
**Builds on (honour, do not re-implement):** W2-U01 guard · W2-U02 query port · W2-U03 features · W2-U04
snapshot/split · W2-U05 experiment registry · W2-U06 model harness · W2-U07 statistical validation ·
W2-U08 calibration.
**Carries forward:** the **R-4 cost-input-provenance** note (W2-U03 review): economic cost inputs declared
as measured / provider-published / **assumed with sensitivity ranges**, never false precision.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver the **Economic Validation Framework** — the layer that answers the question statistical significance
and calibration cannot: *"after real trading frictions, is this model economically usable, or not?"* Per
`07_ML_SPEC` §Economic Validation (and plan §9.3): *"Machine learning success does not imply trading
success… A model may be statistically significant yet economically unusable. **Both conclusions shall be
reported independently.**"*

Every model shall be evaluated under **spread, commission, slippage, latency, liquidity, transaction
costs** (market impact = future). The **headline governance proof** (named in plan §W2-U09 evidence): a
model that is **statistically positive but economically negative** must be **reported as such — the two
verdicts kept separate**, so a good-looking accuracy/Brier never launders into an assumed edge once costs
bite.

This validates economic viability of model outputs as **research reports only**. It touches *trading-cost
concepts* but adds **no execution, no orders, no live signals, no broker connection** — costs are applied to
**hypothetical/backtested** research P&L, never to a real or dispatched trade.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution / orders / positions / broker connection / live signals — real, demo, or paper.**
  This unit reasons about *costs of hypothetical trades in a research report*; it must not place, simulate-
  as-executable, or dispatch anything. W1-U03 Governance Gate stays **CLOSED**; execution research is
  **Wave 6**, live signals **Wave 3**. **Applying costs to a research P&L is NOT execution** — but any code
  path that could route an intent to a broker/execution surface is an automatic FAIL (R17).
- ❌ **No statistical/economic conflation.** Statistical conclusions (W2-U07/U08) and economic conclusions
  **must be reported independently** (`07_ML_SPEC` §Economic Validation). A report that collapses them into
  one "is it good" verdict, or that hides a negative economic result behind a positive statistical one, is
  non-conformant — enforce separation (report both, labelled).
- ❌ **No undeclared / false-precision cost inputs (R-4 carry-forward).** Every cost input
  (spread/commission/slippage/latency/liquidity) must be **explicitly classified** measured / provider-
  published / **assumed**, and assumed values carried **with a range / sensitivity**, not a single fabricated
  number. A single-point cost with no provenance/sensitivity is non-conformant.
- ❌ **No leakage / non-temporal / off-governance evaluation.** Economic validation runs on the **same
  temporal, embargoed, pinned-experiment** outputs (W2-U04/U05/U07); guards stay active. No re-splitting,
  no peeking, no look-ahead in cost application.
- ❌ **No symbol identity as a feature (D-W2-001).** Market/timeframe/regime define cost/eval *slices*
  (required — costs differ by market), never re-enter the model input.
- ❌ **No cherry-picking cost scenarios** (R18). Scenarios are declared (e.g. optimistic/base/pessimistic);
  do not report only the flattering one.
- ❌ **No untested compiled dependency** (wheel-spike on Win/Py3.14.6 if adopted; pure-Python preferred).
- ❌ **No secrets/PII** (§77); **no DB reach-around** (§16).
- ❌ **No regression** (Wave-0/1 + W2-U01–U08). Full suite + prior guard/validation/calibration tests +
  parity smoke.
- ✅ **Preserve:** advisory/research-first, tz-UTC, observability, the full chain, reproducibility (seeded),
  all prior hardening. **Persistence-capture standing instruction applies** (committing-script + `SELECT ≥1
  row` proof for the new economic-report artifact in the FIRST submission).

---

## 3. Scope — Components A–G

### Component A — (Conditional) wheel-compatibility spike (staged sub-gate)
- If a compiled lib is adopted, install→import→smoke on Win/Py3.14.6 + pin versions; else pure-Python +
  stated. Never ship a failing import.

### Component B — Cost model (`07_ML_SPEC` §Economic Validation; plan §9.3; R-4)
- A **transaction-cost model** applying **spread, commission, slippage, latency, liquidity, transaction
  costs** to a hypothetical/backtested research P&L derived from a pinned-experiment model's outputs.
- **Every cost input classified** (measured / provider-published / assumed) with **assumed values ranged**;
  cost parameters may vary **per market class / timeframe** (costs legitimately differ by market). Declared,
  not fabricated.

### Component C — Independent economic vs. statistical conclusions (the separation mandate)
- Compute an **economic result** (e.g. net-of-cost return / P&L / a cost-adjusted metric) and present it
  **separately from** the statistical/calibration conclusions carried from W2-U07/U08 — both labelled, both
  in the report, neither overriding the other. Surface an explicit **"statistically-positive but
  economically-negative"** determination when it occurs.

### Component D — Cost-scenario sensitivity
- Report the economic result across **declared scenarios** (e.g. optimistic / base / pessimistic cost
  assumptions) so the conclusion's dependence on assumptions is visible — no single-point false precision.

### Component E — Economic report artifact (research-only) + headline negative proof
- Persist an **economic validation report** bound to experiment_id + model + (W2-U07) validation + (W2-U08)
  calibration reports: cost model + provenance, per-scenario economic result, the independent
  statistical/economic conclusions, per-slice results, **research-only** status, reproducible (seeded → same
  hash).
- **Headline test (named):** a **statistically-positive-but-economically-negative** fixture is reported as
  **economically unusable with the statistical result still shown separately** (the plan's owed scenario).
  Plus: a report conflating the two conclusions, or with undeclared/no-sensitivity costs, is **rejected**.

### Component F — Governance, registers, ADR
- **ADR:** *Economic Validation Framework* (cost model + provenance/sensitivity policy + independence rule).
- **Registers:** record economic-usability risk; **close the R-4 cost-input-provenance note** (W2-U03);
  reaffirm no-execution (R-PROD-01 Controlled by the gate). Update `PROJECT_STATE`/`CHANGELOG`. Note the
  only remaining Wave-2 unit is **W2-U10**.

### Component G — Verification & Delivery
- Full suite green (baseline **146** backend / **16** frontend) — 0 failed, no regression — **plus** new
  tests: cost model applies spread/commission/slippage/latency/liquidity; **statistically-positive-but-
  economically-negative reported separately** (headline); **conflated / undeclared-cost / no-sensitivity
  report REJECTED**; per-scenario sensitivity; per-slice; reproducible (seeded); no identity-as-feature; no
  execution/live-signal (grep + structural); guards active.
- Delivery Report per §5 (captured `-vv` named tests; **committing-script persisted-PG proof in this first
  submission** per the standing instruction).

### Explicitly OUT of scope (defer)
Multi-market generalization + drift + model-registry maturation (W2-U10); market-impact modelling (future);
any execution / paper trading / execution simulator (Wave 6); live/operator-facing signals (Wave 3); new
model families.

---

## 4. Success Criteria (Definition of Done)

- [ ] (If compiled dep) wheel spike passes on Win/Py3.14.6; else pure-Python + stated.
- [ ] Cost model applies **spread, commission, slippage, latency, liquidity, transaction costs** to a
      hypothetical research P&L; **inputs classified (measured/published/assumed) with sensitivity ranges**
      (R-4); per-market/timeframe cost params allowed.
- [ ] **Statistical and economic conclusions reported INDEPENDENTLY**; an explicit
      **statistically-positive-but-economically-negative** case is surfaced (headline proof).
- [ ] **Rejections proven:** conflated-conclusions / undeclared-cost / no-sensitivity report REJECTED.
- [ ] Per-scenario (optimistic/base/pessimistic) sensitivity reported; per-slice results.
- [ ] Economic report persisted (research-only), reproducible (seeded → same hash), bound to experiment/
      model/validation/calibration; **persisted-PG proof via committing script (first submission).**
- [ ] **No execution/orders/broker/live signal** (R17; gate CLOSED — grep + structural); no identity-as-
      feature (D-W2-001); no leakage/non-temporal; no cherry-picking; no secrets; no DB reach-around.
- [ ] ADR + registers synced (R-4 note closed); full suite green (146/16 + new tests); no regression;
      W2-U01–U08 tests still pass; conforms to `07_ML_SPEC` §Economic Validation / §Research Integrity +
      05 v2.0 (§15/§16/§77) + D-W2-001.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **(If applicable) wheel-spike evidence.**
2. **Operator test console** (raw, `collected N`): backend `pytest` **≥146 + new tests, 0 failed**;
   frontend `vitest 16`; `ruff` clean; `tsc`/build clean.
3. **Migration evidence** (if schema added for economic reports): clean `alembic upgrade head` on
   `PostgresqlImpl`, new head shown. (If none, state so.)
4. **Cost-model evidence:** the model applying the full cost set to a research P&L, with **cost inputs
   labelled measured/published/assumed + sensitivity** (R-4).
5. **Independence + headline evidence (captured `-vv`):** a **statistically-positive-but-economically-
   negative** case reported with **both conclusions shown separately**; and a **conflated / undeclared-cost /
   no-sensitivity report REJECTED**.
6. **Scenario sensitivity evidence:** economic result across optimistic/base/pessimistic.
7. **Reproducibility evidence:** seeded → same report/hash.
8. **Persisted-PG proof (committing-script method — FIRST submission, per standing instruction):** the
   economic-report row via raw `psql SELECT` returning ≥1 row (+ its audit event), bound to experiment/model.
9. **No-execution / no-live-signal / no-identity evidence:** shown grep (R7: cmd + empty output) that no
   execution/order/broker/live-signal path and no identity-as-feature was introduced.
10. **CI green on PostgreSQL** through completion, fail-closed.
11. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
12. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages**; economic result
    stated **honestly with its cost provenance/sensitivity.**

---

## 6. Standards & Constraints
Clean architecture / bounded context (ML Research owns economic validation); **statistical & economic
conclusions independent** (`07_ML_SPEC` §Economic Validation); **cost inputs provenance-classified +
sensitivity** (R-4; no false precision); **no execution/orders/broker/live signal** (R17; §15 gate CLOSED —
costs applied to hypothetical research P&L only); **temporal/leak-free/pinned** (guards active; R18); **no
identity as feature** (D-W2-001, slicing only); **reproducible** (seeded); **research-only** report;
target-proven deps only; no secrets (§77); tz-UTC; **persisted-artifact committing proof first submission**
(standing instruction). Every change in the registers (R20). Cross-platform (Windows + docker/PostgreSQL).

---

## 7. Process
Implement (spike first if needed) → internal verify (suite + cost model + independence/headline + rejections
+ sensitivity + reproducibility + persisted-PG) → doc sync (PROJECT_STATE + registers + ADR; **close R-4**)
→ Delivery Report with §5 evidence (operator-run, green, stat-vs-economic separate, costs provenance+
sensitivity, persisted report shown, honest) → **submit to ITRGA** → independent review → corrections if
required → approval → next Build Order (W2-U10). The DA does not self-approve, does not self-authorize the
next unit, and does not open the broker gate or emit live signals.

---

## 8. Priority Guidance (if staged)
**A (wheel spike if needed) → B (cost model + provenance/sensitivity) → C (independent stat/economic
conclusions) → E-headline (statistically-positive-but-economically-negative reported separately + reject
conflation) → D (scenarios) → F (ADR/registers, close R-4) → G (verify + persisted-PG first-submission).**
Highest-value/highest-risk: the **independence mandate** and the **statistically-positive-but-economically-
negative headline** — the entire point of economic validation is that a good-looking model can still lose
money after costs, and the framework must *say so plainly*. And the **no-execution boundary** (R17): this
unit reasons about trading costs, so be doubly sure it never touches an execution/broker path.

---

## 8b. Gate status
Research/advisory only — **no live signals (Wave 3), no execution (Wave 6), broker gate CLOSED.** Economic
validation produces research reports on *hypothetical* P&L, never a tradeable signal or an order. **W2-U10
(Multi-Market Generalization + Model Registry / Drift) is the LAST Wave-2 unit** — after it, the ML Research
Framework milestone ("Research Framework Complete") is in reach; it needs its own Build Order.

---

*ITRGA — Statistical significance and good calibration are necessary, not sufficient: a model can be right
often, well-calibrated, and still bleed money once spread, commission, slippage, latency, and liquidity are
paid. Report the two verdicts side by side and never let a clean accuracy launder into an assumed edge —
and remember this unit only ever spends *hypothetical* money: no order, no broker, no signal. We don't
guess. We prove.*
