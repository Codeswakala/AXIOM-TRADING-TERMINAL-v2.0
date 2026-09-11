# AXIOM — BUILD ORDER F-05
## Lineage & Evidence Visualization (traceability across the terminal)

| Item | Value |
|------|-------|
| Build Order ID | `BO-F-05` |
| Programme | Frontend Operationalization (Visual Blueprint approved) |
| Authorizing authority | **Operator** (directive 2026-08-21: "authorized") |
| Predecessors | F-04 CLOSED · Reconciliation Determination §17/§37 ("where did this come from") · B-00 provenance protocol |
| Governing documents | `VISUAL_BLUEPRINT.md` · Reconciliation Determination §17 (lineage scope) · `07_ML_SPEC.md` §artifact provenance |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and framing

The Reconciliation Determination (§17) established the traceability requirement:

> *Every domain-derived analytical value presented by the F-05 surfaces must be traceable to its source artifact/data record, provenance, and applicable uncertainty/limitations.*

The infrastructure already exists but is **not wired into the terminal**:
- `ArtifactLineageTree` (UI-008-P04) renders a visual lineage chain (market_input → feature_set → model → report → advisory_signal → assistant_explanation), read-only — but is **only used in the assistant's `ResearchReportSummarizer`**.
- The intelligence reports, advisory signals, and alerts already carry `source_artifact_ids`, `report_hash`, and `audit_correlation_id` — but the terminal surfaces (intelligence cards, signal stream, alerts panel, chart) do **not** surface them as a traceable lineage.

This order wires lineage/evidence into the terminal surfaces so an operator can answer "where did this come from, what supports it, and what are its limitations?" — the product-level §37 question.

---

## 1. Objective

1. Surface **lineage** (source artifact ids, report hash, audit correlation) on the intelligence cards, advisory signals, and alerts.
2. Provide a **lineage/evidence view** (reusing `ArtifactLineageTree` where suitable) for domain-derived values.
3. Preserve the read-only, non-actuating, no-fabrication discipline.

---

## 2. Scope

### F-05.1 — Lineage surfacing on terminal surfaces
- **Intelligence cards:** each report already renders a `data-class` label and report-hash prefix (F-03); add the `audit_correlation_id` and `source_artifact_ids` where present, so the lineage is visible.
- **Advisory signals:** surface the `audit_correlation_id`, `inference_input_hash`, and the model/report lineage ids (`model_artifact_id`, `statistical_report_id`, etc.) the read model already carries.
- **Alerts:** surface the `lineage.source` and `audit_correlation_id` (partly done in F-04; complete it consistently).
- **Chart / structural events:** the structural provenance line already exists (F-02); ensure the chart's indicator-series provenance (series kind, as-of) is similarly visible where relevant.

### F-05.2 — Lineage/evidence view
- A read-only lineage affordance (expandable "Lineage" / "Evidence" panel) that renders `ArtifactLineageTree` (or an equivalent) for a selected artifact: source → artifact → hash → related reports → (assistant explanation where present).
- The view answers, per §37: *what the system indicates, why, how certain, what supports it, what restrictions apply* — by surfacing the already-persisted fields, never by inventing them.

### F-05.3 — Scope discipline (binding, from Reconciliation §17)
- Lineage is surfaced for **domain-derived analytical values** only — intelligence metrics, signal fields, alert provenance, structural events. Presentation-only values (pagination, UI counters, timestamps, layout, system-health) are **not** required to carry lineage, and must not be over-labeled.
- Read-only: no mutation, no actuation.

### F-05.4 — Honesty
- When a lineage field is absent, render an honest "provenance not recorded" rather than a fabricated chain. No invented relationships.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** backend change (pure consumer of already-persisted lineage fields).
- **No** fabrication of lineage/provenance relationships — only persisted fields are rendered.
- **No** mutation/actuation; read-only lineage.
- **No** over-labeling of presentation-only values (§5.3).
- **No** weakening of accessibility, themes, or the design language (F-00).
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. Lineage surfacing on intelligence cards, signals, and alerts (audit correlation, source ids, hashes).
2. A read-only lineage/evidence view reusing `ArtifactLineageTree` for domain-derived values.
3. Tests (new/churn): lineage fields rendered where present, honest "not recorded" where absent, read-only (no mutation), scope discipline (no over-labeling).
4. Delivery Report (§9) with relay-accurate manifest + register-in-patch rows.

---

## 5. Dependencies

- **Upstream:** F-02/F-03/F-04 (the surfaces to wire into) · `ArtifactLineageTree` (existing) · B-00 provenance protocol.
- **Downstream:** F-06 (a11y/perf polish), X-01 Terminal Tier.

---

## 6. Allowed files / components

- `frontend/src/components/terminal/TerminalIntelligenceCards.tsx`, `TerminalSignalStream.tsx`, `StructuralSignalStream.tsx`, and the alerts panel (lineage surfacing).
- `frontend/src/workstation/ai/ArtifactLineageTree.tsx` (reuse; extend only if strictly needed).
- `frontend/src/test/**` + relevant `*.test.tsx` (new/churn).
- `docs/governance/TECHNICAL_DEBT_REGISTER.md` (register-in-patch — **required**).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- Read-only lineage; no mutation, no actuation, no fabricated relationships.
- Only persisted fields rendered; "provenance not recorded" where absent.
- Accessibility and theme conformance preserved.

---

## 8. Acceptance criteria

- [ ] Intelligence reports, signals, and alerts each surface their lineage fields (audit correlation, source ids, hash) where present (test-pinned).
- [ ] A read-only lineage/evidence view renders for a selected domain-derived value (test-pinned).
- [ ] Absent lineage renders as honest "provenance not recorded" (test-pinned).
- [ ] No mutation/actuation (read-only, test-pinned).
- [ ] Scope discipline: presentation-only values are not over-labeled (test-pinned).
- [ ] Register rows ship in the patch (register-in-patch).
- [ ] Full frontend suite green (`npm test`) + typecheck green (`tsc -b`); executed output supplied.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1 + register-in-patch)

**Binding:** CA-TRANSMIT-1 (relay-accurate manifest) + register-in-patch.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed frontend test output + typecheck | Level II | run transcript |
| Screenshot captures (lineage on a report/signal/alert; the lineage view) | Level I | images |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Lineage-surfacing description (per surface, per field)
4. Lineage/evidence view description
5. Scope-discipline + honesty evidence (no over-labeling; "not recorded" where absent)
6. Screenshot evidence
7. Non-actuation/read-only evidence
8. Test evidence (executed)
9. Deviations register
10. Register rows in patch (confirmed) + transmission manifest (relay-accurate)

---

## 11. Rollback / containment

- Frontend-only; revert = revert patch. No backend change, no schema change, no new dependency.

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified, the Delivery Report submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of F-05, **F-06 (accessibility, performance & navigation legibility)** may be issued — the final frontend unit before X-01 Terminal Tier.

---

**End of Build Order F-05**
