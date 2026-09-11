# AXIOM — BUILD ORDER F-04
## Alerts Center Completion (domain filtering + lineage/timestamp surfacing)

| Item | Value |
|------|-------|
| Build Order ID | `BO-F-04` |
| Programme | Frontend Operationalization (Visual Blueprint approved) |
| Authorizing authority | **Operator** (directive 2026-08-21: "authorized") |
| Predecessors | F-03 CLOSED · B-05 (alert emission — delivered) · SURF-P02 (existing alerts surface) |
| Governing documents | `VISUAL_BLUEPRINT.md` · Reconciliation Determination §11/§16 (ack read-state-only) · `08_UI_UX_SPEC.md` |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and honest framing

The alerts center is **already substantially built** — verified in code: `MonitoringAlertsPanel.tsx` renders `alert_type`, severity, subject lineage, a read-state-only acknowledge with **no optimistic update** (M2), ack-error surfacing, and a detail record; `AlertsProvider.tsx` maintains the list and a genuine unread count (`acknowledged === false`). The `MonitoringAlert` type already carries `created_at`, `subject_type/id`, `market_class`, `model_artifact_id`, `signal_id`, `lineage`, and `acknowledged_*` fields.

This order is therefore a **narrow completion**, not a build. It adds the two items the frontend roadmap (§F-04) still calls for, which the existing surface lacks:

1. **Domain filtering** (market / signal / risk / research / system) — the only current "filter" is the unread count; there is no domain filter.
2. **Timestamp + lineage surfacing completeness** — confirm every alert visibly carries its `created_at` (absolute UTC) and its provenance (subject/lineage), per the ack read-state-only discipline.

---

## 1. Objective

1. Add domain filtering to the alerts surface (market / signal / risk / research / system, derived from the alert's `subject_type`/`market_class`/`signal_id`/`model_artifact_id` fields — data-origin-derived, never invented).
2. Ensure every alert card visibly surfaces its timestamp and lineage/provenance.
3. Preserve the read-state-only ack discipline and the honest empty/error states.

---

## 2. Scope

### F-04.1 — Domain filtering
- A filter control (tabs or a dropdown) with the five domains: **market, signal, risk, research, system**.
- Domain assignment is **data-origin-derived** from the alert's persisted fields (`subject_type`, `market_class`, `signal_id`, `model_artifact_id`), not a client-invented category. A documented mapping; unknown/mixed falls to a neutral bucket, never fabricated.
- Filtering is client-side over the fetched list (no backend change — the read API already returns the full list).

### F-04.2 — Timestamp + lineage surfacing
- Every alert card renders its **absolute UTC `created_at`** (not a relative "2h ago" that hides the timestamp), and its **provenance** (subject type/id, and the `lineage.source` where present).
- The detail record continues to surface the full field set.

### F-04.3 — Ack discipline (preserved, binding)
- Acknowledge remains **read-state-only**: it flips `acknowledged` after the API confirms (no optimistic update), and the underlying subject state is never touched. The existing M2 behavior is preserved and test-pinned.

### F-04.4 — Honesty
- Honest empty state ("no alerts"), honest error/ack-error states, no fabricated alerts. Loading uses the existing skeleton.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** backend change (pure consumer of `GET /alerts` + `POST /alerts/{id}/ack`).
- **No** alert generation/emission from the frontend (emission is B-05's backend responsibility).
- **No** auto-action/remediation on ack — ack is read-state only.
- **No** actuation controls; **no** collapsing alerts into other surfaces.
- **No** weakening of accessibility, themes, or the design language (F-00).
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. Domain filter control (5 domains, data-origin-derived).
2. Timestamp + lineage surfacing on every alert card + detail record.
3. Tests (new/churn): domain mapping, filter behavior, timestamp render, lineage render, ack read-state-only (no optimistic update), honest empty/error states.
4. Delivery Report (§9) with relay-accurate manifest + register-in-patch rows.

---

## 5. Dependencies

- **Upstream:** B-05 (emission + read/ack APIs) · SURF-P02 (existing panel/provider) · F-03 (design language).
- **Downstream:** F-05 (lineage), X-01 Terminal Tier.

---

## 6. Allowed files / components

- `frontend/src/components/alerts/MonitoringAlertsPanel.tsx` (+ its stylesheet if needed).
- `frontend/src/components/alerts/AlertsProvider.tsx` (only if the filter state lives there).
- `frontend/src/test/**` + relevant `*.test.tsx` (new/churn).
- `docs/governance/TECHNICAL_DEBT_REGISTER.md` (register-in-patch — **required**).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- Ack remains read-state-only; no optimistic update; no actuation.
- Domain assignment is derived from persisted fields, never invented; no fabricated alerts.
- Accessibility and theme conformance preserved.

---

## 8. Acceptance criteria

- [ ] Five-domain filter present and functional (test-pinned mapping + filtering).
- [ ] Domain assignment is data-origin-derived (no invented categories — test-pinned).
- [ ] Every alert card renders absolute UTC timestamp + provenance/lineage (test-pinned).
- [ ] Ack read-state-only preserved (no optimistic update — test-pinned).
- [ ] Honest empty/error states (test-pinned).
- [ ] Register rows ship in the patch (register-in-patch).
- [ ] Full frontend suite green (`npm test`) + typecheck green (`tsc -b`); executed output supplied.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1 + register-in-patch)

**Binding:** CA-TRANSMIT-1 (relay-accurate manifest) + register-in-patch.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed frontend test output + typecheck | Level II | run transcript |
| Screenshot captures (domain filter, timestamped alert card, ack state) | Level I | images |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Domain-filter mapping (data-origin derivation)
4. Timestamp + lineage surfacing description
5. Ack read-state-only preservation evidence
6. Screenshot evidence
7. Test evidence (executed)
8. Deviations register
9. Register rows in patch (confirmed) + transmission manifest (relay-accurate)

---

## 11. Rollback / containment

- Frontend-only; revert = revert patch. No backend change, no schema change, no new dependency.

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified, the Delivery Report submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of F-04, **F-05 (lineage & evidence visualization)** may be issued.

---

**End of Build Order F-04**
