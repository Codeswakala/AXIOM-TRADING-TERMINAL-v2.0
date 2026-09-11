# AXIOM V2 — Programme Charter

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-GOV-CHARTER-001 |
| Status | **APPROVED** (Operator Decision AXIOM-V2-OD-001, 2026-08-23) |
| Date | 2026-08-23 |
| Author | Development Authority (DA) |
| Build Order | BO-V2-BE-0-001 |

---

## ⚠️ CHARTER STATUS: APPROVED

**This document was drafted by the DA and approved by the Operator on 2026-08-23 per Decision AXIOM-V2-OD-001. It is active governing context for V2 planning and future governed capability work.**

---

## 1. Purpose

This Charter establishes AXIOM Version 2 as an authorized programme extending the V1 foundation into a broader institutional trading and research platform.

## 2. Programme Definition

AXIOM V2 is a deliberate expansion of V1. It is not a replacement. V2 extends V1 into:

- Real and historical market data
- Market context and chart intelligence
- Portfolio and risk management
- Paper trading
- Broker connectivity
- Governed execution
- Backtesting and simulation
- Research automation
- Contextual AI assistance

## 3. V1 Preservation

**All active V1 governing documents remain binding on V2.** Per the Operator decision in `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md`:

- V1 historical evidence is immutable
- V1 Build Orders, Delivery Reports, and ITRGA determinations are preserved
- V1 Git history is preserved
- V1 code, tests, and migrations are preserved

## 4. Governance Model

V2 operates under the same three-authority model as V1:

| Authority | Role |
|-----------|------|
| Operator | Product direction; capability authorization; Charter approval |
| Development Authority | Engineering design; implementation; testing; evidence; Delivery Reports |
| ITRGA | Independent review; evidence assessment; governance findings; determinations |

## 5. Programme Scope

V2 is organized into backend bands (BE-0 through BE-11) and frontend bands (FE-0 through FE-10) as defined in the V2 Backend and Frontend Roadmaps.

## 6. Mode Scope

| Mode | BE-0 Status | Future Status |
|------|-------------|---------------|
| RESEARCH | **Active** | Active |
| SIMULATION | **Active** | Active |
| PAPER | Deferred | Requires BE-8 design and security review |
| LIVE | Deferred | Requires BE-10 design, security review, and production certification |

## 7. Non-Negotiable Invariants

1. V1 historical truth is immutable
2. No fabricated domain state
3. Authoritative work is server-side
4. Frontend-to-broker communication is prohibited
5. Mode isolation is technical, not decorative
6. Execution is default-deny
7. Provider/broker secrets remain isolated
8. Unknown is an allowed state
9. Every material result is traceable

## 8. Amendment Process

Any V2 provision that amends a V1 requirement must:
1. Identify the affected V1 document and section(s)
2. State the prior rule
3. State the replacement rule
4. Define effective scope and date
5. Be approved by the Operator
6. Be recorded in `V2_AMENDMENT_REGISTER.md`

## 9. Approval

| Field | Value |
|-------|-------|
| DA Draft Date | 2026-08-23 |
| Operator Approval | **2026-08-23** (Decision AXIOM-V2-OD-001) |
| ITRGA Determination | APPROVED WITH OBSERVATIONS |

---

**End of Programme Charter (DRAFT)**
