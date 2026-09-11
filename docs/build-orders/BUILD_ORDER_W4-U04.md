# AXIOM BUILD ORDER — W4-U04

## Institutional Intelligence: Scenario Simulation Research Reports (hypothetical, as-of, uncertainty-mandatory, NOT an instruction)

**Build Order ID:** W4-U04
**Wave:** 4 — Institutional Intelligence · **Unit:** 04
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **W4-U03 APPROVED + OBS-1 CLOSED (residual-free)** (Platform v0.33.0) +
operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07/08_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-4 guardrails **GR-1…GR-8**; this unit carries
**R-2, R-4, R-5, R-6** (`ITRGA_REVIEW_WAVE4_DESIGN_PLAN.md`).
**Governing plan:** `WAVE4_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §4.1 (artifact contract), §5.3
(scenario methodology/controls), §8 (**"Scenario output treated as trade instruction" = CRITICAL risk**), §9.
**Builds on:** W4-U01 (context/contract/approved deps) + W4-U02/U03 (persistence+audit, inline raw-SELECT +
no-orphan audit standard, look-ahead/non-signal patterns).
**Baseline to meet/exceed:** backend **211** / frontend **11 files · 25 tests**; Platform **v0.33.0**; head
**20260716_0020**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver **Scenario Simulation Research Reports** — a **hypothetical, counterfactual** research artifact that
explores "what-if" outcomes over an **as-of-bounded** window (e.g. how a normalized price path would behave
under an assumed shock/parameter), **with explicit assumptions, uncertainty, and limitations**, persisted and
auditable. This is the **highest-risk framing in Wave 4**: a scenario must be **prominently labelled
hypothetical and can NEVER be, contain, or be read as a trade instruction, order, or position sizing** (plan
§5.3, §8 CRITICAL). It is research context for the operator — nothing acts on it.

It reads persisted market data read-only, emits the W4-U01 `IntelligenceArtifactContract`, and is read-only.
It uses the **W4-U01-approved deps (numpy/pandas/scipy) or the pure-Python fallback** — nothing else.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **A scenario is NOT an instruction/order/sizing (R-6 — ELEVATED; §8 CRITICAL). MANDATORY NAMED TESTS.**
  A scenario report may not contain, emit, or be promoted into an order payload, position size/quantity,
  stop/target, broker call, advisory signal, or any action. Prove by: (a) the **inert contract** (rejects
  order/remediation/signal keys — inherited from W4-U01, extended to reject sizing/quantity/stop_loss/
  take_profit); (b) a **named test that a scenario artifact carries no order/sizing/execution payload**; and
  (c) a **named "changes-nothing / triggers-nothing" test** (W3-U06 keystone). Prove structurally + by grep.
- ❌ **Not prominently labelled hypothetical.** The artifact `limitations`/framing (and any UI) **must** state
  the scenario is **hypothetical / counterfactual research, not a prediction, not a guarantee, not a trade
  instruction.** No guaranteed/expected-return language anywhere. Prove by test (+ screenshot if UI).
- ❌ **No look-ahead (R-2 — MANDATORY NAMED NEGATIVE TEST).** No data beyond `as_of_end` may influence the
  scenario baseline/inputs. Prove by a named test (inject future data → excluded/unchanged), W3-U04 style;
  ideally a live artifact `excluded_future_count` too.
- ❌ **No uncertainty-free scenario (GR-7).** Every scenario outcome carries **uncertainty + the stored
  assumptions/inputs** that produced it. No point-estimate implying a definite future.
- ❌ **Economic usefulness REPORTED, not merely "separate" (R-5).** The artifact **shall** carry an explicit
  economic-usefulness verdict/limitations field **independent** of any statistical/simulation result —
  "a scenario being computable ≠ tradable/economically useful," reported as an independent conclusion (may be
  `not_assessed` with a reason, as W4-U02/U03, but the field must exist and be honest).
- ❌ **No un-audited persisted report (R-4 — INLINE, as W4-U03).** New `scenario_reports` table triggers the
  persistence-capture control with the reinforced proof: Alembic head advance + committing script + **raw
  `psql SELECT ≥1 row` on `scenario_reports`** + **no-orphan audit JOIN** (`scenario_report.created`,
  `orphan_count 0`) — delivered inline in the first submission. `research_status` mandatory; **assumptions +
  inputs stored** (plan §5.3).
- ❌ **No execution / order / broker / gate path** (GR-1/GR-3). Gate stays CLOSED. Prove by **R-3 wave-wide
  grep** (command + output, incl. `gate_open|allow_execution|order_size|position_size|quantity`), residuals
  disclosed + benign.
- ❌ **No unspiked compiled dependency** (R-1 standing). numpy/pandas/scipy (approved) or pure-Python only.
- ❌ **No D-W2-001 breach** — normalized/generalized inputs, no symbol-identity feature, no per-market model.
- ❌ **No client-side authoritative recompute** (GR-8) if any UI is added — presentation-only; browser
  screenshots mandatory if UI (label hypothetical, uncertainty, **no action controls**). If no UI, state so.
- ❌ **No regression** (Wave-0/1/2/3 + W4-U01/U02/U03). Full suite green + **CI via the documented Git-Bash
  path → `LOCAL_CI_EXIT_CODE: 0`** + parity smoke. (Point Tee/marker-check at the **W4-U04** transcript.)
- ✅ **Preserve:** advisory/research-first, tz-UTC, market-agnostic, all prior hardening, npm-audit 0,
  ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.** Given the CRITICAL risk, the R-6 non-instruction/no-sizing proof is the
keystone of this unit.

---

## 3. Scope (Components A–D)

### A. Scenario service (backend, `institutional_intelligence`)
- Compute a **hypothetical/counterfactual** outcome over an as-of-bounded, backward-looking baseline from
  persisted candles (read-only) under **explicit stored assumptions** (e.g. an assumed return shock / volatility
  multiplier / horizon), using approved numpy/scipy or the pure-Python fallback.
- Attach **assumptions + inputs + uncertainty + limitations** (hypothetical/not-a-prediction/not-an-instruction)
  and an **economic-usefulness field (R-5)**.
- Emit `IntelligenceArtifactContract` (`artifact_type = "scenario_report"`): scenario outcome(s), assumptions,
  uncertainty, method_version, config, input_lineage + source_artifact_ids, `economic_usefulness`,
  `research_status`, report_hash, audit_correlation_id. **No order/sizing/quantity/stop/target/signal field.**

### B. Persistence + audit (R-4 — inline)
- New `scenario_reports` table + Alembic migration; committing repository/script; immutable
  `scenario_report.created` audit event; no orphan by construction; assumptions + inputs persisted.

### C. Read-only API
- `GET /api/v1/intelligence/scenario-reports` (list) + `GET …/{report_id}` (detail) — authenticated,
  read-only. Unauth → **401**; POST → **405/404**. No emit/execute endpoint.

### D. (Optional) presentation-only surface
- If any UI (e.g. a scenario view): presentation-only, **prominently labelled hypothetical**, shows
  assumptions + uncertainty + limitations, has **no execution/order/sizing controls (R-3)** and no
  action affordance; **browser screenshots** from a reachable served session. If no UI, state so.

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL)

Report `DELIVERY_REPORT_W4-U04.md` + raw `operator results.md`. **Prove build identity first.**

1. **Build identity** — new files/ADR exist; v0.34.0; `git log -1 --oneline`.
2. **R-6 keystone (elevated)** — named test(s): scenario artifact carries **no order/sizing/quantity/stop/
   target/signal payload**; scenario **triggers/changes nothing**; inert-schema citation (`\d scenario_reports`
   shows no such columns).
3. **Hypothetical labelling** — a produced report whose `limitations` state hypothetical/not-a-prediction/
   not-an-instruction; test asserting the framing; no guaranteed-return language (grep).
4. **R-2 no-look-ahead** — named negative test PASSED (+ live `excluded_future_count` if feasible).
5. **Uncertainty + assumptions (GR-7)** — report shows outcome + uncertainty + stored assumptions/inputs;
   bare point-estimate rejected.
6. **R-5 economic usefulness** — the report carries an explicit `economic_usefulness` verdict/limitations field
   independent of the simulation result (honest; `not_assessed` + reason acceptable).
7. **R-4 persistence (inline)** — Alembic `upgrade head` + `alembic current` (new head); committing script;
   **raw `psql SELECT ≥1 row` on `scenario_reports`**; **no-orphan audit JOIN** (`scenario_report.created`,
   `orphan_count 0`).
8. **API** — unauth **401**; **list 200** + **detail 200** (non-blank echoes of key fields); POST → **405/404**.
9. **Dependency discipline** — approved deps or fallback only; grep confirms no unspiked import.
10. **R-3 wave-wide grep** — command + output (incl. `order_size|position_size|quantity|gate_open|
    allow_execution`); residuals disclosed + benign; Gate CLOSED (broker gate tests).
11. **Full regression** — backend `pytest` **≥ (211 + new)**, 0 failed; frontend green; ruff/tsc/build clean;
    npm audit 0.
12. **CI** — **documented Git-Bash invocation** `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` →
    `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** (Tee/marker-check at the W4-U04
    transcript — retire the leftover filename label).
13. **Browser screenshots** if any UI; else explicit "no UI this unit." **Parity smoke.**

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.34.0.
- [ ] **R-6 (keystone):** named tests prove scenario carries **no order/sizing/execution/signal payload** and
      triggers nothing; inert `\d scenario_reports` (no order/sizing/quantity/stop/target columns).
- [ ] Scenario **prominently labelled hypothetical**; no guaranteed/expected-return language.
- [ ] **R-2** named no-look-ahead negative test PASSED.
- [ ] Every scenario carries **uncertainty + stored assumptions/inputs**; bare point-estimate rejected.
- [ ] **R-5** explicit `economic_usefulness` field, independent + honest.
- [ ] **R-4** `scenario_reports`: Alembic head advanced; committing script + **raw SELECT ≥1 row** + no-orphan
      audit JOIN (`scenario_report.created`, orphan 0) — inline.
- [ ] Read-only API 401 / list-200 / detail-200 / POST-405; non-blank detail echoes.
- [ ] Only approved deps or fallback; no unspiked import; no D-W2-001 breach.
- [ ] **R-3** grep empty/benign (command+output); Gate CLOSED; no execution/broker/sizing path.
- [ ] No regression; full suite green; **CI via Git-Bash path → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke;
      browser evidence if UI.
- [ ] DA does not self-approve, self-advance, build W4-U05+, adopt an unspiked dep, or open the Gate.

**A single CRITICAL, unmet mandatory evidence, or a red gate ⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA
approves W4-U04, advances to **v0.34.0**, and (on operator authorization) issues `BUILD_ORDER_W4-U05.md`
(Portfolio/Risk Research Analytics) carrying **R-2/R-4/R-5/R-8** (R-8 = no account/broker/position linkage).

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Portfolio/risk/signal-validation features (W4-U05/U06, each own Build Order).
- Any execution/order/broker/account/position/**sizing** path; opening the Gate.
- Any unspiked compiled dependency; any per-market model / symbol-identity feature.
- A scenario framed/emitted/read as a trade instruction, order, sizing directive, or guaranteed/expected
  return.
- Any Wave-5/6 work.

---

## 7. Notes to the Development Authority

This is the **highest-risk unit of Wave 4** — the plan itself flags "scenario treated as trade instruction" as
**Critical**. So the keystone proof is **R-6**: a scenario is hypothetical research that **cannot carry a
sizing/order/execution/signal payload and triggers nothing** — prove it with named tests + an inert
`\d scenario_reports` (no quantity/stop/target/order columns) + a mutation-aware grep. Label it hypothetical
prominently, carry uncertainty + stored assumptions, report economic-usefulness honestly (R-5), and deliver
the **raw SELECT + no-orphan audit inline** (as W4-U03). Use the **documented Git-Bash CI invocation** so the
exit code is a clean 0 (no WSL artifact), and point the transcript at W4-U04. Prove build identity first;
disclose grep residuals with output.

DA does not self-approve, self-advance the version, build W4-U05+, adopt an unspiked dependency, add
execution/broker/sizing, or open the Gate. The next unit follows ITRGA's verdict + a new Build Order +
operator authorization.

> **We don't guess. We prove.** — ITRGA
