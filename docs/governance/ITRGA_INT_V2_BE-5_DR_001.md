# ITRGA-INT-V2-BE-5-DR-001 — Delivery-Report Intake Review & Correction Items: AXIOM-V2-BE-5-DR-001

| Item | Value |
|---|---|
| Reviewer | ITRGA (succession ITRGA-REA-V2-SUCCESSION-001) |
| Date | 2026-09-02 (Africa/Nairobi) |
| Artifact | `AXIOM-V2-BE-5-DR-001` (Delivery Report, 2026-09-02; received via Operator custody channel 2026-09-02) |
| Governing chain | BO-V2-BE-5-001 · AXIOM-V2-BE-5-DA-PLAN-001 v1.0.0 + ITRGA-PRV-V2-BE-5-PLAN-001 (P-1…P-5) · Operator BE-5 authorization 2026-09-02 · Operator full-depth-review standing rule (2026-09-02) |
| Status | **INTAKE REVIEW — DR accepted as face-consistent; band NOT yet determined. Two corrections issued (C-1 mandatory before determination; C-2 mandatory at the working-DB application act). Evidence package requested. Full source/evidence review opens on receipt.** |

## 1. Intake consistency checks (face-value; all PASS)

- Arithmetic chains exact vs the BO/P-5 pins: triggers 18→24→28 (delta exactly 10); `v2_permission` 27→34→35; `v2_computation_version` 3→4→5.
- Test accounting internally consistent: 24 + 9 + 14 + 3 + 16 = 66 new; 789 + 66 = **855 ≥ 853** floor pin; fail-first order stated with a concrete evidence note (module-import failure preceded `decisions.py`).
- Pins P-1…P-5 each explicitly addressed (§4), with honest disclosures (backlink nuance, band-declared freshness bounds, withheld-state emitter absence declared debt-class).
- Drift claims match the ITRGA's own empirical format map (head-satisfied → itemized 9 distinct tokens; non-head 0044 → revision-offset form; PGF-014 cited correctly).
- Register discipline: maturity rows moved to IMPLEMENTED only, COMPLETE expressly left to the determination — correct custody of the determination right.
- Data-honesty spine present: 6-class taxonomy, first-landing restriction, pipeline-validation tier, no market claim anywhere.

Face-consistency is a gate, not acceptance (report existence necessary, never sufficient — 07_ML_SPEC discipline). The determination review requires the evidence package (§4) and the C-1 correction (§2).

## 2. Correction C-1 (MANDATORY before determination): `superseded_by` vocabulary inversion

The P-1 pin specified `superseded_by String(36) NULL` ("id of the superseding record row") — a **forward link**. I own the inconsistency in that wording: under full immutability the predecessor row can never be mutated, so a forward link is writable only at row creation when no successor yet exists; the pin as literally drafted was unimplementable in its letter. The DA implemented the only coherent mechanism — a **successor-side backlink**, currency = greatest `record_seq` — and disclosed it honestly (DR §4 P-1, limitation 1).

The mechanism is ACCEPTED. The vocabulary is NOT: a column named `superseded_by` on the successor holding its predecessor's id reads as "this row is superseded by <predecessor>", the opposite of fact. In an immutable institutional schema this is a permanent false-reading hazard, and the correction window is NOW — migration 0044 has been applied only on DA test chains; after the future working-DB application it becomes permanent.

**Required correction:** rename the column `superseded_by` → **`supersedes`** (String(36), NULL) in migration `20260902_0044_v2_be5_ml_governance.py` (content unchanged: successor holds the superseded predecessor's id), update every model/test/projection reference, re-run the full suite (855), and re-ship the evidence manifests affected (source transcript hash manifest will change accordingly; DR updated to v1.0.1 noting this single-column rename as the only schema change). Scope is deliberately one column name: no constraint, semantic, or test-count change is requested.

## 3. Correction C-2 (MANDATORY at the working-DB application act): compver provenance extension — no re-delivery needed now

The DR discloses that the 0044/0045 migrations hash the engine files **from disk at upgrade time** to seed `v2_computation_version.source_hash`. Honest and functional — and it makes migration output machine-dependent, departing from the 0043 determinism discipline (literal pinned values, ITRGA-recomputed). This is accepted for the test chain **with a packing requirement**: at any future sanctioned working-DB application of 0044/0045, the apply instrument's provenance layer MUST pin the six engine files (three per package) by hash before upgrade and MUST assert post-upgrade compver content against those exact pins (the 0043 provenance/check pattern, extended from migration-file pinning to engine-file pinning). Required to be stated in the application-act scope assessment when its time comes. No migration change — the pinning lives in the instrument, not the migration.

## 4. Evidence package required for the source/evidence review

The DR cites three artifacts (DR §6) that did not accompany the delivery:

1. `docs/evidence/V2_BE-5_SOURCE_TRANSCRIPT.md` — REM-001 literals, 15 new + 4 modified files, SHA-256 manifest, reused-V1 hash pins. *Review use:* file-set verification vs the OBS-1 enumeration; full code review of the migrations (DDL/triggers/seeds), the decision engine (ladder, refusals, spec citations), the signal writer, and the test modules; independent recomputation of claimed hashes where feasible.
2. `docs/evidence/V2_BE-5_API_TRANSCRIPT.txt` — Level I executed transcript incl. the 10 inline ASSERTs and the drift direct runs at both heads. *Review use:* terminal-state runtime proof vs T-1…T-12.
3. `docs/evidence/V2_BE-5_TESTRUN_TRANSCRIPT.txt` — raw `pytest -v`, 855/855. *Review use:* executed-floor proof, module counts (24/9/14/3/16), fail-first trace where visible.

The DR gives **truncated 8-hex md5 prefixes** (`f80c5939…` etc). Truncated hashes cannot pin identity — transmit **full MD5 and/or SHA-256** for each artifact; irrespective, the ITRGA recomputes on receipt and any mismatch voids the item reviewed.

## 5. Disposition

- DR: **face-consistent; review OPEN.** Not a rejection — no roadmap/design violation detected at intake, and the DA's disclosures are of the honest class the programme rewards.
- Determination `ITRGA-DET-V2-BE-5-FINAL-001` is rendered only after: (i) corrected DR/evidence satisfying C-1; (ii) the evidence package (§4) verified; (iii) full-depth source review of the migration/engine/test/test evidence against T-1…T-12, the REQ checklist, and P-1…P-5.
- Working-DB application of 0044/0045 remains an unopened, separate sanctioned act (C-2 recorded for its scope assessment).

— ITRGA, 2026-09-02. We don't guess. We prove.
