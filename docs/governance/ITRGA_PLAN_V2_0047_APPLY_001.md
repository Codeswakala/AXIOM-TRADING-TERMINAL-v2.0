# ITRGA INSTRUMENT DESIGN RECORD — 0047 WORKING-DB APPLICATION ACT
# ITRGA-PLAN-V2-0047-APPLY-001 · v1.0.0 · 2026-09-04 · AXIOM Trading Terminal v2.0
# Authority chain: CN-V2-BE-7-001 → REQ → PRV → BO-V2-BE-7-001 (0047 application
#   named a separate sanctioned act) → INT (PASS) → FINAL → CR-001 →
#   ITRGA-ACC-V2-BE-7-001 (band accepted; §5 fixes this act's preconditions)
#   → operator authorization ("proceed", 2026-09-04) → THIS DESIGN RECORD.

## §1 — Act definition

Terminal act of the BE-7 chain: apply the ACCEPTED band corpus (17 delivered
files) and migration `20260903_0047_v2_be7_research_jobs` ONCE to the
application's working SQLite database (`backend\axiom_dev.db`, PS 5.1,
alembic 1.19.0, pytest 8.4.2, repo `.venv\Scripts\python.exe`), then prove
the terminal state independently. Delivered as the household pair:
`ITRGA_V2_0047_APPLY_PACK_V1.ps1` (runs first) +
`ITRGA_V2_0047_VERIFY_PACK_V1.ps1` (runs second) +
`ITRGA_V2_0047_BASELINE_PINS.txt` (repo-root pin file; strict KEY=VALUE).

## §2 — Apply instrument (A0–A10)

- **A0 startup hygiene (E-0046-DUP law):** refuse-if-completed — the pack
  never deletes a completed-run record; `AXIOM_TD_*` authority-variable
  sweep; baseline pin cross-check (11 keys).
- **A1 target + toolchain:** single input (DB path, quote-normalized);
  venv discovery (`.venv\Scripts\python.exe` primary); alembic 1.19.0 /
  pytest 8.4.2 gates; floor migration presence; 0047 file absence;
  `alembic current/heads` == single `20260903_0046`, not at 0047.
- **A2 rollback anchor:** byte-hash-compared copy to
  `operator-evidence\BE-7\0047-ANCHOR-axiom_dev.bak` + `integrity_check=ok`
  BEFORE any modification.
- **A3 pre-state pins:** six V1 files re-hashed vs attested pins; floor
  censuses exactly 32/41/6; the three overwrite targets must carry their
  BE-6 floor markers (router mounts, `RESEARCH_PF_READ`, `v2_portfolio`).
- **A4 file landing:** 17 base64 literals embedded in the pack; each
  decode→SHA-256→pin-checked BEFORE write; new files refuse-if-present;
  the three modified files are hash-witnessed, backed up to
  `pre-write-backup\`, overwritten with the pinned cumulative bodies, and
  re-hashed AFTER write.
- **A5 sanctioned mutation:** exactly one — `alembic upgrade head`;
  post-state `current == 20260903_0047 (head)`, single head.
- **A6 post-census:** 42/49/8 with exact members; ten trigger names
  present; `v2_research_job_immutable_*` proven ABSENT (FP-1 by-design);
  compver rows byte-exact to the ACC §5 literals — **RPE
  `1499343d48b778af17065e8bf1eaabcffc116880fa6967ab442db1255992b178`
  (unchanged) · RJE
  `8f107d174e081dc0a1527fea841b89dfb73744e3f16eba2d29c60521158c0598`
  (CR-001 value)** — the apply-time compver gate.
- **A7 live guard probes:** ten transactional insert-probe-rollback
  cycles; each refusal string compared EXACT against this pack's own
  independent literals; nothing persists.
- **A8 full suite:** `python -m pytest -q`, exit 0, summary declares
  `972 passed`, tail witnessed.
- **A9 drift gate:** `alembic check` non-zero exit required; zero
  band/v2 tokens (8-marker negative space, PGF-014); inheritance witness
  present.
- **A10 state record:** strict KEY=VALUE `0047-APPLY-FINAL-STATE.txt`
  (identity pinned), then PASS banner (restart only after verify PASS).

## §3 — Verify instrument (B0–B7)

Order law (strict-parses the apply record; refuses if its own completed
record exists — a verify that ran without the apply, or twice, is
refused); toolchain + target identity vs the apply record's DB_PATH;
re-hashes all 17 delivered files + 6 V1 pins; independent chain-head +
census re-computation vs THIS pack's embedded literals; the ten live
guard probes again; full suite again (972/0); drift gate again; writes
`0047-VERIFY-FINAL-STATE.txt` PASS. Trusts nothing it did not recompute.

## §4 — Pack proof summary (gates executed at issuance, all PASS)

PowerShell AST parse (PW 7.4.6): **0 errors** both packs. Post-build
gates (PGF-016): ASCII purity; here-string pairing 19/19 (apply) + 3/3
(verify) with closers alone on their lines; zero adjacent-duplicate
lines outside literals; brace/paren balance; no `$(` in strings; no
strict-glue seams. Pack-integrity proof executed with the pack's own
.NET calls: **17/17 embedded literals base64-decode and SHA-256 to their
declared pins** (payload 157,782 B = the accepted corpus);
helper literals byte-equal the staged ASCII python helpers in both
packs; six V1 pin tokens present in both.

## §5 — Sanctioned-mutation statement

Exactly one schema mutation: `alembic upgrade → 20260903_0047` on the
target file. File-landing writes: the 17 delivered files (14 new + 3
cumulative overwrites with pre-write backups). Evidence writes:
transcript, anchor, backups, state records under `operator-evidence\BE-7`.
No Git operations. No credentials anywhere. Operator return channel:
`0047-APPLY-RUN-V1.txt` + `0047-VERIFY-RUN-V1.txt` (state records remain
in place).

— ITRGA-PLAN-V2-0047-APPLY-001 · v1.0.0 · 2026-09-04 (Africa/Nairobi)
