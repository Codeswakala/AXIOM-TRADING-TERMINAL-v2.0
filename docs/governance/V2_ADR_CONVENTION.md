# AXIOM V2 — Architecture Decision Record (ADR) Convention

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-GOV-ADR-001 |
| Status | Active |
| Date | 2026-08-23 |
| Author | Development Authority (DA) |
| Build Order | BO-V2-BE-0-001 |

---

## Purpose

Architecture Decision Records (ADRs) document significant architectural decisions made during V2 development. They ensure decisions are traceable, justified, and preserved as institutional knowledge.

---

## ADR Format

```markdown
# ADR-V2-NNN: [Title]

| Field | Value |
|---|---|
| ADR ID | ADR-V2-NNN |
| Date | YYYY-MM-DD |
| Status | Proposed / Accepted / Superseded / Retired |
| Decision Makers | DA / Operator / ITRGA |
| Related Band | BE-N |

## Context

[What is the issue that we're seeing that is motivating this decision?]

## Decision

[What is the change that we're proposing and/or doing?]

## Alternatives Considered

1. [Alternative A] — [pros/cons]
2. [Alternative B] — [pros/cons]

## Consequences

[What becomes easier or more difficult because of this change?]

## Related

- [Links to related ADRs, Build Orders, or documents]
```

---

## ADR Rules

1. Every significant architectural decision gets an ADR
2. ADRs are immutable once accepted — supersession is by a new ADR
3. ADRs are authored by the DA and reviewed by ITRGA
4. ADRs do not authorize implementation — Build Orders do
5. ADR IDs are sequential: `ADR-V2-001`, `ADR-V2-002`, etc.

---

## ADR Register

| ADR ID | Date | Title | Status |
|--------|------|-------|--------|
| *(No ADRs yet — register initialized)* | | | |

---

**End of ADR Convention**
