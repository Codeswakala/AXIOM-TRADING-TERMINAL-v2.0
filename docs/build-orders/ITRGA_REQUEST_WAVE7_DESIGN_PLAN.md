# ITRGA REQUEST FOR WAVE 7 ENGINEERING DESIGN PLAN — "INSTITUTIONAL PLATFORM"

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Document type:** Pre-wave Design Plan Request + Pre-registered Guardrails
**Date:** 2026-07-18
**Platform of record:** v0.54.0 · Alembic head `20260717_0033` · backend **350 passed** · frontend **18 files / 58 tests**
**Governing anchors:** `04_PROJECT_ROADMAP.md` (Wave 7 — Institutional Platform, the **FINAL** wave); `05_SYSTEM_ARCHITECTURE.md` v2.0 §15/§16/§17/§43/§46/§48 + RBAC/API-auth/multi-user architectural concerns + §68 Scalability; `07_ML_SPEC.md`; `08_UI_UX_SPEC.md`; `10_CONSTITUTIONAL_HIERARCHY.md`; D-W2-001 (LOCKED).
**Motto:** *We don't guess. We prove.*

---

## 0. Status & Instruction

Wave 6 is **CLOSED** ("Execution Research Environment Complete," v0.54.0). The Operator has **authorized the opening of Wave 7 — Institutional Platform**, the roadmap's **last wave**.

Per the non-negotiable wave-opening pattern (Waves 2/3/4/5/6 each opened with pre-registered guardrails + an ITRGA-requested Engineering Design Plan reviewed **before** any unit Build Order), **no W7 unit Build Order will be issued until the DA delivers a Wave 7 Engineering Design & Implementation Plan and the ITRGA has reviewed and accepted it** (accept-with-refinements pattern).

Wave 7 turns AXIOM into a **complete institutional research terminal** — but "institutional platform" must **not** become an execution or real-money terminal, and its new surface (external **API ecosystem**, **plugin architecture**, **multi-user readiness**) introduces the **largest attack/abuse surface of the whole project.** The guardrails below preserve everything proven across Waves 0–6 and fence the new surface hard.

---

## 1. Roadmap-named Wave 7 components (and how each is fenced)

Roadmap names: *Workspace customization · Portfolio dashboard · Research management · Strategy laboratory · Plugin architecture · API ecosystem · Advanced reporting · Enterprise scalability · Multi-user readiness.* Milestone: **"Institutional Platform Complete."**

| Component | Permitted Wave-7 interpretation (research/advisory, Gate CLOSED) | Hard prohibition |
|---|---|---|
| **Workspace customization** | Per-operator layout/preferences over existing research surfaces; presentation-only (§30/§11.1). | No new actuation control; no customization that surfaces execution/order/broker affordances. |
| **Portfolio dashboard** | **Research** aggregation/visualization over existing advisory/simulated artifacts; hypothetical/labelled. | No real account/position/balance/margin/P&L; no live portfolio state; no sizing that actuates. |
| **Research management** | Organize/tag/search existing governed research artifacts (signals, reports, plans, journals, simulations). | No mutation of governed artifacts' content/audit; no new persisted artifact without persistence-capture. |
| **Strategy laboratory** | Research/simulation experimentation reusing the Wave-6 simulation + pre-registration + no-look-ahead machinery. | No live/broker/order path; no real-money backtest-to-live bridge; carries R6-7 (uncertainty, no cherry-picking, no look-ahead). |
| **Plugin architecture** | Extension **only through published extension contracts** (§17); core independent of plugin impls (report exporters, chart types, analytics). | **No plugin may reach a broker/order/account/live seam, open the Gate, exfiltrate secrets/PII, or bypass audit.** Plugins are sandboxed to contracts. |
| **API ecosystem** | Documented, **authenticated**, versioned read/research API contracts (§ approved API contracts). | No execution/order/account endpoint; no unauthenticated data exposure; no secrets/PII leak; rate-limited/abuse-guarded. |
| **Advanced reporting** | Report generation/export over existing artifacts with uncertainty + disclaimers (stat≠economic). | No real-P&L/guaranteed-return; no report that asserts execution suitability. |
| **Enterprise scalability** | Performance/observability/scale of the research platform (§68). | No scale feature that weakens governance, audit, or the Gate. |
| **Multi-user readiness** | **Readiness** — coarse roles / RBAC scaffolding / API-auth / per-operator scoping over the existing `operators` identity. | Not production SSO/MFA unless separately governed; must not weaken auth; no privilege that can open the Gate or reach execution. |

The DA is **not** obligated to build every named component in Wave 7 and **should not** over-scope; propose the smallest coherent, safely-fenced set and sequence it.

---

## 2. PRE-REGISTERED WAVE 7 GUARDRAILS (binding acceptance criteria)

**Constitutional (carried, non-negotiable):**
- **GR7-1 — Gate stays CLOSED.** The Constitutional Governance Gate remains CLOSED for all of Wave 7. No unit, **no plugin, and no API endpoint** may open it or reach a broker/order/account/live/real-money seam. Any change = **GOVERNANCE_AMENDMENTS amendment + Operator + ITRGA** (three-party act, never a feature-unit/plugin code change).
- **GR7-2 — Research/advisory only, by construction.** No live execution, no real account/position/balance/margin/capital/P&L path — even via a plugin, API call, portfolio dashboard, or strategy lab. Prove absence (endpoints/plugins provably cannot reach an execution seam).
- **GR7-3 — §16 broker containment + §17 plugin containment.** Broker logic only in External Integration; **plugins interact only through published extension contracts** and the core stays independent of plugin implementations. Grep/structural-provable.
- **GR7-4 — Uncertainty-mandatory & stat≠economic (07_ML_SPEC)** on any analytic/report/portfolio/strategy output; no cherry-picking; no real-P&L/guaranteed-return. Option A / D-W2-001 LOCKED (no symbol-identity feature without amendment).

**New-surface security (EXTRA for Wave 7 — largest attack surface):**
- **GR7-5 — API ecosystem is authenticated, authorized, versioned, and abuse-guarded.** Every new endpoint requires auth (401 without token proven), enforces per-operator scoping, is rate-limited/guarded, exposes **no** execution/order/account surface, and leaks **no secrets/PII** (§77). Prove: unauth→401, forbidden endpoints absent (405/404), no secret in payloads.
- **GR7-6 — Plugins are sandboxed & least-privilege.** A plugin may only use published read/research extension contracts; it cannot import broker logic, open sockets to venues, read secrets/other operators' data, mutate governed artifacts, or bypass audit. Prove with a containment test + a hostile-plugin refusal test (analogous to the assistant anti-injection proofs of Wave 5).
- **GR7-7 — Multi-user readiness must not weaken auth or isolate poorly.** Roles/RBAC scaffolding must default-deny, scope data per operator (no cross-operator leakage — prove with a two-operator isolation test), and grant **no** role the ability to open the Gate or reach execution. The standing security debt (dev `admin/admin123`, no refresh rotation, WS-JWT-in-query TD-022, no full RBAC) should be **addressed as readiness/hardening here** or explicitly deferred with justification — not silently shipped as production auth.
- **GR7-8 — No secrets/PII in telemetry, reports, exports, API, or plugin surfaces (§77).** Prove with the standing secret-marker/no-leak checks extended to the new surfaces.

**Method / evidence (standing, carried):**
- **GR7-9 — Persistence-capture control.** Any new persisted artifact/table owes, on FIRST submission: committing script + raw `psql SELECT ≥1 row` on the CORRECT table + a matching immutable **no-orphan audit JOIN** (`orphan_count 0`) — INLINE. API read-back does NOT substitute (W4-U02/W6-U04 C-1). `operator_id → operators.id` (no `users` table).
- **GR7-10 — UI judged in the browser.** Mandatory served-session screenshots (SIMULATED/research framing, **no execution/actuation controls**, logged-out block). Sandbox-only/report-claim shots ⇒ WITHHELD/CONDITIONAL.
- **GR7-11 — CI via documented Git-Bash path** → `==> Local CI equivalent complete` + inline `LOCAL_CI_EXIT_CODE: 0`. (Note the resolved TD-W6-CI-AUDIT: if the CI `npm audit` step hits a TLS-intercept/offline registry, fix the network path/CA or make audit degrade gracefully — never `strict-ssl false`.)
- **GR7-12 — No unspiked dependency.** Any new compiled / LLM / tokenizer / broker-SDK / plugin-runtime / API-framework dependency owes its own wheel-compat spike; a broker SDK remains barred (GR7-1/GR7-3).
- **GR7-13 — External LLM stays a FUTURE hard-gated separate Build Order** (R5-2). Never inside a Wave-7 feature/plugin unit.

---

## 3. What the Design Plan must contain

The DA shall deliver `WAVE7_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` containing:

1. **Scope & non-scope** — which roadmap components are in Wave 7, which are deferred, and why (favor the smallest safe set).
2. **Constitutional + security fence map** — for each proposed component, the §1 row: permitted interpretation + the concrete mechanism that makes each prohibition impossible **by construction** (Gate-closed, no-execution, §16/§17 containment, auth/scoping/no-leak).
3. **Unit decomposition** — one-unit-per-Build-Order (operator-agreed policy), sequenced. **W7-U01 MUST be the smallest safe slice that proves the institutional-platform safety/foundation envelope BEFORE any feature** — e.g. the API-auth/RBAC-readiness or plugin-contract **safety seam** ("prove the lock before the door," W3-U01/W4-U01/W5-U01/W6-U01 precedent). Recommend W7-U01 = the API/plugin/multi-user **security foundation** (auth + default-deny + no-execution-surface + containment), not a feature.
4. **Data model** — any new tables/artifacts with persistence-capture (GR7-9) + Alembic head progression from `20260717_0033`.
5. **Security & containment test plan** — auth (401/403), per-operator isolation (two-operator test), plugin sandbox + hostile-plugin refusal, API no-execution-surface, no-secret/PII leak, Gate-closed.
6. **UI plan** — research-framed, no execution/actuation controls, browser-evidence plan (GR7-10).
7. **Analytics/reporting method** — uncertainty, stat≠economic, no cherry-picking (GR7-4).
8. **Dependency declaration** — explicit statement of any new dep (API framework, plugin runtime, RBAC lib) + its spike plan; broker SDK barred outright.
9. **Risk register** — with the **falsification method** for each risk (proven, not "mitigated"), especially for plugin escape, API abuse, cross-operator leakage, and any execution-surface exposure.
10. **Disposition of standing security debt** — how Wave 7 addresses or explicitly defers `admin/admin123`, refresh rotation, WS-JWT-in-query (TD-022), full RBAC/MFA.

---

## 4. Process from here

1. **DA → Operator → ITRGA:** deliver `WAVE7_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md`.
2. **ITRGA:** review line-by-line → `ITRGA_REVIEW_WAVE7_DESIGN_PLAN.md` (ACCEPTED-WITH-REFINEMENTS pattern; refinements R7-n pre-registered as binding).
3. **On operator authorization:** `BUILD_ORDER_W7-U01.md` (smallest safe slice — the security/foundation envelope).
4. **Per unit thereafter:** on "authorized" → next `BUILD_ORDER_W7-U0n.md`; on delivery → verify + verdict + onboarding bump + present. Final unit = Wave-7 closeout → milestone **"Institutional Platform Complete"** (and, as the roadmap's last wave, a candidate for overall platform completion).

---

## 5. Reviewer posture reminder (unchanged)

- Never approve on report-claims alone (Level-IV lowest). Operator-run evidence on target is MANDATORY.
- A single CRITICAL or unmet mandatory evidence ⇒ **APPROVAL WITHHELD**. A red gate is a finding, never relabeled green (investigate env-flakes; don't relabel).
- Verify build identity FIRST (unit id + version in the pack; watch for stale/concatenated re-attachments).
- CONDITIONAL only when every *risk* item is proven and a *named* proof item is missing; superseded by a `_FINAL` on closure.
- Persistence-capture is raw `psql` SELECT + no-orphan audit JOIN — API read-back never substitutes.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
