# AXIOM — Frontend Roadmap (v2 · Operator-Reconciled)
## Targeted UI additions on the retained terminal architecture

| Item | Value |
|------|-------|
| Document class | **ITRGA sequencing recommendation** — revision 2, reconciled against Operator Review (2026-08-19) |
| Status | **DRAFT — not an Operator directive, not a DA engineering design plan, not a Build Order, not self-authorization** |
| Date | 2026-08-19 |
| Baseline | frontend React 18.3 + Vite 8 + TypeScript (typecheck passes) · unified terminal shell, docks, stage views |

> **Binding design constraint (retained from v1):** the shell, workspace registry, docking model, design-token system, RBAC route-gating, and non-actuation posture are **kept**. This is additive work — no remodel, no new navigation paradigm, no actuation, no external-LLM/assistant-actor drift.

---

## 0. Authority boundary (Operator §23 — reconciled)

Same reconciliation as the Backend roadmap: this is a sequencing recommendation only. It is **not** the DA's engineering design plan, not an Operator directive, and not a Build Order. The DA produces per-unit design plans; Build Orders are issued through the governed lifecycle. ITRGA recommends sequencing without authoring, designing, or implementing.

Repository/custody (§24) and programme-wide data honesty (§22, §0.2 of the Backend roadmap) apply equally here: no implied unlimited repo access, and every data-driven output labels its source (synthetic / simulated / historical real / live / stale / unavailable).

---

## 0.1 Guiding principles

1. **The shell is a keeper.** Build *inside* it.
2. **UI waits for data, not the reverse.** No fake/mock data shipped to "complete" a view.
3. **Presentation-only.** Read-only or research-note writes; no execution/order/account controls.
4. **Reuse** the design system and accessibility infrastructure.
5. **Evidence per unit** — screenshots, contrast checks, keyboard/focus walkthroughs, measured latency.

---

## Dependency map (aligned to the programme-wide model)

```
                        BASELINE
                           │
              ┌────────────┴─────────────┐
              │                          │
           BACKEND                    FRONTEND
              │                          │
             B-00                      F-00
              │                          │
             B-01                      F-01 ──(scaffold parallel; final acceptance needs B-06.1)
              │                          │
             B-02                        │
              │                          │
             B-03 ───────────────────► F-02
              │
             B-04 ───────────────────► F-03
              │
             B-05 ───────────────────► F-04
              │
         B-02..B-05 ────────────────► F-05
              │                          │
              └────────────┬─────────────┘
                           ▼
                    B-07 + F-06
                           │
                           ▼
                X-01 END-TO-END VERIFICATION
```

---

## Phase F-00 — Hygiene & visual baseline

- **F-00.1** Favicon wiring (Doc 16 §XI — currently 404).
- **F-00.2** Add the missing `<h1>` on the operations landing surface (OBS-2).
- **F-00.3** React Router future-flag strategy *(reconciled: explicit decision, Operator §12)*. The Build Order must choose **one** explicit outcome:
  - **Option A** — enable the v7 future behavior now (opt in to `v7_startTransition` / `v7_relativeSplatPath`), or
  - **Option B** — remain on current behavior and record the v7 upgrade as **explicit technical debt** in the debt register.
  - The DA may not pick whichever is easiest; the governing decision must be stated.
- **F-00.4** Frontend dependency remediation — **owned by F-00** (Operator §11.1). Same severity/exception acceptance model as B-00.2: no unaccepted critical/high findings; remaining findings classified; exceptions documented; lockfiles updated; gate passed. B-00 references this as a shared baseline dependency.
- **F-00.5** Committed visual QA baseline: reference screenshots per workspace, contrast assertions, reduced-motion check — the measurable anchor for "professional," replacing subjective judgment.

**Acceptance:** all items closed with SHA evidence; baseline screenshots committed.

---

## Phase F-01 — Assistant input surface *(reconciled: dependency correction)*

**Dependency correction (Operator §13):** F-01 may **begin in parallel** with the backend; but its **final acceptance requires B-06.1** (`POST /api/v1/collaboration/assistant-respond`). F-01 is therefore *not* fully independent of backend data — it is backend-*gated* at acceptance, not at start.

- **F-01.1** Accessible question input + submit, wired to `POST .../assistant-respond` (B-06.1).
- **F-01.2** Response rendering: grounded summary, source-artifact lineage, `RESEARCH-ONLY · NON-ACTUATING` disclaimer, and classed refusal rendering with audit reference.
- **F-01.3** Loading/empty/error/401 states; deterministic-local disclosure ("no external LLM; external LLM requires a future gated Build Order").
- **F-01.4** Context chips fed from **real** workspace context (symbol/timeframe/artifact), replacing static suggestions.

**Acceptance (final, gated on B-06.1):** ask → real response or classed refusal, keyboard-accessible, audit-linked; zero actuation; no external network calls.

---

## Phase F-02 — Signal presentation (gated on B-03)

- **F-02.1** Signal list/cards: confidence, direction, guardrail status, staleness, uncertainty — never a bare "BUY/SELL."
- **F-02.2** Signal drill-down → investigation: rationale, guardrails, lineage, linked reports.
- **F-02.3** Withheld-signal visibility (honest display of *why* withheld).

**Acceptance:** renders real signal rows; no fabricated states; drill-down traces lineage.

---

## Phase F-03 — Intelligence presentation (gated on B-04)

- **F-03.1** Correlation report rendering (matrix + sample counts + uncertainty).
- **F-03.2** Regime detection view (classification + confidence + explanation).
- **F-03.3** Scenario comparison table (assumptions, uncertainty, economic-usefulness).
- **F-03.4** Portfolio/risk display (hypothetical framing; no account/broker linkage).

**Acceptance:** server-stored values only (no client recompute); uncertainty and limitations always visible.

---

## Phase F-04 — Alerts center (gated on B-05)

- **F-04.1** Alert list: severity, source lineage, timestamps, read-state ack.
- **F-04.2** Filtering by domain (market / signal / risk / research / system).

**Ack semantics (Operator §16, aligned to B-05):** ack may modify **alert read-state only**; it must not mutate trading, account, broker, model, analytical-source, or execution state.

**Acceptance:** real alerts render; ack changes read-state only.

---

## Phase F-05 — Lineage & evidence visualization *(reconciled: narrowed scope)*

**Scope correction (Operator §17):** replace the over-broad "any displayed number" with:

> **Every domain-derived analytical value presented by the F-05 surfaces must be traceable to its source artifact/data record, provenance, and applicable uncertainty/limitations.**

This excludes presentation-only values (pagination, UI counters, timestamps, layout, system-health, presentation calculations).

- **F-05.1** Artifact lineage tree over **real** artifacts (source → artifact → hash → related report).
- **F-05.2** Provenance/hash display answering: *where did this come from, what supports it, what are the limitations?* (catalogue §17, §37).

**Acceptance:** an operator can trace any domain-derived analytical value to its source artifact and its uncertainty.

---

## Phase F-06 — Accessibility, performance & final polish *(reconciled: explicit thresholds)*

**Performance criteria (Operator §18):** define and meet **quantitative** thresholds before execution, for at least:

| Interaction | Target (to be finalized in the Build Order) |
|-------------|---------------------------------------------|
| Command-palette response | ≤ 100 ms |
| Workspace switching | ≤ 300 ms |
| Instrument selection | ≤ 200 ms |
| Chart first render | ≤ 1 s |
| Live-update propagation | ≤ 500 ms |

(Exact numbers are the DA's to propose and the Operator/ITRGA's to approve — the requirement is that they be **measurable and stated**, not left as "responsive.")

- **F-06.1** Accessibility audit over all new surfaces (keyboard, focus, screen-reader, contrast, reduced-motion).
- **F-06.2** Measure and hit the latency targets with recorded evidence.
- **F-06.3** Final polish within the existing design system (refinement, not redesign).

**Acceptance:** thresholds met with measured numbers; accessibility walkthrough documented; visual baseline compared to F-00.5 and reviewed.

---

## X-01 — End-to-end platform verification (shared with Backend roadmap)

Joint gate, added per Operator §20. Owned jointly; sequenced after B-07 + F-06. See Backend roadmap §X-01 for the full workflow and acceptance question. Neither roadmap "complete" alone proves the platform works.

---

## Sequencing summary

| Order | Units | Gate |
|-------|-------|------|
| 1 | F-00 + F-01 (scaffold) | start now, parallel to backend |
| 2 | F-01 final acceptance | requires B-06.1 |
| 3 | F-02 | after B-03 |
| 4 | F-03 | after B-04 |
| 5 | F-04 | after B-05 |
| 6 | F-05 | after B-02…B-05 artifacts |
| 7 | F-06 | continuous; final after F-02…F-05 |
| 8 | X-01 | joint, after B-07 + F-06 |
