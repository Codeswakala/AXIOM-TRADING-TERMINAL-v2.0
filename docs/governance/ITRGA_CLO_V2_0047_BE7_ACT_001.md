# ITRGA CLOSURE RULING — BE-7 0047 WORKING-DB APPLICATION ACT
# ITRGA-CLO-V2-0047-BE7-ACT-001 · v1.0.0 · 2026-09-04 · AXIOM Trading Terminal v2.0
# Office of the Independent Technical Review & Governance Authority (ITRGA)
# VERDICT: THE ACT IS CLOSED. THE CHAIN IS COMPLETE, BYTE-PROVEN END TO END.

## §1 — Final machine ledger of record (operator box, all recomputed live)
- Working DB: backend\axiom_dev.db at 20260903_0047, single head.
  Post-mutation sha256 (witnessed PRE==POST across 3 read-runs):
  27bda3112e53baf426604532da4d5f44ef0c4d089c0f002e08d0ab9b740c776f
- Anchor (pre-mutation snapshot) intact:
  operator-evidence\BE-7\0047-ANCHOR-axiom_dev.bak
  sha256 5bd60aff6ab2d7fb6889b60363653b1d5e95d4405f15c0a7220a649ed233e795
- Censuses: 42 triggers / 49 permissions (+14 BE-7) / 8 compver members;
  RPE 1499343d…b178 (unchanged law), RJE 8f107d17…0598 (new literal).
- Delivered files: 17/17 byte-pins + 6/6 V1 pins — exact on every run.
- Guard probes: all ten immutability triggers refused live with exact
  contract messages, twice independently (apply-resume 16:00Z, verify 17:56Z).
- Suite: 972 passed / 0 failed (twice: 1,575.03s and 1,177.17s).
- Drift gate (PGF-014): alembic check nonzero-exit, zero band/v2 tokens,
  inheritance witness audit_write_failure_records — the pre-0042 V1
  baseline as declared in the BO. (The "FAILED: New upgrade operations…"
  block in transcripts is alembic's stderr for that nonzero exit — expected.)
- State records on disk (canonical, 13/12 clean KEY=VALUE lines):
  0047-APPLY-FINAL-STATE.txt (STATE_FILE_ID …-V4, UTC 16:28:07Z)
  0047-VERIFY-FINAL-STATE.txt (STATE_FILE_ID …-V5, UTC 18:16:33Z)
- Instrument editions of record (closure pair):
  APPLY_RESUME ed-3  MD5 BA6565C3A1048759FC4E896BB3323806
  VERIFY V5 ed-5     MD5 97581F0E57F80CF17053A9CB09893712
  BASELINE_PINS      MD5 32F9270B1B56E9A9B78A0501FD8A6F80
- Correction branch (CB-001): corrected test file landed and live-proven,
  sha256 84ac22435a73f402274c508edc31a657fb2424a49ea659f0164c18ed8257000b;
  acceptance ITRGA-ACC-V2-0047-SUITE-ISOLATION-CB1-001. DEF-BE1-05 green on
  the mandated dist-present environment.

## §2 — Ruling
1. The BE-7 band's working-DB application act (migration 20260903_0047) is
   PROVEN COMPLETE on the mandated operator environment: mutation witnessed,
   re-proven twice by pure-read instruments, verify chained and clean.
2. The application may be RESTARTED and the terminal returned to normal use.
3. Both instruments now refuse reruns by design (apply-record + verify-record
   exist) — any such refusal is standing proof of completion, not a fault.
4. Required evidence return: 0047-APPLY-RUN-V4.txt, 0047-APPLY-RESUME-RUN-V1.txt
   (16:00Z run), 0047-VERIFY-RUN-V5.txt — attach for archive; closure
   contingent on receipt of the three transcripts.

## §3 — Statutes added to the ITRGA review battery this act
PGF-020 (probe SQL must be validated against embedded DDL; offline replica
proof pre-issuance), PGF-021 (filesystem-conditional behavior screening;
operator-terminal ≠ CI environment), PGF-022 (per-line anchoring for output
containment; '^' binds a joined string's start; quiet/non-TTY forms must be
shape-proven on real captures), PGF-023 (parenthesize every concatenated
element inside @(...) — comma binds before binary +; writer blocks proven by
round-trip), PGF-024 (cross-instrument sweep: any content correction
duplicated across live instruments is verified byte-equal pre-issuance),
plus execution-card law (cards must never instruct locking files an
instrument owns; no Start-Transcript onto pack-owned transcripts).

## §4 — DA register-sync content (DA owns the registers; exact text below)
In V2_CURRENT_STATE.md (next version, operator approves):
- Row: BE-7 | status ACCEPTED -> **OPERATIONAL (DB applied & verified
  2026-09-04T18:16:33Z; ITRGA-CLO-V2-0047-BE7-ACT-001)** | working DB
  20260903_0047 | RPE 1499343d… / RJE 8f107d17… | suite 972/0 (x2).
- Close line: ITRGA-CB-V2-0047-SUITE-ISOLATION-001 = RESOLVED (test fixture
  isolation only; zero product change; OBS-E closed by
  V2_BE-7_CB1_FAILING_RUN_WITNESS.txt, 3,258 B, sha 9b0fef58…).
- Statute register: append PGF-020..PGF-024 summaries per §3.
- Note for future issuance: VERIFY V5's missing-record throw text cites
  "APPLY_PACK_V4" (stale pre-RESUME wording; cosmetic, no re-issue).

## §5 — Parking-lot (post-closure; backlog items for future BOs)
- Screen future deliveries against PGF-020..024 (battery harness exists).
- Machine-conditional regression guard for the frontend/dist SPA catch-all:
  consider moving test isolation to a path-pattern route filter (advisory
  note already in ACC-CB1 §4).
- Migration consolidation remains a BO-planning topic (reduces single-migration
  pack churn); manual alembic-by-hand requires explicit BO amendment.

**We don't guess. We prove. The act is closed.**
— ITRGA-CLO-V2-0047-BE7-ACT-001 · v1.0.0 · 2026-09-04
