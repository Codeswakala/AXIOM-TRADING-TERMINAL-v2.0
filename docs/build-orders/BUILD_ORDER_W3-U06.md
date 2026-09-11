# AXIOM BUILD ORDER — W3-U06

## Live Research Advisor: Monitoring, Drift & Health Alerts (inform a human, never act)

**Build Order ID:** W3-U06
**Wave:** 3 — Live Research Advisor · **Unit:** 06
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-15
**Authorized By:** ITRGA, following **W3-U05 APPROVED** (Platform v0.27.0; first operator UI; F-1 closed) +
operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001).
**Builds on:** W1-U02 observability (health/metrics) + W2-U10 drift-monitoring design (drift ≠ auto-retrain)
+ W3-U01..U05 (eligibility, signals, guardrails, live inference, advisory UI).
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver **operator-facing monitoring & alerts** for the Live Research Advisor — surfacing **market**,
**health**, and **drift** conditions as **inert alert records shown to a human.** Per the accepted Wave-3
plan §9 and `07_ML_SPEC` §Drift Monitoring, the single defining constraint (§9.3): **a drift/health alert
informs the operator and NEVER acts** — it never retrains, never changes a model, never triggers an
order/action. It carries the W2-U10 "drift ≠ auto-retrain" rule into the live operator-facing layer.

Alerts are the live analogue of the guardrail outcomes W3-U03 already persists: `MODEL_OUT_OF_DOMAIN`,
`MODEL_CALIBRATION_WARNING`, `MODEL_ECONOMICALLY_UNUSABLE`, `DRIFT_DETECTED`, `LIVE_DATA_STALE`,
`INFERENCE_HEALTH_DEGRADED`, `SIGNAL_WITHHELD` (plan §9.4). This unit **generates, persists, audits, and
exposes (read-only) alerts** — reusing W1-U02 observability and W2-U10 drift — and **stops at informing the
operator.** No execution, no auto-action, no automated remediation of any kind.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No auto-action / no auto-remediation of any kind (the headline).** An alert **must not** retrain a
  model, change a model's status, adjust a config, emit/withhold a signal on its own, place an order, or
  trigger any automated response. It **only records + informs.** Any alert→action path is an automatic FAIL
  (§9.3; W2-U10 drift≠auto-retrain; R17). Prove by named negative test (a `DRIFT_DETECTED`/degraded alert
  triggers **no** retrain/model-change/order/action) + grep.
- ❌ **No execution / orders / broker / paper trading; no execution controls in any alert UI.** Gate CLOSED
  (R17). An alert UI (if any) carries **no action buttons** beyond acknowledge/dismiss (which change only
  alert *read-state*, never the system). Prove by grep + (if UI) browser screenshot.
- ❌ **No model/config mutation from monitoring.** Monitoring **reads** (health/metrics via W1-U02; drift via
  W2-U10; signal/live-feed state) — it must not write to models, experiments, or config. Prove structurally.
- ❌ **No unaudited/unpersisted alert.** Every alert is **persisted + audited** (append-only); no in-memory-
  only alert. **Persisted-artifact committing proof (raw `SELECT` + API read-back) first submission.**
- ❌ **No false-precision / no raw-score-as-confidence in alerts** — alert content reuses the honest
  calibrated/economic/domain/freshness states already established (W3-U03).
- ❌ **No secrets/PII in alerts/logs** (§77); **no DB reach-around** (§16); **no live push that acts** —
  surfacing alerts to the operator (read-only API and/or a read-only UI indicator) is informational only.
- ❌ **No regression** (Wave-0/1 + W2 + W3-U01..U05). Full suite + **green CI (exit 0, capture the echo)** +
  parity smoke; prior gates green.
- ✅ **Preserve:** advisory/research-first, UX presentation-only, tz-UTC, observability, no execution controls
  (R-3), all prior hardening.

---

## 3. Scope — Components A–F

### Component A — Market + health monitoring (reuse W1-U02 observability; plan §9.1/§9.2)
- Surface **market** conditions (live-feed status, candle freshness, market-data lag, source authority,
  missing features, stale model/report links) and **health** conditions (backend health, DB latency, live
  adapter/WebSocket/inference/signal-store status) — computed from existing observability/state, not
  recomputed authoritatively. Read-only.

### Component B — Drift alerts (surface W2-U10; plan §9.3 — the headline constraint)
- Surface W2-U10 drift signals as **`DRIFT_DETECTED` alerts** with evidence. **Rules (proven):** the alert
  **never retrains, never changes the model, never triggers an order/action** — the operator sees the
  warning + evidence and decides. (Governance-gated remediation, if ever, is a future human-initiated
  action, not an alert side-effect.)

### Component C — Alert contract (inert, persisted, audited) + types (plan §9.4)
- An **alert record** (Alembic-migrated table) with: `alert_id`, `created_at` (UTC), `alert_type`
  (`MODEL_OUT_OF_DOMAIN`/`MODEL_CALIBRATION_WARNING`/`MODEL_ECONOMICALLY_UNUSABLE`/`DRIFT_DETECTED`/
  `LIVE_DATA_STALE`/`INFERENCE_HEALTH_DEGRADED`/`SIGNAL_WITHHELD`), severity, subject (model/market/feed),
  evidence/detail, correlation/lineage, read/ack state, `audit_correlation_id`. **Inert — no action/order
  payload, no remediation directive.** Every alert writes an **append-only audit event.**

### Component D — Read-only alert surface (API; optional read-only UI indicator)
- A **read-only, authenticated** alerts API (list/query/ack). If a UI indicator is added, it is **read-only
  + acknowledge/dismiss only** (changes alert read-state, never the system) — **no execution controls**
  (R-3), browser evidence if UI touched. No live push that acts.

### Component E — Governance, registers, ADR
- **ADR:** *Monitoring/Drift Alert Policy* (alerts inform, never act; drift ≠ auto-retrain). **Registers:**
  alert-auto-action / drift-auto-retrain / monitoring-mutates-model risks mitigated; update `PROJECT_STATE`/
  `CHANGELOG`; note W3-U07 (analytics)/U08 (closeout) deferrals.
- **Persisted proof:** alert records + audit shown via **raw `SELECT` + API read-back** (both, first
  submission).

### Component F — Verification & Delivery
- Full suite green (baseline **183** backend / **20** frontend) — 0 failed, **green CI (exit 0)**, no
  regression — **plus** new tests: alerts generated for market/health/drift conditions; **`DRIFT_DETECTED`/
  degraded alert triggers NO retrain / NO model-change / NO order / NO auto-action** (headline negative
  test); alerts inert (no action/order payload); monitoring does not mutate model/config; alerts persisted +
  audited; read-only alerts API (401/200; write limited to ack read-state; no emit/execute); prior gates
  (W3-U01..U05 + broker) green.
- Delivery Report per §5 (+ browser screenshot **only if** a UI indicator is added — showing no execution
  controls).

### Explicitly OUT of scope (later Wave-3 / Wave 6)
Performance analytics + confidence-viz depth (W3-U07); Wave-3 closeout/hardening (W3-U08); any execution/
order/broker/paper trading or automated remediation (Wave 6 — and forbidden regardless); external
notification providers (future gated). **No auto-action, no execution, no automated remediation in W3-U06.**

---

## 4. Success Criteria (Definition of Done)

- [ ] Market + health + drift conditions surfaced as **inert, persisted, audited** alerts (types per §9.4);
      reuse W1-U02 observability + W2-U10 drift (no authoritative recomputation).
- [ ] **Headline: a drift/degraded alert triggers NO retrain / NO model-change / NO order / NO auto-action**
      — proven by named negative test + grep; monitoring does not mutate model/config.
- [ ] Alert record inert (no action/order/remediation payload); every alert persisted + audited.
- [ ] Read-only authenticated alerts API (list/query/ack read-state only; no emit/execute); if UI indicator
      added, **no execution controls** (browser screenshot).
- [ ] Persisted proof (raw `SELECT` + API read-back) for alert records + audit (first submission).
- [ ] No execution/order/broker; gate CLOSED; no secrets; **green CI (exit 0 echo captured).**
- [ ] ADR + registers synced; full suite green (183/20 + new tests); no regression; W3-U01..U05 + W2 +
      broker tests still pass; conforms to `07_ML_SPEC` §Drift + 05 v2.0 (§15/§16/§77) + plan §9 + R-3.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **Operator test console** (raw, `collected N`): backend `pytest` **≥183 + new tests, 0 failed**; frontend
   `vitest` **≥20, 0 failed**; `ruff` clean; `tsc`/build clean.
2. **Migration evidence:** clean `alembic upgrade head` on `PostgresqlImpl` incl. the alerts table; new head.
3. **Alert-generation evidence (captured `-vv`):** alerts created for market/health/drift conditions with
   the correct `alert_type`.
4. **No-auto-action evidence (headline, captured `-vv`):** a `DRIFT_DETECTED`/degraded alert triggers **no**
   retrain / model-change / order / auto-action (negative test) + grep (no retrain/order/execute path from
   the alert code).
5. **Inert + read-only evidence:** alert has no action/order payload; alerts API list/query/ack works;
   **no emit/execute path**; unauth 401.
6. **Persisted-PG proof (both forms, first submission):** alert records + audit via raw `psql SELECT ≥1 row`
   + authenticated API read-back.
7. **(If UI indicator added) browser evidence:** read-only alert indicator, **no execution controls**,
   acknowledge/dismiss only.
8. **CI green on PostgreSQL** through completion, **`LOCAL_CI_EXIT_CODE: 0` echoed inline.**
9. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
10. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages.**

---

## 6. Standards & Constraints
Alerts inform, never act (§9.3; W2-U10 drift ≠ auto-retrain); **no auto-action/auto-remediation/execution**
(R17; §15 gate CLOSED); monitoring reads, never mutates model/config; inert + persisted + audited alerts;
read-only alerts surface (ack = read-state only); **no execution controls** (R-3); reuse W1-U02 observability
+ W2-U10 drift; no secrets (§77); tz-UTC; persisted-artifact committing proof (both forms) first submission;
green CI with exit-0 echo. Every change in the registers (R20). Cross-platform.

---

## 7. Process
Implement → internal verify (suite + alert generation + **no-auto-action negative test** + inert + persisted-
PG) → doc sync (PROJECT_STATE + registers + ADR) → Delivery Report with §5 evidence (operator-run, green,
no-auto-action proven, persisted proof both forms, CI exit-0) → **submit to ITRGA** → independent review →
corrections if required → approval → next Build Order (W3-U07). The DA does not self-approve, self-authorize
the next unit, add any auto-action/execution, or open the broker gate.

---

## 8. Priority Guidance (if staged)
**A (market/health monitoring) → B (drift alerts) → C (inert alert contract + audit) → D (read-only alerts
API/indicator) → E (ADR/registers) → F (verify, headline no-auto-action + persisted both forms).**
Highest-value/highest-risk: the **no-auto-action guarantee** — an alert that could retrain, change a model,
or trigger an order silently crosses the advisory→action line the entire wave defends; and **monitoring must
not mutate** what it watches. *Prove the drift alert changes nothing and triggers nothing — it only tells a
human.*

---

## 8b. Gate status
Research/advisory only — alerts **inform** the operator; they **never act**. No auto-retrain, no auto-
remediation, no execution (Wave 6), no execution controls (R-3), broker gate CLOSED; flow ends at Operator
Decision (§15). W3-U07 (Performance Analytics + Confidence Visualization) is the recommended next unit and
needs its own Build Order.

---

*ITRGA — Let the platform watch itself and warn the operator — drift, stale data, degraded health, a
withheld signal — but let a warning be only ever a warning: it retrains nothing, changes no model, places no
order, remediates nothing on its own. Prove the drift alert moves nothing but a human's attention. The
platform watches, reasons, and now alerts; it still does not act. We don't guess. We prove.*
