# ITRGA DETERMINATION — V2 BE-5 Working-DB Application Act (0044+0045)

- **DETERMINATION_ID:** `ITRGA-DET-V2-0045-APPLY-001`
- **Date:** 2026-09-02
- **Act:** band BE-5 working-database application on the Operator's machine (`backend\axiom_dev.db`), single sanctioned mutation `alembic upgrade 20260902_0045`.
- **Instruments:** `ITRGA-V2-0045-APPLY-PACK-V1` (run-of-record), `ITRGA-V2-0045-VERIFY-PACK-V2` (resumption instrument, per `ITRGA-ISS-V2-0045-PACKS-002`).
- **Evidence envelope received:** `0045-APPLY-RUN-V1.txt` (SHA-256 `747123cd…57508` — recomputed by the ITRGA from the returned file, identical to the value recorded by the verify run on the Operator's machine) and `0045-VERIFY-RUN-V2.txt` (SHA-256 `dc2fccb1…ac50c`).

## 1. Verdict — C-2: **CLOSED**. T-1/T-2: **LANDED** on the working lineage.

The working database carries the BO-V2-BE-5-001 terminal state, proven on the artifact itself (Level I on the working DB):

| Gate | Evidence |
|---|---|
| Revision exactly `20260902_0045` (single head) | Apply run A4/A5.1 + V2 verify B2/B0g |
| 28 v2 triggers, set-difference exactly the ten BE-5 guards, 18 inherited intact | Apply A5.2 (executed in the apply run); V2 B5 full name listing re-verified |
| Ten BE-5 guard messages verbatim, on the working DB | V2 B7 (ten transactional probes, rolled back) + inherited compver guards intact + two CHECK-vocabulary refusals |
| Five tables; `record_seq`/`supersedes`/`model_type`/`instrument_class`; `updated_at_event_id` absent; determinism-anchor columns | V2 B5b DDL pins |
| **P-1 and P-2 uniqueness anchors** | V2 B5b **behavioral** probes: `UNIQUE constraint failed` on (model_artifact_id, record_seq) and on (model_artifact_id, inputs_hash, engine_versions_hash) |
| Six indexes exact-named | V2 B5b |
| compver exactly 5 rows; evidence_ref exact; **mge/sge hashes == runtime recomputation** (`mge 83e73e24…9dcff`, `sge dd1f308e…ee439`) | V2 B4 |
| Permissions: 8 additive BE-5 content-exact; total 35; zero duplicates | V2 B5 |
| All five BE-5 tables empty (pre-restart state) | V2 B5/B7 re-asserted after probes |
| Inherited BE-1…BE-4 untouched | V2 B6: provider/history/audit content-exact; BE-4 report digests pinned to the apply run's pre-apply captures (both `4f53cda1…02b945`) |
| Drift = exactly the 9 inherited V1 tokens, **itemized at head**, zero BE-5/V2 tokens | V2 B9 (full itemized output preserved in transcript) |
| No authority variable present; no credential used; serverless | Both runs' A0d/B8/B0d |
| Rollback pre-image bound: 0043 record POST (`947684f2…696a`) == anchor copy == Tier-1 baseline | Apply A0b/A1.2/A2; V2 B0e |
| Final file posture: integrity ok; journal delete; no sidecars; size 1,445,888; SHA-256 `8d0e5a36…578ab0` (recorded) | V2 B10 |

## 2. Incident record — PGF-015 (instrument defect; not a delivery defect)

The apply pack V1 completed the mutation and terminally verified A5.1/A5.2, then aborted fail-closed at probe A5.3 which queried the non-existent `sqlite_master.origin` column. Classification: **ITRGA instrument defect**. Recovery per `ITRGA-ISS-V2-0045-PACKS-002`: a resumption VERIFY pack V2 with the PGF-015 correction (behavioral uniqueness proofs; index introspection by name only; tri-bound pre-image instead of the never-written state record). The application's tie-out and DB state were never implicated. Canon: *PGF-015 — prove UNIQUE anchors behaviorally; `sqlite_master` has no `origin` column.*

## 3. Independent ITRGA corroboration beyond the transcripts

- Apply-run transcript hash recomputed from the returned file == value recorded by the verify run on the Operator's machine — chain of custody intact.
- **Closed-loop code authenticity:** the mge/sge source hashes recomputed by the ITRGA from the REM-001 transcript literals (in this workspace) equal the Operator's runtime recomputation — the reviewed code, the on-disk code, and the compver provenance rows are one and the same bytes.

## 4. Record effects

- Correction register: **C-1 CLOSED (delivery); C-2 CLOSED (this act)**. The BE-5 correction chain is empty.
- `BO-V2-BE-5-001` terminal state T-1…T-12: complete on both evidence planes (Level I/II in-band; Level I on the working DB). The one remaining Level-II-on-working-lineage item (in-band suite on the working stack) stands per the DA's executed evidence; nothing further is owed.
- The Operator may restart the application (the V2 pack's verdict line already releases it).
- Next governance steps (already recommended in `ITRGA-DET-V2-BE-5-FINAL-001` §7): final acceptance authorization → registry synchronization Rev 13 → file placement per DR §9.1 → close `BO-V2-BE-5-001`. Maturity rows `02-MACHINE_LEARNING_PREDICTIVE` (6-ML) and `03-SIGNALS_STRATEGY` (4-SIGNAL) → COMPLETE stands recommended.

**ISCRIVED as DETERMINATION `ITRGA-DET-V2-0045-APPLY-001`.**
