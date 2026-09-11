# ITRGA PLAN — 0043 WORKING-DATABASE APPLICATION ACT · INSTRUMENT DESIGN

Plan ID: `ITRGA-PLAN-V2-0043-APPLY-001`
Date: 2026-09-02
Authority: `AXIOM-V2-OD-BE-4-009`; scope per `ITRGA-ASS-V2-0043-APPLY-001`
Status: ISSUED for Build Order drafting (this plan does not authorize execution; execution is by sanctioned instrument only)

## 1. Instrument set (two sanctioned instruments, two console runs)

| Instrument | Kind | Mutation | Purpose |
|---|---|---|---|
| Apply pack (V1) | sanctioned apply act | **one** mutation (the 0043 upgrade) | apply 0043 to the working DB with pre-checks, anchor, post-checks |
| Verify pack (V1) | read-only verify act | none | re-prove the terminal state in a fresh run; closes the act with the closure determination |

Both: PowerShell 5.1 compatible, pure ASCII, `${}` bracing only for `^[A-Za-z_][A-Za-z0-9_]*$` names (PGF-009), no param-alias collisions (PGF-001), UTF-8 console + `PYTHONIOENCODING` (middle dot via `chr(183)`), failure-atomic (verdict only at the end), embedded Operator instruction card (PTN-V2-PACK-001 §2.2), MD5 self-check step (PGF-011).

## 2. Apply pack — boundaries (abort before mutation on any pre-check failure)

- **A0 RUN IDENTIFICATION** — pack self-ID (`ITRGA-V2-0043-APPLY-PACK-V1`), OD-009, started, repo root, target file (single Read-Host input, PGF-008 quote-stripping, leaf-name check, not-inside-evidence check), credentials NONE, read-write scope statement (one sanctioned mutation).
- **A1 BASELINE (pre-mutation)** — working DB: size 1,310,720 B; last write 2026-08-31 14:09:55 +03:00; sha256 `0483f9fe…` (byte-identity to the in-force state — **abort on any difference**); sqlite version; `integrity_check` ok; journal delete; no sidecars; **12 v2 triggers**; `alembic current` token exactly `20260829_0042` (**abort if not exactly 0042 — in particular if already 0043**); alembic version recorded (informational).
- **A2 ANCHOR** — copy the working DB to `operator-evidence\BE-4\axiom_dev.db.pre-0043-<yyyymmddhhmmss>.bak` (directory created by the pack); record size + sha256; `integrity_check` on the copy ok. **The mutation may not precede a valid anchor.**
- **A3 PROVENANCE (on-disk, runtime)** — sha256 of `backend\alembic\versions\20260831_0043_v2_be4_research_read_models.py` = `ab905762…`; sha256 of 0038 = `6e071157…`; 0039 = `bc11cae2…`; 0041 = `d775c34a…` (the re-pinned values of `ITRGA-ASS-V2-0043-APPLY-001` §3). Abort on any mismatch.
- **A4 APPLY** — exactly one invocation: `alembic upgrade 20260831_0043` via the repo venv python (CAP Continue, merged output, exit-code check). Environment block as the verify packs (testing env, pack-managed values, TD variables removed; **no authority variable exists for this act**).
- **A5 POST-APPLY STATE** — `alembic current` = `20260831_0043`; **18 v2 triggers**; the six new guard trigger names exact; the three tables present (`v2_computation_version`, `v2_market_context_report`, `v2_chart_intelligence_report`); constraints `uq_v2_compver_component_version`, `uq_v2_mcr_determinism_anchor`; indexes `ix_v2_mcr_instrument`, `ix_v2_mcr_mode`, `ix_v2_cir_mcr`; 5 permission seed rows; 3 computation-version seed rows; integrity ok; journal delete; no sidecars; final file state recorded (size/last-write/sha256 — new expected values; the anchor sha256 must still equal the A2 record).
- **A6 GUARD SPOT-CHECKS** — six `tryrefuse` probes: UPDATE + DELETE on each of the three tables, each refused with the exact R-2 message (`V2 computation version registry is immutable; % prohibited` / `V2 market context reports are immutable; % prohibited` / `V2 chart intelligence reports are immutable; % prohibited`).
- **A7 DRIFT RE-BASELINE** — format-independent (PGF-014 discipline): non-zero exit + "not up to date" asserted (inherited V1 drift persists); when the alembic version prints the itemized list: the token set must be **exactly the 9 inherited V1 tokens** — no `v2_*`/`ix_v2_*` token may appear (the BE-4 set must have left the drift set); when it prints the summary: PGF-014 NOTE line + existence assertion (itemized set stands from run 1 lineage + A5 table/trigger presence proves the BE-4 objects exist).
- **A8 VERDICT + CLEANUP** — APPLY VERDICT (PASS only at the very end), anchor path, transcript path, env cleanup, helper removal, "restart the application when ready".

## 3. Verify pack (V1) — terminal-state re-proof (read-only)

Same boundary skeleton as verify pack V3 (instrument of record), re-pinned to the post-apply world:
- B1: file state (new expected size/sha256 recorded at apply A5 — **the verify pack pins the apply pack's recorded final values**; last write = the apply act's; integrity; journal; sidecars; **18 v2 triggers**).
- B2: current revision exactly `20260831_0043`; repository head recorded (expect `20260831_0043`; alembic version recorded).
- B3: anchor (the 0043 pre-image) present, integrity ok, sha256 cross-checked against the apply record.
- B4–B6: the three tables' seed content exact (3 computation-version rows; the permission seeds count/classification; report tables empty — no rows yet; content-exact where rows exist).
- B7: six guard refusals exact (R-2).
- B8: no authority variable (n/a for this act — recorded as UNSET-NA, the six TD variables absent as in prior acts).
- B9: drift = exactly the 9 inherited V1 tokens (format-independent, as A7).
- Terminal verdict PASS only at the very end; final file state must equal B1.

## 4. Verification battery (PTN-V2-PACK-001 §2.1 floor; record to be archived)

1. Deterministic `${...}` span audit (every span fullmatches the PGF-009 pattern; `$env:` provider syntax exempt).
2. Full AST parse (pwsh 7.x), zero errors.
3. Dry-run matrix in the controlled world (faithful schema at the 0042 state — the proven recipe — plus the **real hash-verified 0043 file**; alembic shim extended to execute `upgrade 20260831_0043`):
   - W1: apply success, itemized drift world (end state = 0043, 18 triggers, drift = 9 tokens) → PASS;
   - W2: apply success, summary-format world (the recorded operator environment, alembic 1.19.0 class) → PASS;
   - N1: baseline sha256 altered → abort at A1, **DB byte-unchanged, no anchor, no mutation**;
   - N2: 0043 file hash altered → abort at A3, no mutation;
   - N3: current revision already 0043 → abort at A1, no mutation;
   - N4: anchor copy integrity fails → abort at A2, no mutation;
   - verify pack dry run against the W2 post-apply state → PASS.
4. MD5/SHA-256 of the issued bytes recorded at issuance; instruction card embedded; superseded instruments (verify V1/V2, the V3 verify pack — still valid but **not the instrument for this act**) marked "do not execute for this act".

## 5. Environment requirements (Operator console)

Application stopped before the apply run (live connection holds the SQLite file); repo root `C:\Users\victo\.vscode\AXIOM\axiom`; PowerShell 5.1; venv python; network not required by the packs; no credential of any kind.

## 6. Closure

Apply pack PASS + verify pack PASS (both transcripts archived, credential-scanned) → ITRGA act-closure determination (`ITRGA-DET-V2-0043-APPLY-001`): working DB at head 0043; drift re-baselined to the 9 inherited V1 tokens; 18 v2 triggers in force; residual B-1 of `ITRGA-DET-V2-BE-4-FINAL-001` §7 closed.

— ITRGA, 2026-09-02
