# OPERATOR DECISION — AXIOM V2: 0043 WORKING-DATABASE APPLICATION ACT

| Field | Value |
|---|---|
| Decision ID | `AXIOM-V2-OD-BE-4-009` |
| Date | 2026-09-02 |
| Decided by | Operator (stated "authorized" in direct response to ITRGA's exactly-one-next-action of 2026-09-02; recorded by ITRGA) |
| Basis | `ITRGA-DET-V2-BE-4-FINAL-001` §7 (residual B-1); `ITRGA-CHK-V2-BE-ROADMAP-001` §B (item B-1); `ITRGA-PTN-V2-PACK-001` §4 |
| Related decisions | `AXIOM-V2-OD-BE-4-008` (BE-4 Build Order; 0043 delivered, not applied); `AXIOM-V2-OD-BE-3-P2-004`/`-005` (the apply-act pattern precedent) |

## Verbatim statement

> authorized

## Record note

The Operator's statement is the single word "authorized", issued in direct response to ITRGA's exactly-one-next-action of 2026-09-02: *"Issue OD-009: authorize the 0043 working-DB application act (sanctioned pack, file-level backup anchor, verify act; re-pins 0038/0039/0041 as precondition; no other repository change authorized)."* The scope of this decision is exactly the scope of that instruction; ITRGA records no broader authority.

## Effect

1. The application of migration `20260831_0043_v2_be4_research_read_models` to the application's working SQLite database (`backend\axiom_dev.db`) is authorized as a **single sanctioned apply act**, per the BE-3 P2 transition apply-act pattern: sanctioned ITRGA apply pack (MD5 self-check, fail-atomic), file-level backup anchor, and a subsequent read-only verify act.
2. Precondition (recorded in the OBS-9 residual): ITRGA re-pin of migrations 0038/0039/0041 against the accepted records before pack issuance. **Resolved 2026-09-02 in the same session by ITRGA Level II recomputation — all three VERIFIED — see `ITRGA-ASS-V2-0043-APPLY-001` §3.** No external input is required for this act.
3. The working database is mutated **exactly once**, by the sanctioned apply pack. **No other repository change is authorized by this decision. No Git operation is authorized** (custody remains deferred). No other migration is applied. The creation of the three BE-4 tables, their six guard triggers, three indexes, two unique constraints, five permission seed rows, and three computation-version seed rows is the sole state effect.
4. ITRGA opens the governed chain: scope assessment → plan → Build Order → sanctioned instruments (apply pack + verify pack, full battery) → Operator execution → verify → act-closure determination.
5. Credential law applies to every artifact of this chain: scan before archive; the Four Secrets are never shared, never recorded, `***` in all transcripts.

— recorded by ITRGA, 2026-09-02
