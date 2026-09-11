# AXIOM BUILD ORDER — W4-U05

## Institutional Intelligence: Portfolio/Risk Research Analytics (hypothetical, uncertainty-mandatory, NO account/broker/position linkage)

**Build Order ID:** W4-U05
**Wave:** 4 — Institutional Intelligence · **Unit:** 05
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **W4-U04 APPROVED — CLEAN** (Platform v0.34.0; scenario reports non-instruction) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07/08_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-4 guardrails **GR-1…GR-8**; this unit carries
**R-2, R-4, R-5, R-8** (`ITRGA_REVIEW_WAVE4_DESIGN_PLAN.md`).
**Governing plan:** `WAVE4_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §4.1 (artifact contract), §5.4
(portfolio/risk methodology/controls), §8 (**"Portfolio/risk analytics imply guaranteed returns" = HIGH**), §9.
**Builds on:** W4-U01…U04 (context/contract/approved deps, inline raw-SELECT + no-orphan audit standard,
look-ahead/non-signal/no-sizing patterns).
**Baseline to meet/exceed:** backend **218** / frontend **11 files · 25 tests**; Platform **v0.34.0**; head
**20260716_0021**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver **Portfolio/Risk Research Analytics** — a **hypothetical, research-level** view of risk/exposure
(e.g. drawdown, realized volatility, stress/VaR-style metrics) over an **as-of-bounded** window, **with
uncertainty + sample count + limitations**, persisted and auditable. This is **advisory research context for
the operator** — it describes hypothetical risk characteristics of market series, **not** a real portfolio,
account, or live position, and **never** implies a guaranteed/expected return (plan §5.4, §8 HIGH).

It reads persisted market data read-only, emits the W4-U01 `IntelligenceArtifactContract`, and is read-only.
It uses the **W4-U01-approved deps (numpy/pandas/scipy) or the pure-Python fallback** — nothing else.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **NO account/broker/position linkage (R-8 — KEYSTONE). MANDATORY NAMED TEST + GREP.** The analytics are
  **hypothetical/market-series-level only.** No real account id, broker account, live position/holding,
  order, or execution linkage may be introduced. Prove by: (a) **inert schema** — `\d` shows no
  account/broker/position/order columns; (b) a **named test** that the artifact carries no account/broker/
  position linkage; and (c) a **grep** (`broker_account|account_id|position_id|holding|portfolio_id.*broker|
  live_position|place_order|order_payload`) that is empty/benign (command + output). "Unless future governance
  authorizes" (plan §5.4) is **deferred to a future wave and is OUT OF SCOPE here.**
- ❌ **No guaranteed/expected-return framing (§8 HIGH).** Every metric is **hypothetical/research**; the
  artifact `limitations` (and any UI) state not-a-guarantee / not-financial-advice / hypothetical. No language
  implying assured profit or a real portfolio outcome. Prove by test (+ screenshot if UI).
- ❌ **No uncertainty-free risk metric (GR-7).** Drawdown / volatility / stress metrics each carry
  **uncertainty + sample_count**. No bare point estimate. Statistical evidence and economic usefulness remain
  **separate** — and economic usefulness is **REPORTED (R-5)**, independent + honest (may be `not_assessed`
  with a reason).
- ❌ **No look-ahead (R-2 — MANDATORY NAMED NEGATIVE TEST).** No data beyond `as_of_end` influences any metric.
  Named test (inject future data → excluded/unchanged); live `excluded_future_count` if feasible.
- ❌ **Not a signal / triggers nothing (R-6 standing).** A risk report is not a signal/instruction and mutates/
  triggers nothing. Inert contract + a "changes-nothing" named test; grep `auto_retrain|model.status =|
  advisory_status =|emit_signal` benign.
- ❌ **No un-audited persisted report (R-4 — INLINE).** New `portfolio_risk_reports` table triggers the
  persistence-capture control with the reinforced proof: Alembic head advance + committing script + **raw
  `psql SELECT ≥1 row` on `portfolio_risk_reports`** + **no-orphan audit JOIN** (`portfolio_risk_report.
  created`, `orphan_count 0`) — inline in the first submission. `research_status` mandatory.
- ❌ **No execution / order / broker / gate path** (GR-1/GR-3). Gate CLOSED. **R-3 wave-wide grep** (command +
  output, incl. `gate_open|allow_execution|order_size|position_size`), residuals disclosed + benign.
- ❌ **No unspiked compiled dependency** (R-1); numpy/pandas/scipy or pure-Python only. **No D-W2-001 breach.**
- ❌ **No client-side authoritative recompute** (GR-8) if any UI; presentation-only; browser screenshots
  mandatory if UI (hypothetical + not-guaranteed labels, uncertainty, **no execution/account controls**). If
  no UI, state so.
- ❌ **No regression** (Wave-0…W4-U04). Full suite green + **CI via documented Git-Bash path →
  `LOCAL_CI_EXIT_CODE: 0`** + parity smoke (Tee/marker-check at the **W4-U05** transcript).
- ✅ **Preserve:** advisory/research-first, tz-UTC, market-agnostic, all prior hardening, npm-audit 0,
  ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.** The R-8 no-account/position-linkage proof is the keystone.

---

## 3. Scope (Components A–D)

### A. Portfolio/risk service (backend, `institutional_intelligence`)
- Compute hypothetical risk metrics (e.g. max drawdown, realized volatility, a stress/VaR-style measure) over
  an as-of-bounded, backward-looking window from persisted candles (read-only), using approved numpy/scipy or
  the pure-Python fallback.
- Attach **uncertainty + sample_count + limitations** (hypothetical/not-guaranteed/not-a-real-portfolio) and
  an independent **economic_usefulness** field (R-5).
- Emit `IntelligenceArtifactContract` (`artifact_type = "portfolio_risk_report"`): metrics, uncertainty,
  method_version, config, input_lineage + source_artifact_ids, `economic_usefulness`, `research_status`,
  report_hash, audit_correlation_id. **No account/broker/position/order/sizing field.**

### B. Persistence + audit (R-4 — inline)
- New `portfolio_risk_reports` table + Alembic migration; committing repository/script; immutable
  `portfolio_risk_report.created` audit event; no orphan by construction.

### C. Read-only API
- `GET /api/v1/intelligence/portfolio-risk-reports` (list) + `GET …/{report_id}` (detail) — authenticated,
  read-only. Unauth → **401**; POST → **405/404**. No emit/execute endpoint.

### D. (Optional) presentation-only surface
- If any UI (e.g. a risk-analytics view): presentation-only, **hypothetical + not-guaranteed labels**, metrics
  with uncertainty, **no execution/account/position controls (R-3/R-8)**; **browser screenshots** from a
  reachable served session. If no UI, state so.

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL)

Report `DELIVERY_REPORT_W4-U05.md` + raw `operator results.md`. **Prove build identity first.**

1. **Build identity** — new files/ADR exist; v0.35.0; `git log -1 --oneline`.
2. **R-8 keystone** — named test: artifact carries **no account/broker/position linkage**; inert
   `\d portfolio_risk_reports` (no account/broker/position/order columns); grep (`broker_account|account_id|
   position_id|holding|live_position|place_order`) empty/benign (command + output).
3. **No guaranteed-return** — `limitations` state hypothetical/not-guaranteed/not-financial-advice; test; grep
   for guaranteed/expected-return language benign.
4. **GR-7 + R-5** — each metric shows uncertainty + sample_count; independent `economic_usefulness` field;
   bare point-estimate rejected.
5. **R-2 no-look-ahead** — named negative test PASSED (+ live `excluded_future_count` if feasible).
6. **R-6 non-signal / no mutation** — named "changes-nothing" test; grep benign.
7. **R-4 persistence (inline)** — Alembic `upgrade head` + `alembic current` (new head); committing script;
   **raw `psql SELECT ≥1 row` on `portfolio_risk_reports`**; **no-orphan audit JOIN** (`portfolio_risk_report.
   created`, `orphan_count 0`).
8. **API** — unauth **401**; **list 200** + **detail 200** (non-blank echoes); POST → **405/404**.
9. **Dependency discipline** — approved deps or fallback only; grep no unspiked import.
10. **R-3 wave-wide grep** — command + output; residuals disclosed + benign; Gate CLOSED (broker gate tests).
11. **Full regression** — backend `pytest` **≥ (218 + new)**, 0 failed; frontend green; ruff/tsc/build clean;
    npm audit 0.
12. **CI** — **documented Git-Bash invocation** → `==> Local CI equivalent complete` +
    **`LOCAL_CI_EXIT_CODE: 0`** (transcript labelled W4-U05).
13. **Browser screenshots** if any UI; else explicit "no UI this unit." **Parity smoke.**

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.35.0.
- [ ] **R-8 (keystone):** named test + inert `\d portfolio_risk_reports` (no account/broker/position/order
      columns) + empty/benign linkage grep. No live account/position/broker anywhere.
- [ ] No guaranteed/expected-return framing; hypothetical/not-financial-advice labels.
- [ ] **GR-7 + R-5:** every metric has uncertainty + sample_count; independent economic_usefulness; no bare
      point-estimate.
- [ ] **R-2** named no-look-ahead negative test PASSED.
- [ ] **R-6** non-signal / no-mutation (named test + benign grep).
- [ ] **R-4** `portfolio_risk_reports`: Alembic head advanced; committing script + **raw SELECT ≥1 row** +
      no-orphan audit JOIN — inline.
- [ ] Read-only API 401 / list-200 / detail-200 / POST-405; non-blank detail echoes.
- [ ] Only approved deps or fallback; no unspiked import; no D-W2-001 breach.
- [ ] **R-3** grep empty/benign (command+output); Gate CLOSED.
- [ ] No regression; full suite green; **CI via Git-Bash → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke; browser
      evidence if UI.
- [ ] DA does not self-approve, self-advance, build W4-U06+, adopt an unspiked dep, or open the Gate.

**A single CRITICAL, unmet mandatory evidence, or a red gate ⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA
approves W4-U05, advances to **v0.35.0**, and (on operator authorization) issues `BUILD_ORDER_W4-U06.md`
(Professional Signal Validation Extension) carrying **R-2/R-4/R-5/R-6** (+ raw-score-exclusion + no
cherry-picking, per plan §5.5).

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Signal-validation / dashboard / closeout (W4-U06/U07/U08, each own Build Order).
- Any account/broker/position/order/execution/**sizing** linkage; opening the Gate.
- Any unspiked compiled dependency; any per-market model / symbol-identity feature.
- Risk analytics framed as guaranteed/expected returns or as a real portfolio/account.
- Any Wave-5/6 work.

---

## 7. Notes to the Development Authority

The defining risk here is **"portfolio risk" drifting toward a real account/position.** The keystone is
**R-8**: these analytics are **hypothetical, market-series-level, with NO account/broker/position linkage** —
prove it by an inert `\d portfolio_risk_reports` (no such columns) + a named test + a linkage grep. Carry
uncertainty + sample_count on every metric (no false precision), keep economic-usefulness independent and
honest (R-5), never imply guaranteed returns, deliver the **raw SELECT + no-orphan audit inline**, and run CI
via the **documented Git-Bash path** for a clean exit 0 (transcript labelled W4-U05). Prove build identity
first; disclose grep residuals with output.

DA does not self-approve, self-advance the version, build W4-U06+, adopt an unspiked dependency, add
execution/broker/account linkage, or open the Gate. The next unit follows ITRGA's verdict + a new Build Order
+ operator authorization.

> **We don't guess. We prove.** — ITRGA
