# AXIOM Document Precedence Policy

| Item | Value |
|------|--------|
| Document ID | AXIOM-GOV-PREC-001 |
| Version | **2.0.0** |
| Status | **ACTIVE** |
| Authority | `10_CONSTITUTIONAL_HIERARCHY.md` + Operator/ITRGA (W0-U07 baseline notice F-4) |
| Last Updated | 2026-07-11 |

---

## 1. Purpose

This policy implements the **constitutional hierarchy** defined in `10_CONSTITUTIONAL_HIERARCHY.md`.

When documents conflict, the **higher tier always prevails**. Lower documents shall be amended; implementation shall not proceed on unresolved conflicts.

---

## 2. Constitutional pyramid (Tier 1 highest)

| Tier | Authority | Canonical document(s) |
|------|-----------|------------------------|
| 1 | Vision & Principles | `00_VISION_AND_PRINCIPLES.md` |
| 2 | Constitutional Specification | `03_AXIOM_SPEC.md` |
| 3 | Strategic Roadmap | `04_PROJECT_ROADMAP.md` |
| 4 | Technical Constitution | **`05_SYSTEM_ARCHITECTURE.md` (v2.0)** |
| 5 | Domain Constitutions | ML: `07_ML_SPEC.md` (workspace); UI/UX: `08_UI_UX_SPEC.md` (workspace naming). Hierarchy text cites `06_ML_SPEC` / `07_UI_UX_SPEC` as logical names — map to current corpus files until renumbered. |
| 6 | Institutional Reasoning | `09_DEVELOPER_REASONING_FRAMEWORK.md`; ITRGA reasoning framework when provided |
| 7 | Operational Governance | `PROJECT_STATE.md`, technical debt, risk, quality gates, amendments |
| 8 | Execution Governance | Build Orders, ADRs, engineering plans |
| 9 | Engineering Evidence | Code, tests, runtime evidence, Delivery Reports |
| 10 | Institutional Investigation | ITRGA ITRRs |

Also retained:

| Domain | Document |
|--------|----------|
| Product Mission | `01_PRODUCT_MISSION.md` (subordinate to Vision; elaborates product) |
| Design Philosophy | `02_DESIGN_PHILOSOPHY.md` (design criteria; subordinate to Vision/Spec) |
| DA Operations | `DEV_AI_ONBOARDING.md` |
| Constitutional Hierarchy | **`10_CONSTITUTIONAL_HIERARCHY.md`** (this policy’s parent) |

---

## 3. Architecture authority (F-4 / W0-U07)

| Document | Status |
|----------|--------|
| **`docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0** | **CANONICAL — single authoritative architecture** |
| `docs/governance/SYSTEM_ARCHITECTURE.md` (v1.1 merge) | **SUPERSEDED** — historical only |
| Pre-merge `05`/`06` uploads from project start | Historical only |

Chart State Service (architecture §30): **presentation state only** — no analytical reasoning in the chart layer.

---

## 4. Domain-family supersession (still valid)

Within the same domain family, a newer document becomes superior when **provided and the DA is explicitly notified** (Operator/ITRGA update notice). Cross-tier conflicts still resolve by **tier number** first.

---

## 5. Build Order citation rule (F-4)

W0-U07 and future Build Orders cite the **canonical set**. Delivery Reports shall reference:

- `00_VISION_AND_PRINCIPLES.md`
- `03_AXIOM_SPEC.md`
- `04_PROJECT_ROADMAP.md`
- **`05_SYSTEM_ARCHITECTURE.md` v2.0**
- Domain ML/UI specs as present in workspace
- `10_CONSTITUTIONAL_HIERARCHY.md`

Not: retired `AXIOM_SYSTEM_ARCHITECTURE_MERGED v1.1` or `03_AXIOM_SPEC_v1.1` filenames.

---

**End of Document**
