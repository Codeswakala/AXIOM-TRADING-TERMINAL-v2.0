# Operator Decision — V2 BE-4 Scope Decision (SD-1, SD-2)

| Field | Value |
|---|---|
| Decision ID | `AXIOM-V2-OD-BE-4-007` |
| Date | 2026-08-31 |
| Decided by | Operator (stated 2026-08-31; recorded by ITRGA) |
| Basis | `ITRGA-ASS-V2-BE-4-SCOPE-001` (SD-1/SD-2 options; Option A recommended for both) |
| Related decisions | `AXIOM-V2-OD-BE-4-006` (BE-4 chain opened); `AXIOM-V2-OD-BE-3-P2-003` (programme sequencing directive — remains in force) |

## Decision (verbatim)

> Operator decision: for BE-4, I decide **SD-1 = Option A** (labelled-synthetic data basis; persistence remains a separate, later-governed act) and **SD-2 = Option A** (API-level evidence closure; browser evidence a recorded residual). I direct the DA to produce the BE-4 design plan per the requirements of `ITRGA-ASS-V2-BE-4-SCOPE-001` §6. **No repository changes are authorized by this decision.**

*Record note:* the submission presented the decision text in two identical copies; it is recorded once. No substantive difference between the copies.

## Effect

1. **SD-1 = A (data basis):** BE-4 is built and evidenced against the BE-2 normalized model fed by the **V1 simulator adapter (labelled synthetic)** — pipeline-validation tier (roadmap §0.2). `persistence_permitted` remains `false`; **no provider network call in any test**; no credential read/set/use. Real-data research validation (real historical data via a permitted, integrated source) is a **separate, later-governed act** and does not block BE-4 closure.
2. **SD-2 = A (exit evidence):** BE-4 closes on **API-level evidence** (direct API evidence of facts versus interpretation; full determinism / temporal-integrity / lineage evidence). **Browser evidence is a recorded residual**, to be verified at the FE band / X-01 joint gate. The sequencing directive is **unchanged**.
3. The **DA is directed** to produce the BE-4 design plan per `ITRGA-ASS-V2-BE-4-SCOPE-001` §6. ITRGA formalizes this direction as request **`ITRGA-REQ-V2-BE-4-001`** (`ITRGA_REQUEST_V2_BE-4_DESIGN_PLAN.md`), which carries the pre-registered guardrails and the required plan content.
4. **No repository changes are authorized by this decision.** Nothing in the chain to date has modified any file, table, or configuration.
5. **Chain state:** scope assessment stage complete; the chain is at **stage 4 — DA design plan** (awaiting delivery per `ITRGA-REQ-V2-BE-4-001`). No Build Order issues before an ITRGA-approved plan (roadmap §3; pre-work pattern).
6. **Credential law:** the decision text was scanned before archiving — **CLEAN** (no credentials, no account identifiers, no provider keys, no bearer or dev-marker strings).

— recorded by ITRGA, 2026-08-31
