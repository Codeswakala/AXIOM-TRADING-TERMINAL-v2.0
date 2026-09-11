# ITRGA REQUEST — WAVE 5 CONSTITUTIONAL GUARDRAILS + DESIGN PLAN

| Field | Value |
|---|---|
| Issuing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Wave | **5 — Human-AI Collaboration** |
| Roadmap objective (Tier-3 `04_PROJECT_ROADMAP`) | "Create an interactive AI-assisted trading environment." Milestone: **Human-AI Collaborative Workspace Complete** |
| Status | **GUARDRAILS PRE-REGISTERED (binding) · DESIGN PLAN REQUESTED** |
| Date | 2026-07-16 |
| Precedent | Waves 2/3/4 each opened with an ITRGA-requested Design Plan reviewed/accepted before any unit Build Order |
| Preconditions | Wave 3 ("Professional Advisor Platform Complete", v0.30.0) + Wave 4 ("Institutional Intelligence Layer Complete", v0.38.0) both closed; Gate CLOSED |

> **We don't guess. We prove.** This is the highest-risk wave yet — an interactive assistant and a "trade planning workspace" edge toward instruction and autonomy. Design within the boundaries; ITRGA reviews the design before anything is built.

---

## 1. Purpose & separation of responsibilities

Wave 5 builds an **interactive, AI-assisted, collaborative research workspace** (chart assistant, drawing
tools, AI annotations, scenario comparison, **trade planning workspace**, signal investigation, **manual trade
journal**, decision explanations, interactive research assistant). Its output is **operator decision support —
it does not, and must not, act, instruct, or execute.** Per the established separation: **the Development
Authority designs the implementation; the ITRGA determines whether the proposed design remains constitutionally
compliant.** ITRGA first **pre-registers the binding guardrails below**, then **requests a comprehensive Wave-5
Design Plan**, which ITRGA will independently review **before any Wave-5 Build Order is issued.**

**Why Wave 5 is treated as the riskiest wave to date:** it introduces two new hazard classes the prior waves
did not have —
1. **An interactive AI/LLM assistant** (a generative surface: prompt injection, data exfiltration,
   hallucinated "advice"/instructions, unbounded tool access); and
2. **A "trade planning workspace" + "trade journal"** (surfaces whose names border on instruction/execution and
   real positions).
The guardrails below are written to hold the advisory/research-first, Gate-CLOSED line against both.

---

## 2. Binding constitutional guardrails for Wave 5 (pre-registered — automatic FAIL if violated)

Wave 5 shall remain a **research/decision-support** wave. It shall **not** introduce execution capability,
broker interaction, order generation, position sizing, autonomous action, account/position linkage, or any
modification to the Constitutional Governance Gate. The platform shall remain **strictly advisory,
research-first, and operator-controlled.**

Carried forward and binding on every Wave-5 subsystem:

- **GR-1 — The Constitutional Governance Gate remains CLOSED** (05 v2.0 §15). No Wave-5 unit may open, weaken,
  or add a code path toward opening it.
- **GR-2 — All outputs are advisory/research/decision-support only.** No assistant reply, annotation, plan,
  journal entry, scenario comparison, or explanation may be framed, styled, or wired as an instruction, an
  order, a guarantee, or an automated action. R-3 (advisory-not-instruction / no execution controls) applies
  to every new surface.
- **GR-3 — No execution / order / sizing / broker / account / position-linkage path** anywhere (05 v2.0 §16
  broker logic isolated & closed). Proven wave-wide by the standing execution/mutation grep every unit,
  extended for Wave 5 to include planning/journal action verbs.
- **GR-4 — Everything explainable, auditable, reproducible, traceable** (05 v2.0 §15; 07_ML_SPEC lineage). Any
  AI-generated content (annotation, explanation, assistant reply) carries provenance/lineage and is auditable;
  "decision explanations" explain **persisted, governed** research, not fabricated rationale.
- **GR-5 — Existing governance, evidence, persistence, audit requirements remain mandatory** — Level-IV
  report-claims never approve; operator-run target evidence (Windows/PowerShell + PostgreSQL) required; a
  failing test is a finding; a blank grep is a non-result; UI is judged in the browser.
- **GR-6 — Standing engineering controls remain in force:** wheel-compat spike for any NEW compiled dependency
  (numpy/pandas/scipy already discharged; anything else — incl. any ML/LLM/tokenizer lib — owes its own spike);
  persistence-capture control (committing script + raw `psql SELECT ≥1 row` on the correct table + no-orphan
  audit) for any new persisted artifact; R-3 on every new UI (grep + test + browser screenshot).
- **GR-7 — Statistical/economic honesty + no fabricated certainty.** Any quantitative surface carries
  uncertainty; statistical ≠ economic; no cherry-picking; no guaranteed/expected returns. Applies to scenario
  comparison and any assistant-surfaced metric. Market-agnostic discipline (D-W2-001 Option A) stands.
- **GR-8 — Presentation-only UX** (05 v2.0 §30/§11.1) — workspaces/assistants **display/compose over**
  persisted, governed artifacts and read-only APIs; they do not authoritatively recompute inference/analytics
  client-side.

### Wave-5-specific guardrails (new hazard classes — pre-registered)

- **GR-9 — The "trade planning workspace" and "trade journal" are RESEARCH ONLY.** A plan/journal entry is a
  **hypothetical, operator-authored research note** — it **carries no order/sizing/quantity/stop/target/
  broker/account/position payload**, is **inert** (persisting or viewing it triggers/executes nothing), and is
  never emitted to or read by any execution path. Prove structurally (inert schema + named test) + grep — the
  W4-U04/U05 keystone standard, extended.
- **GR-10 — The interactive AI/LLM assistant is bounded, grounded, and non-actuating.** It **(a)** has **no
  tools/actions that mutate state, place orders, open the Gate, or write outside its own audited
  research-note/annotation store**; **(b)** is **grounded in persisted, governed AXIOM artifacts** (it explains/
  surfaces existing research; it does not invent signals/prices/outcomes) with provenance shown; **(c)** carries
  an **explicit "AI-generated, research-only, not financial advice / not an instruction, may be wrong —
  operator judgment required" disclaimer** on every AI output; **(d)** is **resistant to prompt-injection /
  instruction-escalation** — no user/assistant text can cause an action, a Gate change, or an unaudited write.
  Prove by named tests (assistant cannot act / cannot be injected into acting) + grep + browser.
- **GR-11 — No secrets/PII/model-internals leakage via the assistant** (05 v2.0 §77). The assistant/workspace
  must not surface secrets, tokens, raw model scores, or un-governed internals; sampled-output check required.

---

## 3. What the Design Plan must contain

Within the boundaries of §2, the DA shall prepare a **comprehensive Wave-5 Design Plan** identifying:

1. **Bounded contexts & architectural decomposition** under canonical `05_SYSTEM_ARCHITECTURE` v2.0 single
   ownership (§13) — where the chart assistant, drawing tools, AI annotations, scenario comparison, **trade
   planning workspace**, signal investigation, **trade journal**, decision explanations, and interactive
   research assistant each live; and explicitly **which context owns the AI/LLM assistant boundary** (it owns
   no feeds/order flow/broker/auth/Gate).
2. **The AI/LLM assistant architecture (GR-10) in detail** — model/provider choice (and its **wheel-compat/
   dependency spike** if compiled/new; note any external API and how §77 secrets are handled), **grounding
   strategy** (which persisted artifacts it may read), **its tool/action allowlist (must be non-actuating and
   confined to an audited research-note store)**, **prompt-injection defenses**, provenance/audit of AI output,
   and the mandatory disclaimer.
3. **The trade planning workspace + journal data model (GR-9)** — schemas that are **inert** (no order/sizing/
   account columns), persistence-capture + audit plan, and how they are structurally prevented from reaching
   any execution path.
4. **Implementation sequence & unit breakdown (W5-U01…U0n)** — smallest-safe-slice first (the W3-U01/W4-U01
   precedent: prove the safety controls before the feature); which unit is the AI-assistant safety foundation
   (recommend it early, before rich interactive features).
5. **Dependencies** — internal (which Wave-2/3/4 artifacts each feature reads) and external (any new
   compiled/LLM/tokenizer lib → flag for spike; **no external live-data provider/broker connection**; any LLM
   API keyed via §77-compliant secret handling).
6. **UX surfaces** — presentation-only design for each new surface; R-3 compliance; how AI-generated content is
   labelled, how uncertainty/provenance is shown, and that **no surface has execution/order/sizing controls.**
7. **Risks & governance implications** — mapped to a planned RISK_REGISTER set, each with a mitigation + the
   negative test/structural proof (e.g. "assistant cannot be prompt-injected into acting — prove by named
   test"; "trade plan carries no order payload — grep + inert schema + test").
8. **Bright-line self-check** — a table showing how each capability honors GR-1…GR-11 and why nothing in
   Wave 5 approaches execution, the Gate, or autonomous action.
9. **Recommended W5-U01 scope** — the single smallest unit that proves the wave's core safety controls first
   (recommend: the AI-assistant safety/grounding/non-actuation foundation + inert planning/journal contract).

---

## 4. Process

1. **DA delivers the Wave-5 Design Plan** (this request).
2. **ITRGA independently reviews** for constitutional compliance (GR-1…GR-11) + engineering soundness →
   `ITRGA_REVIEW_WAVE5_DESIGN_PLAN.md` with refinements (accept / accept-with-refinements / request-changes).
   **No Wave-5 Build Order issues until the plan is accepted.**
3. On acceptance → ITRGA issues `BUILD_ORDER_W5-U01.md` (smallest safe slice) on operator authorization.

---

## 5. Note

These guardrails are pre-registered so the DA designs **within** the constitutional envelope from the outset —
and so ITRGA's later review measures the plan against a standard fixed **before** the design existed. Wave 5's
generative/interactive nature makes the non-actuation, grounding, and anti-injection controls (GR-9/GR-10/GR-11)
as important as the long-standing no-execution line. Design freely inside the boundaries; the boundaries do not
move without a governed amendment. Execution remains roadmap-gated to **Wave 6**.

> **We don't guess. We prove.** — ITRGA
