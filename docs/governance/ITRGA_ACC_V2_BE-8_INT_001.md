# ITRGA-ACC-V2-BE-8-INT-001 — INT ACCEPTANCE + DRIFT GATE (BLOCKING SEAL)

- **Record:** v1.0.0 · 2026-09-05 · AXIOM V2 / BE-8 (paper trading)
- **Chain:** REQ → DESIGN v1.1.0 ACCEPTED (`76e718c4…ccc073`) → BO-V2-BE-8-001 → DR v1.0.0 → ITRGA-REV-V2-BE-8-INT-001 (BUILD PASS) → DA-INT-ACK-001 → ITRGA-INTAKE-V2-BE-8-ACK-001 → **THIS ACCEPTANCE**
- **Status:** **INT ACCEPTED**. The 0048 working-DB act remains a **separate, not-yet-authorized** Operator declaration.

## 1 — Operator declaration (on file, 2026-09-05)

The Operator directed: *"there is no need to check for hashes for the delivery report files, only the necessary ones — you can issue INT acceptance + drift-gate instrument."*

Recorded precisely to forestall any future claim-inversion: **no verification was skipped.** At review time each of the following was already executed and passed:

| Layer | Verification already on record |
|---|---|
| Report-evidence identity | All 5 artifact md5/bytes == the DR §5 manifest (ITRGA intake, REV-INT) |
| Source corpus | 20/20 transcript bodies re-hashed == declared per-file SHA-256; manifest rows == block declarations 1:1 |
| Amendment anchoring | 5 diffs == sanctioned amendments only, vs 0047-act pins (`ad4afdd4…`, `a3dff082…`, `32b0f770…` re-produced from the BE-7 source corpus) and repo references |
| DA disk | DA §2 full sweep: 20/20 byte+sha match (corroboration) |
| Compver expectations | PXS/PRG independly recomputed == DA pre-declared (INTAKE memo) |

The waived item is the Operator's personal second spot-hash only. **INT acceptance stands on performed verification, not on trust.**

## 2 — Accepted baseline (constitutionally gating)

- Migration head: **`20260904_0048`** (single-revision op from `20260903_0047`).
- Suite floor: **1,026 passed / 0 failed** = 972 (0047 baseline) + 54 BE-8 (15+10+16+13 across `test_v2_be8_simulator|migration|orders|boundaries`).
- Census pins: **57 permissions** (49+8), **58 triggers** (42+16), **10 computation versions** (8 + pxs-1.0.0 + prg-1.0.0), **8 paper tables**, and the exact paper API surface of **14 routes** (6 POST writers + 8 GET readers — asserted by `test_api_surface_census_exact`, counted directly in `api.py`).
- Corpus frozen: the 20-file §PINS census of ITRGA-REV-V2-BE-8-INT-001 binds every future comparison (re-stated in §4).

## 3 — DRIFT GATE (binding at the act; auto-checked into the act evidence set)

1. **Audit-write checklist** — every paper writer/reader refusal path audits durably (12 observed audit classes incl. refusal audits); refusal audits commit before return (C-1 law).
2. **Alembic-check evidence, both heads, both DB file-format forms** (the parametrized gate): nonzero exit expected; **zero BE-8 drift tokens** (`v2_paper_account`, `v2_paper_order_intent`, `v2_paper_risk_decision`, `v2_paper_order_event`, `v2_paper_fill`, `v2_paper_position_snapshot`, `v2_paper_balance_snapshot`, `v2_paper_reconciliation`) at head **and** at pre-upgrade; the inherited V1 drift is exactly the **9-token class** with `audit_write_failure_records` as representative; 18 printed ops = 9 tokens × 2 heads (arithmetic, on record).
3. **Suite re-print at act boundary**: 1,026/0 only; any other byte = act aborts.
4. **20-file station census** at the act: every delivered path hashed vs §PINS before the upgrade runs; mismatch = act aborts, bytes restored from the pinned transcript corpus.
5. **Any drift, census miss, hash mismatch, or suite regression = the act is void before it starts and the anomaly is a typed refusal surface, never corrected in-place.**

## 4 — PINS carried into the act (frozen corpus; sha256)

Twenty rows as pinned in ITRGA-REV-V2-BE-8-INT-001 §PINS (15 new + 5 amended), with the apply-time compver expectations verified against that corpus:

```
pxs-1.0.0 (paper_execution_suite, over {simulator.py, ledger.py}):   c58a06a5402f30a3828012f91b4aeb564008a9bfa34685cc57558e1003d106c0
prg-1.0.0 (paper_risk_gateway,  over {risk.py, contracts.py}):       ed6434fa5ff00b937b71e1d76a8fef32bc019f134e56831ac9f74af525376b1b
RPE/RJE compver rows: unchanged (0047 bytes carried; no rewrite permitted)
```

Law: computed at apply-time from live disk via the migration's own rolling-hash recipe; the act instrumentation prints all four rows and pins them to this table — divergence means bytes moved after pinning = abort.

## 5 — Post-act obligations (staged, not applied)

- **DA** files the register entry staged in DA-INT-ACK §4 (verbatim line + the F-e operator-option sentence: granting operator `v2.paper.*.read` remains an open Operator option for a later governed act).
- **Maturity**: BE-8 build phase = COMPLETE (this seal). Run/act phase = PENDING the Operator's explicit 0048 authorization.

## 6 — Next lawful action (one only)

**Operator authorization of the 0048 application order** (working-DB upgrade `20260903_0047 → 20260904_0048` on the 0047 chassis + PGF-020…024 statutes + E-0046-DUP startup law + register sync). This instrument does **not** authorize it. On your explicit word I issue the application order with these pins compiled in.

**We don't guess. We prove.**
