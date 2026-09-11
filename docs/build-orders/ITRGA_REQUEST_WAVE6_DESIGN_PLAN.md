# ITRGA REQUEST FOR WAVE 6 ENGINEERING DESIGN PLAN — "EXECUTION RESEARCH"

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Document type:** Pre-wave Design Plan Request + Pre-registered Guardrails
**Date:** 2026-07-17
**Platform of record:** v0.46.0 · Alembic head `20260717_0027` · backend **291 passed** · frontend **17 files / 53 tests**
**Governing anchors:** `04_PROJECT_ROADMAP.md` (Wave 6 — Execution Research); `05_SYSTEM_ARCHITECTURE.md` v2.0 §15/§16/§43/§45/§46/§48; `07_ML_SPEC.md`; `08_UI_UX_SPEC.md`; `10_CONSTITUTIONAL_HIERARCHY.md`; D-W2-001 (LOCKED).
**Motto:** *We don't guess. We prove.*

---

## 0. Status & Instruction

Wave 5 is **CLOSED** ("Human-AI Collaborative Workspace Complete," v0.46.0). The Operator has **authorized the opening of Wave 6 — Execution Research.**

Per the established, non-negotiable wave-opening pattern (Waves 2/3/4/5 each opened with pre-registered guardrails + an ITRGA-requested Engineering Design Plan reviewed **before** any unit Build Order), **no W6 unit Build Order will be issued until the DA delivers a Wave 6 Engineering Design & Implementation Plan and the ITRGA has reviewed and accepted it** (accept-with-refinements pattern).

**Wave 6 is THE highest-risk wave in the entire roadmap.** Execution is the constitutional red line, and the **Constitutional Governance Gate is Wave 6's central subject.** The guardrails below are deliberately stricter than any prior wave. The DA shall treat every one as a first-class acceptance criterion, not an aspiration.

---

## 1. The Constitutional Red Line (verbatim anchors the DA must design around)

The ITRGA has re-verified the following in the canonical documents this turn:

- **Approved operational flow is the ONLY approved flow** (`05_SYSTEM_ARCHITECTURE.md` §43):
  `Professional Recommendation → Operator Decision → (Constitutional Governance Gate) → Future Broker Execution` — and **"Every recommendation shall remain explainable."** The Gate sits **between** the operator and any execution. It is **CLOSED.**
- **§15 flow (system-level):** `… → User Experience System → Operator → (Constitutional Governance Gate) → Future Broker Integration (Roadmap Controlled)`. "Future architectural extensions shall preserve this flow unless amended through governance."
- **§16 Dependency Rule (hard):** *"Broker-specific logic shall never appear outside the External Integration System."* The current null/hard-closed broker and `test_broker_integration.py::test_governance_gate_refuses_connect_and_execute` are the standing proof that the Gate refuses `connect`/`place_order`.
- **§46 Human-in-the-Loop:** *"The Operator shall retain final decision authority. Future automation shall require constitutional approval through the Roadmap and Governance Framework."*
- **Roadmap Wave 6 Note (verbatim):** *"No live automated execution shall be authorized unless future governance explicitly approves it."*

**Consequence for Wave 6:** "Execution Research" means **simulation only** — an *environment for researching execution workflows* that **never** connects to a live broker, never places a real order, never touches a real account/position/balance, and never opens the Governance Gate. Wave 6 must make the Gate's closure **more provable**, not less.

---

## 2. Roadmap-named Wave 6 components (and how each is fenced)

The roadmap names: *Execution simulator · Risk engine · Broker abstraction · Paper trading · Execution analytics · Position management research · Trade replay · Performance comparison · Execution experimentation.* Milestone: **"Execution Research Environment Complete."**

Several of these names sit **directly against the red line.** The DA's Design Plan must, for each component it proposes to build in Wave 6, state explicitly which side of the line it is on and how it is fenced:

| Roadmap component | Permitted Wave-6 interpretation (RESEARCH/SIM-ONLY) | Hard prohibition |
|---|---|---|
| **Execution simulator** | Deterministic in-process simulation of fills against historical/replayed data; produces *simulated* fills labelled as such. | No live order routing; no external venue call; no network to any broker/exchange. |
| **Risk engine** | Advisory pre-trade risk *analytics* on hypothetical/simulated orders (research output). | No position sizing that actuates; no account-linked limits; no capital/margin state. |
| **Broker abstraction** | An *interface/adapter shape* whose only Wave-6 implementation is a **NullBroker / SimulatedBroker** that REFUSES connect/execute while the Gate is CLOSED — must live in the External Integration System (§16). | No concrete live-broker adapter; no credentials; no real endpoint; no code path that can execute if a key were supplied. |
| **Paper trading** | A clearly-labelled **simulation ledger** of hypothetical trades on simulated fills; research artifact only. | Must NOT be presentable as, or convertible into, live trading; no "go live" toggle. |
| **Execution analytics / Performance comparison** | Post-hoc analytics over *simulated* executions (slippage-model, fill-quality, strategy comparison) with mandatory uncertainty. | No claim of real P&L; stat-significance ≠ economic success (07_ML_SPEC); no cherry-picking. |
| **Position management research / Trade replay / Execution experimentation** | Read-only/simulated research over replayed history; pre-registered experiments. | No mutation of real state; no live position; no actuation. |

The DA is **not** obligated to build every named component in Wave 6, and **should not** over-scope. Propose the smallest coherent, safely-fenced set and sequence it.

---

## 3. PRE-REGISTERED WAVE 6 GUARDRAILS (binding acceptance criteria)

These are pre-registered so a later "we didn't know" cannot be a defense. Every W6 unit will be judged against ALL applicable items.

**Constitutional / execution-safety (EXTRA-STRICT, Wave-6-specific):**
- **GR6-1 — Gate stays CLOSED.** The Constitutional Governance Gate remains CLOSED for the entirety of Wave 6. No unit may open it. Any change to Gate state requires an explicit **GOVERNANCE_AMENDMENTS amendment + Operator authorization + ITRGA governance decision** — a three-party act, never a code change inside a feature unit.
- **GR6-2 — Simulation/research only.** No live broker connection, no real order placement, no real account/position/balance/margin/capital path, no real-money path — **by construction**, not by config flag. There must be **no code path** that could execute against a live venue even if a credential/endpoint were supplied. Prove absence (the strongest proof: endpoint/adapter **provably refuses** — e.g. raises/returns refusal + increments the governance-refusal metric; connect/execute proven **absent or 405/refused**).
- **GR6-3 — Broker logic containment (§16).** Any broker-abstraction code lives ONLY in the External Integration System. Grep-provable: no broker-specific logic imported/instantiated in intelligence/signals/UX layers except the audited refusal seam.
- **GR6-4 — Null/Simulated broker refuses.** The only Wave-6 broker implementation refuses connect + execute while the Gate is CLOSED, extending the standing `test_governance_gate_refuses_connect_and_execute` proof to every new seam. Deliver the refusal test + raw run inline.
- **GR6-5 — No execution/actuation controls on the UI (R-3 lineage).** No "buy/sell/submit/go-live/connect-broker" affordance. Every execution-research surface is **research-framed** and labelled **SIMULATED**. Judged in the browser (see GR6-10).
- **GR6-6 — Simulated artifacts are labelled and inert.** Every simulated fill/paper-trade/position record is persisted and rendered with an unambiguous SIMULATED marker and is non-actuating (GR-9/R-6 lineage: no sizing that actuates, no account linkage).

**Method / evidence (standing, carried forward):**
- **GR6-7 — Uncertainty mandatory; stat ≠ economic (07_ML_SPEC).** Any execution-analytics/performance-comparison output carries uncertainty; no cherry-picking; pre-registered experiments; statistical significance is not asserted as economic success.
- **GR6-8 — Option A / D-W2-001 (LOCKED).** Generalized market-agnostic modeling; no symbol-identity feature; any per-market specialization needs a GOVERNANCE_AMENDMENTS amendment.
- **GR6-9 — Persistence-capture control.** Any new persisted artifact/table owes, on FIRST submission: a committing script + raw `psql SELECT ≥1 row` on the CORRECT table + a matching immutable **no-orphan audit JOIN** (`orphan_count 0`), delivered INLINE. An API read-back does NOT substitute for a named raw SELECT + audit join (W4-U02 C-1).
- **GR6-10 — UI judged in the browser.** Mandatory browser screenshots from a reachable served session; sandbox-only/report-claim shots ⇒ WITHHELD/CONDITIONAL (W3-U05/W0-U06 precedent).
- **GR6-11 — CI via documented Git-Bash path.** `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → `==> Local CI equivalent complete` + inline `LOCAL_CI_EXIT_CODE: 0` (W4-U03 lesson: bare `bash` → WSL failure gives spurious exit 1).
- **GR6-12 — No unspiked dependency.** Any new compiled / LLM / tokenizer / broker-SDK dependency owes its own wheel-compat spike (TD-065 pattern; numpy/pandas/scipy already discharged, nothing else is). A broker SDK is **not** permitted in Wave 6 regardless (GR6-2/GR6-3) — this bars it doubly.
- **GR6-13 — External LLM stays a FUTURE hard-gated separate Build Order** (R5-2). Never inside a Wave-6 feature unit.

---

## 4. What the Design Plan must contain

The DA shall deliver `WAVE6_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` containing:

1. **Scope & non-scope** — which roadmap components are in Wave 6, which are deferred, and why (favor the smallest safe set).
2. **Constitutional fence map** — for each proposed component, the §2 table row: permitted interpretation + the concrete mechanism that makes the prohibition impossible **by construction** (not by flag).
3. **Unit decomposition** — one-unit-per-Build-Order (operator-agreed policy), sequenced. **W6-U01 MUST be the smallest safe slice that PROVES the Gate-stays-closed / simulation-only safety envelope BEFORE any execution-research feature** — the "prove the lock before the door" precedent (W3-U01/W4-U01/W5-U01). Recommend: W6-U01 = the SimulatedBroker/refusal-seam safety foundation + its refusal proofs.
4. **Data model** — any new tables/artifacts, each with its persistence-capture plan (GR6-9), each simulated record's SIMULATED marker and inertness (GR6-6), and Alembic head progression from `20260717_0027`.
5. **Refusal & containment test plan** — the concrete tests proving GR6-1…GR6-6 (Gate closed, connect/execute refused, §16 containment grep, no-actuation).
6. **UI plan** — research-framed, SIMULATED-labelled surfaces; no execution/actuation controls (GR6-5); browser-evidence plan (GR6-10).
7. **Analytics method** — uncertainty, pre-registration, no-cherry-picking, stat≠economic (GR6-7).
8. **Dependency declaration** — explicit statement that NO broker SDK / live-venue client / new compiled dep is introduced (or, if any compiled dep is proposed, its wheel-compat spike plan; a broker SDK is barred outright).
9. **Risk register** — with the falsification method for each risk (not "mitigated"; *proven*).

---

## 5. Process from here

1. **DA → Operator → ITRGA:** deliver `WAVE6_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md`.
2. **ITRGA:** review line-by-line → `ITRGA_REVIEW_WAVE6_DESIGN_PLAN.md` (ACCEPTED-WITH-REFINEMENTS pattern; refinements R6-n pre-registered as binding).
3. **On operator authorization:** `BUILD_ORDER_W6-U01.md` (smallest safe slice — the safety envelope).
4. **Per unit thereafter:** on "authorized" → next `BUILD_ORDER_W6-U0n.md`; on delivery report + `operator results.md` (+ screenshots) → verify → `ITRGA_REVIEW_W6-U0n.md` (or `_FINAL` on closure) → bump onboarding → present.

---

## 6. Reviewer posture reminder (unchanged)

- Never approve on report-claims alone (Level-IV lowest). Operator-run evidence on target is MANDATORY.
- A single CRITICAL or unmet mandatory evidence ⇒ **APPROVAL WITHHELD**. A red gate is a finding, never relabeled green.
- Verify build identity FIRST (unit id + version in the pack) before judging pass/fail — the previous turn's pack has been mis-attached before.
- CONDITIONAL only when every *risk* item is proven and a *named* proof item is missing; superseded by a `_FINAL` on closure.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
