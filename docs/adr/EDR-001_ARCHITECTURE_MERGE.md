# Engineering Decision Record — EDR-001

| Field | Value |
|-------|--------|
| ID | EDR-001 |
| Title | Merge dual System Architecture documents into single canonical architecture |
| Date | 2026-07-10 |
| Status | Accepted |
| Authority | Operator directive; executed by Development Authority |
| Domain | System Architecture / Governance |

---

## Context

The project corpus contained two active architecture documents:

- `05_SYSTEM_ARCHITECTURE.md` — logical layers and eight capability subsystems
- `06_SYSTEM_ARCHITECTURE.md` — technology stack, seven major systems, events, database detail

Both claimed governing authority (Project Readiness Report contradiction **C-01** / **C-02**).

## Problem

Dual architecture sources risk divergent implementation, ambiguous review criteria, and citation conflicts for ITRGA.

## Options Considered

1. Designate 05 only as canonical  
2. Designate 06 only as canonical  
3. Keep both as Layer View vs Stack View without merge  
4. **Merge into one canonical document absorbing both**

## Decision

Option 4 — merge into `governance/SYSTEM_ARCHITECTURE.md` v1.1.0.

## Justification

Operator explicitly approved the merge. A single document preserves:

- eight logical layers and eight capability subsystems (from 05)
- explicit stack and event/database detail (from 06)
- resolved UI computation boundary
- tightened execution language consistent with Vision / Roadmap Wave 6

## Consequences

- `05` and `06` are **SUPERSEDED** (historical retention only).
- All future architecture citations use the merged document.
- Related readiness risks **R-01** and contradiction **C-01** are closed pending ITRGA awareness.
- No application code was written as part of this decision.

## Related

- `governance/SYSTEM_ARCHITECTURE.md` v1.1.0
- `governance/DOCUMENT_PRECEDENCE.md` v1.0.0
- `governance/PROJECT_READINESS_REPORT.md` (addendum)

---

**End of EDR-001**
