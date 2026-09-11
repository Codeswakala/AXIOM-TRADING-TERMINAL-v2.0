# DA TECHNICAL REVIEW — REQ-V2-BE-11-001 (input to the Operator adjudication)
# AXIOM-V2-BE-11-DA-REQREV-001 · v1.0.0 · 2026-09-06 · AXIOM Trading Terminal v2.0
# Object: REQ-V2-BE-11-001 "Paper-Execution Bridge to Live Practice-Book Truth"
# Author: Replacement Development Authority (DA)
# Reading rule: adjudication is the OPERATOR'S (ADOPT/AMEND/REFUSE per section).
# DA-side feasibility input only. No ruling made or implied.

---

## §0 — Register note acknowledged

The REQ's header adopts ruling-(b) convention from BE-10: band-id BE-11,
roadmap execution family renumbers to BE-12+ at its future commissioning.
The DA has applied the consequential maturity-register annotation at the
BE-10 closeout sync (v1.5.0: Execution Gateway / Order Management /
Position Management rows → BE-12+ with the ruling citation). The register
collision flagged at the BE-10 REQ is thereby resolved convention-forward.

## §1 — Section-by-section technical assessment

| Section | DA assessment |
|---|---|
| R-0 mission | Sound and exactly what the standing stack supports: the BE-8 paper machinery (8 `v2_paper_*` tables, all zero rows on the working lineage — the survey's fact) has never had a REAL balance/position basis to size against; BE-9 supplies it. The loop-close is the natural next band |
| R-1.1 IN | Feasible with one seam note: the BE-8 paper domain and the BE-9 broker domain are separated by the N3 wall — **tested from both sides** (`test_n3_paper_wall_from_broker_side` / `_from_paper_side` forbid cross-imports). The bridge band therefore CANNOT live inside either domain; it must be a third package (e.g. `app/v2/paper_bridge/`) that imports from both — and the N3 wall tests stay untouched (they bind the two domains, not the bridge). The DR must declare this wall-preserving topology explicitly; the boundary scans then grow a bridge-specific law (bridge may import both domains' PROJECTIONS/engines; the domains still may not import each other or the bridge) |
| R-1.2 IN | The drift surface is BE-8's `reconcile()` law generalized: paper-ledger derivation vs broker-truth projection, exact-compare with EXPLICIT seeded tolerance bands (R-3.4 — a deliberate, welcome departure from BE-9's no-tolerance law, since paper-vs-broker drift is a DIFFERENT comparison class: two independent simulations of the same world, not one authority vs its projection). State-noun vocabulary inherits cleanly |
| R-1.3 OUT | Fully enforceable with standing machinery; the strengthened banned-import set is one line of law. Note the strongest structural fact available: BE-8's `EXECUTION_BACKENDS` frozen registry still has exactly one key (`paper`), and the investor password makes broker-side writes impossible even under total code compromise — the two arms compose |
| R-1.4 OUT | The fail-closed default (intents + gateway decisions only; fill simulation deferred absent lawful price basis) is correct. **DA pre-survey for the DR's first evidence act** (candidate surfaces present on the schema; working-DB row counts are the act's job): (a) V1 `candles` corpus — 109,326 real bars, but `historical_real` is CORPUS-GATED (V2-TD-18) and stale vs a live book; (b) v2 md bars — the BE-7 governed lineage, synthetic/simulated classes; (c) **`v2_broker_fill` prices + `v2_broker_position` avg prices — BE-9 projection FACTS, provenance-pinned, same basis discipline as the balances the gateway sizes against**. DA's non-binding early read: (c) is the only price family that is both lawful and basis-consistent today; it supports mark-to-basis ledger math but NOT bar-replay fill simulation — which aligns with the REQ's conservative default. The DR's evidence act decides on working-DB rows |
| R-2 | Correct. pxs/prg consumed as-is (compver-pinned; any byte movement would trip the standing rolling-hash law); the bridge is a thin join. One migration, compver +1 (`paper_bridge_engine`-class), zero new tables unless the DR justifies (the drift surface may justify ONE lineage table on the BE-9 `reconcile_run` precedent — clean runs must be evidenced, C-2 law; the DR should carry that question explicitly) |
| R-3.1 | Per-world determinism canon (N-O13 law) ports directly: digest over (basis sync_run_id, intent payload, pxs/prg/bridge versions) |
| R-3.2 | All three arms are standing law generalized; nothing new to invent |
| R-3.3 | The reason-coded decision vocabulary (`accept-with-notes / deferred / refused-under-policy`) is enumerable and closed; the naming law (no broker-order verbs in table/column names) extends the BE-10 wording scan to DDL identifiers — a one-test addition |
| R-3.4 | Seeded, audited tolerance bands: the BE-7 citation law is the right chassis (`{value, unit, citation}` per band — never a hidden default). Flag for the DR: band VALUES are Operator inputs at BO, like the BE-8 risk defaults (A-1 class) |
| R-3.5 | The BE-8 idempotency anchors already enforce this at schema (`uq(account_id, idempotency_key)` on intents); the bridge inherits rather than re-invents |
| R-4 | POST intents/evaluate + GET reads inside the standing `v2.paper.*` namespace — no new marker exemption needed (the D-1 prefix already stands); exact permission set is DR work. Note: POST writers put this band in PAPER mode territory (BE-8 D-2 law — writers demand `mode == "PAPER"`); the DR must declare the mode posture for the bridge writers explicitly |
| R-5 | Standard. Suite floor 1,121 + budget; DA early sizing (non-binding): ~35–45 tests |
| R-6 | All inherited disciplines already encoded or adopted DA-side (three-layer enumeration; interpreter pretense check noted and adopted for any DA-side act script; ASCII console; file-invoked scripts) |

## §2 — DA readiness statement

On ADOPT (with the R-1.4 evidence act as the DR's first station, as the
REQ itself orders), the DA is ready under the six-question discipline.
The three DR-stage questions the DA will bring answers for: the
wall-preserving bridge topology (§1 R-1.1), the drift-lineage-table
question (§1 R-2), and the bridge-writer mode posture (§1 R-4).

## §3 — BE-10 closeout register sync (executed with this memo)

Per `ITRGA-CAMPAIGN-BE10-CLOSE-001`: maturity **v1.5.0** — new row
`Account Context Intelligence → COMPLETE — OPERATING` (fielded head
`20260908_0050`, sha-after `90660b5d…f9de`; ace-1.0.0 verified
fielded-live; census 76/65/12; first-read witness wire==fielded; the
empty matrix is TRUE ACCOUNT STATE, not absence); execution-family rows
annotated BE-12+ per ruling (b). Corrected ACC edition (N-O9 pin fix
`…322a0a8de`) filed in place — DA-F1 closed as corrected. The correction
ledger's symmetry is noted for the record: N-O8/N-O9 DA-owned,
N-O10/N-O11/N-O13 ITRGA-owned, N-O12 environmental — six catches, six
closures, zero reached the field. The three-layer enumeration law and
the interpreter pretense check are adopted DA-side as standing.

**We don't guess. We prove.**

— AXIOM-V2-BE-11-DA-REQREV-001 · v1.0.0 · 2026-09-06
