# ITRGA PRACTICE NOTE — SANCTIONED-PACK DISCIPLINE AND PACE COMMITMENTS (V2 CHAIN)

Practice Note ID: `ITRGA-PTN-V2-PACK-001`
Date: 2026-09-02
Trigger: Operator question of 2026-09-02 — "we still have a lot of work and we are moving slowly due to multiple errors that require corrections; can we increase the pace?"
Scope: binds ITRGA's own instrument-issuance and review practice for all subsequent sanctioned acts. Changes no determination, no build order, and no governance rule. The invariants of the charter and onboarding (independent review, no self-authorization, one decision per act, fail-atomic instruments) are NOT negotiable and are not relaxed by this note.

## 1. Error ledger — what actually slowed the record (all facts, no attribution games)

**Apply act, BE-3 P2 TRANSITION (2026-08-31):** 5 instrument attempts (V1–V5). ITRGA-owned findings PGF-001…PGF-012 (12, all LOW) were each found by the instrument's own fail-atomic gates, owned, and corrected in dated supersessions **before** any state damage. The working database was mutated exactly once (attempt V5, 2026-08-31 14:09:55 +03:00) and has been byte-identical ever since (re-proven in verify runs 1, 3, 4, 5 — sha256 `0483f9fe…`). Every correction in this chain happened in the instrument, never in the database.

**Verify re-run cycle (2026-09-01 → 2026-09-02):** 4 re-runs after the run-1 PASS:

| Run | Instrument | Outcome | Root cause | Whose "error" | Status |
|---|---|---|---|---|---|
| 2 | V1 | FAIL at B2 | Environment event: repository head moved to 0043 (the 2026-09-01 17:26 +03:00 bulk-write event, OBS-9). The instrument **correctly detected and aborted** — that is a guard working, not a defect | No instrument defect (record: "no ITRGA instrument defect is claimed for the abort") | Superseded by V2 re-pin |
| 3 | V2 | FAIL at B9 | **PGF-014 (a)** — B9 token assertions were format-dependent on the alembic output format, which changed with the venv (now recorded: alembic 1.19.0) | **ITRGA instrument defect — owned** | Superseded by V3; CLOSED 2026-09-02 |
| 4 | V2 (superseded) | FAIL at B9 | The superseded instrument was executed instead of V3 (file selection at the console; the self-check step was performed correctly, on the V2 filename) | Operator selection slip; no procedure deviation, no defect | Record only; V3 proven present on machine by the run itself |
| 5 | **V3** | **PASS** | — | — | Instrument of record; PGF-014 (a)+(b) closed |

**Finding register: PGF-001…PGF-014 — 14 findings, all LOW, all ITRGA-owned, ALL CLOSED.** Zero open instrument defects as of this note.

Honest read for the Operator: of the four red-flagged runs, one was the guard doing its job on a real environment change, one was a genuine ITRGA defect (owned, fixed, closed), one was a superseded file at the console, and the corrections never touched the working database. The slow part was real; its cause is now fully identified, and the two ITRGA-controllable causes (instrument fragility; ambiguity at the console) are addressed below.

## 2. Committed practice changes (effective from the next sanctioned pack)

1. **Pre-issuance battery floor (raised).** Every sanctioned pack ships only after: (a) deterministic `${...}` span audit; (b) full AST parse (PowerShell 7.x); (c) a dry-run matrix that is the **V3 five-case matrix as the minimum** — i.e. both observed alembic output formats × the observed head states, at least one negative case, and one world replicating the current operator-machine environment (recorded facts: alembic 1.19.0, head `20260831_0043`, DB at `20260829_0042`); (d) MD5/SHA-256 of the issued bytes recorded at issuance.
2. **Embedded Operator instruction card.** Every pack header carries the five-line card: exact self-check hash (MD5), exact execution command naming **that one file**, the single expected input, the exact transcript path to send, and the line: *do not execute any other pack file; if the self-check hash does not match, stop and report to ITRGA.* This eliminates the run-4 class of error.
3. **Same-session turnaround.** Evidence in → assessment + (where in scope) corrected instrument issued, within the same working session. (Practice since run 2; now a commitment.)
4. **Up-front dependency disclosure.** Every act's chain opens with the scope note listing its external inputs (e.g. the 0038/0039/0041 re-pins for the 0043 application act) so nothing stalls mid-chain. A stall caused by an undisclosed ITRGA-side dependency is an ITRGA defect.
5. **Supersession made inaudible.** Superseded instruments are listed with explicit "SUPERSEDED — do not execute" status in every subsequent instruction card.

## 3. What this note does NOT change (the pace floor)

- One Operator decision per act. ITRGA does not self-authorize, pre-approve, or batch-approve.
- Independent review of every plan and delivery; fail-atomic instruments; the working database is mutated only by a sanctioned apply act with anchor + verify.
- The gates are what caught every defect in this programme — including all 14 ITRGA findings — before they could reach state. Compressing them converts detected errors into undetected ones; that is not pace, that is risk.

## 4. Net effect

The remaining path to the next band exit is known and short: the 0043 application act (B-1) is a two-run act (sanctioned apply run + read-only verify run) whose only open dependency — the 0038/0039/0041 re-pins — is disclosed up front (item 2.4). With items 2.1–2.5 in force, the expected remaining correction surface for that act is near zero; the instrument is pre-validated against the exact recorded environment (alembic 1.19.0) before it ever reaches the console.

— ITRGA, 2026-09-02
