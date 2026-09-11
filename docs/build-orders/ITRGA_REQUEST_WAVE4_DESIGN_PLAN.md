# ITRGA REQUEST — WAVE 4 CONSTITUTIONAL GUARDRAILS + DESIGN PLAN

| Field | Value |
|---|---|
| Issuing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Wave | **4 — Institutional Intelligence** |
| Roadmap objective (Tier-3 `04_PROJECT_ROADMAP`) | "Expand analytical capabilities." Milestone: **Institutional Intelligence Layer Complete** |
| Status | **GUARDRAILS PRE-REGISTERED (binding) · DESIGN PLAN REQUESTED** |
| Date | 2026-07-16 |
| Precedent | Wave-2 and Wave-3 each opened with an ITRGA-requested Design Plan reviewed/accepted before any unit Build Order (`ITRGA_REQUEST_WAVE2/3_DESIGN_PLAN.md`) |
| Precondition | Wave-3 residual hardening (`BUILD_ORDER_W3-U08.1_HARDENING.md`, OBS-1/OBS-2) approved first |

> **We don't guess. We prove.** Design within the boundaries; ITRGA reviews the design before anything is built.

---

## 1. Purpose & separation of responsibilities

Wave 3 ("Professional Advisor Platform Complete", v0.30.0) is closed. Wave 4 expands **analytical/research and
operator decision-support** capability — it does **not** move the platform toward autonomy or execution. Per
the established separation: **the Development Authority designs the implementation; the ITRGA determines
whether the proposed design remains constitutionally compliant.** Accordingly, ITRGA first **pre-registers the
binding constitutional guardrails below**, then **requests a comprehensive Wave-4 Design Plan**, which ITRGA
will independently review **before any Wave-4 Build Order is issued.**

---

## 2. Binding constitutional guardrails for Wave 4 (pre-registered — automatic FAIL if violated)

Wave 4 shall remain an **Institutional Intelligence** wave whose sole purpose is to strengthen research,
analysis, and operator decision support. It shall **not** introduce execution capability, broker interaction,
order generation, autonomous trading, or any modification to the Constitutional Governance Gate. The platform
shall remain **strictly advisory, research-first, and operator-controlled.**

The following constraints carry forward automatically and are binding on every Wave-4 subsystem:

- **GR-1 — The Constitutional Governance Gate remains CLOSED** (05 v2.0 §15). No Wave-4 unit may open, weaken,
  or add a code path toward opening it.
- **GR-2 — All outputs are advisory/research-oriented only.** No signal, analytic, correlation, regime,
  portfolio/risk metric, or scenario result may be framed, styled, or wired as an instruction, a guarantee, or
  an automated action. R-3 (advisory-not-instruction / no-execution-controls on any UI) applies to every new
  surface.
- **GR-3 — No execution pathways, order payloads, broker integration, or execution APIs** may be introduced
  anywhere (05 v2.0 §16 broker logic isolated & closed). Proven wave-wide by the standing execution/mutation
  grep every unit.
- **GR-4 — All new intelligence must remain explainable, auditable, reproducible, and fully traceable**
  (05 v2.0 §15 "every recommendation shall remain explainable"; 07_ML_SPEC lineage/experiment governance).
  Every derived metric carries its lineage/inputs; every persisted artifact carries an immutable audit event.
- **GR-5 — Existing governance, evidence, persistence, and audit requirements remain mandatory** — Level-IV
  report-claims never approve; operator-run target evidence (Windows/PowerShell + PostgreSQL) is required; a
  failing test is a finding; a blank grep is a non-result.
- **GR-6 — Standing engineering controls remain in force for every new subsystem:**
  - **Wheel-compat spike (TD-065)** — the FIRST Wave-4 unit adopting a compiled ML/scientific dependency
    (numpy/scipy/scikit-learn/statsmodels/pandas-with-C-extensions, etc.) MUST perform and evidence an
    install/import/smoke spike on Windows + Python 3.14.6 before relying on it. **Wave 4 is the likely trigger**
    (correlation engine, regime detection, portfolio/risk analytics).
  - **Persistence-capture control** — any unit persisting a NEW report/artifact type must show a
    committing-script + raw `psql SELECT ≥1 row` on the CORRECT table in its FIRST submission.
  - **R-3 no-execution-controls** on every new UI (grep + test + browser screenshot).
- **GR-7 — Statistical & economic honesty (07_ML_SPEC)** — any new analytic that estimates a quantity must
  report **uncertainty, not only point estimates**; statistical significance ≠ economic usefulness (report
  independently); no cherry-picking / misleading aggregation; correlation/regime claims get leakage,
  look-ahead, and base-rate sanity checks. Market-agnostic discipline (D-W2-001 **Option A**) stands — no
  amendment unless a GOVERNANCE_AMENDMENTS amendment is first approved.
- **GR-8 — Presentation-only UX** (05 v2.0 §30/§11.1) — dashboards/annotations/simulations **display**
  persisted, governed artifacts; they do not authoritatively recompute inference/analytics client-side.

---

## 3. What the Design Plan must contain

Within the boundaries of §2, the DA shall prepare a **comprehensive Wave-4 Design Plan** that identifies:

1. **Bounded contexts & architectural decomposition** — where each capability lives under the canonical
   `05_SYSTEM_ARCHITECTURE` v2.0 ownership (single ownership, §13); which context owns correlation, regime,
   macro, sector, portfolio, risk, scenario-simulation, chart-annotation, cross-market intelligence, and
   professional signal validation.
2. **Implementation sequence & unit breakdown (W4-U01…U0n)** — smallest-safe-slice first (the W3-U01
   precedent: prove the safety controls before the feature); which unit triggers the **wheel-compat spike**.
3. **Dependencies** — internal (which Wave-2/3 artifacts each capability reads) and external (any new compiled
   ML/scientific libraries — flag them for the spike; **no external live-data provider/broker connection**).
4. **Data & persistence design** — new artifact/report types (each subject to the persistence-capture
   control), schemas/migrations, and lineage/audit for each.
5. **Statistical/economic methodology** — for correlation/regime/portfolio/risk/scenario: the estimators,
   uncertainty treatment, look-ahead/leakage guards, validation approach (walk-forward/OOS/CV where relevant),
   and how results are reported as research (not guarantees).
6. **UX surfaces** — presentation-only design for any new dashboards/annotations/simulation views; R-3
   compliance; how uncertainty and advisory framing are shown.
7. **Risks & governance implications** — mapped to a planned RISK_REGISTER set, each with a mitigation and the
   negative test/structural proof that will demonstrate it (e.g. "scenario simulation is hypothetical, not a
   trade instruction — prove by grep + test + screenshot").
8. **Bright-line self-check** — an explicit table showing how each capability honors GR-1…GR-8 and why nothing
   in Wave 4 approaches execution or the Gate.
9. **Recommended W4-U01 scope** — the single smallest unit that proves the wave's core safety controls first.

---

## 4. Process

1. **Wave-3 residual hardening (W3-U08.1) approved** → Wave 3 is residual-free.
2. **DA delivers the Wave-4 Design Plan** (this request).
3. **ITRGA independently reviews** the plan for constitutional compliance (GR-1…GR-8) and engineering soundness,
   issues `ITRGA_REVIEW_WAVE4_DESIGN_PLAN.md` with any refinements (accept / accept-with-refinements /
   request-changes). **No Wave-4 Build Order is issued until the plan is accepted.**
4. On acceptance → ITRGA issues `BUILD_ORDER_W4-U01.md` (smallest safe slice) on operator authorization.

---

## 5. Note

These guardrails are pre-registered so the DA designs **within** the constitutional envelope from the outset,
and so ITRGA's later review measures the plan against a standard fixed **before** the design existed — not one
retrofitted afterward. Design freely inside the boundaries; the boundaries do not move without a governed
amendment.

> **We don't guess. We prove.** — ITRGA
