# ITRGA ASSESSMENT — 0043 WORKING-DATABASE APPLICATION ACT · SCOPE

Assessment ID: `ITRGA-ASS-V2-0043-APPLY-001`
Date: 2026-09-02
Authority: `AXIOM-V2-OD-BE-4-009` (recorded 2026-09-02)
Chain position: stage 1 of the 0043 application act (scope) — no pack is issued by this assessment; no execution is authorized by this assessment.

## 1. Subject

Apply migration `20260831_0043_v2_be4_research_read_models` (BE-4; approved; hash-verified in the Operator repository) to the application's working SQLite database, as a single sanctioned mutation, followed by a read-only verify act. Pattern: the BE-3 P2 transition apply act (`ITRGA-DET-V2-BE-3-P2-TRANS-APPLY-FINAL-001`).

## 2. What the act is — and is not

**Is:** one `alembic upgrade` to revision `20260831_0043` on `backend\axiom_dev.db`, executed by a sanctioned ITRGA apply pack (fail-atomic, MD5 self-check, app-stopped precondition), preceded by a file-level backup anchor and followed by a dedicated read-only verify pack.

**Is not:** a repository change; a Git operation; a delivery act; a provider operation; a modification of any other table/trigger/row; a network call; a credential of any kind. 0043 is **not** a status transition — no authority variable is involved, set, or touched.

## 3. Precondition status — re-pins 0038/0039/0041: **RESOLVED (Level II recomputation, 2026-09-02)**

The OBS-9 residual required re-pinning the three chain migrations without an approved per-file pin before application. ITRGA performed the recompute from the accepted corpus artifacts (approved source transcripts/CA-response deliveries; `## File:` sections; convention: content lines joined with LF plus trailing newline — the convention proven against 0042/0043). All seven extracted sections reproduce their declared SHA-256 exactly (7/7), validating the extraction. Result:

| File | Operator-repo sha256 (Level I, SECTION 3B, runs 3–5) | Approved final content source (document · declared sha256) | ITRGA recomputation | Verdict |
|---|---|---|---|---|
| `20260823_0038_v2_be1_core.py` | `6e071157c204e29bfb1254400f0a4543d776931fa5834723cc497d12a0b8f588` | `V2_BE-3_P2_CA_RESPONSE_DELIVERY-001.md` (BE-3 P2 correction cycle) · declared `6e071157…` | `6e071157…` (reproduced from content) | **VERIFIED** |
| `20260824_0039_v2_be2_marketdata.py` | `bc11cae24cdbe47361454a676604a9f81b1754df47058185dd4c002689ab5b19` | `V2_BE-2_CA_RESPONSE_DELIVERY-001.md` (BE-2 correction cycle) · declared `bc11cae2…` | `bc11cae2…` (reproduced from content) | **VERIFIED** |
| `20260825_0041_v2_be3_p2_entitlement.py` | `d775c34aedac8fffd594f4ac4434f48c9d9cfd2fa88f4d3fd1cf9e7ba278dadd` | `V2_BE-3_P2_CA_RESPONSE_PG-001.md` (BE-3 P2 PostgreSQL cycle) · declared `d775c34a…` | `d775c34a…` (reproduced from content) | **VERIFIED** |

Lineage recorded (explains every previously observed discrepancy — **no divergence; no repository-state defect**):

- **0038:** BE-1 original `34ec444d3a9e…` (`V2_BE-1_SOURCE_REVIEW_PART_1.md`; matches the `V2_BE-1_EVIDENCE.md` manifest) → superseded by the BE-3 P2 correction-cycle version `6e071157…` (222 → 239 lines). This is why git shows `M` for 0038 against the BE-1-era frozen HEAD.
- **0039:** BE-2 original `022e644b21bd…` (`V2_BE-2_SOURCE_TRANSCRIPT.md` manifest) → superseded by the BE-2 correction-cycle version `bc11cae2…` (316 → 325 lines).
- **0041:** BE-3 P2 original `da3ed7c130b5…` (`V2_BE-3_P2_SOURCE_TRANSCRIPT.md` manifest) → correction `4dd261e0d979…` (`V2_BE-3_P2_CA_RESPONSE_DELIVERY-001.md`) → final PostgreSQL-cycle version `d775c34a…` (`V2_BE-3_P2_CA_RESPONSE_PG-001.md`).

**Consequence:** the Operator repository holds the final approved version of every chain file 0038–0043. The re-pin precondition of OD-009 is satisfied **without any external input**. The OBS-9 residual "re-pin 0038/0039/0041 before application" is closed by this record; the remaining OBS-9 item is unchanged (the Operator's one-line accounting of the 2026-09-01 17:26 +03:00 bulk-write operation).

## 4. Already-proven state (Level I, this session; re-verified at runtime by the apply pack)

| Fact | Evidence |
|---|---|
| Working DB in force at `20260829_0042`, byte-identical: 1,310,720 B; last write 2026-08-31 14:09:55 +03:00; sha256 `0483f9fe12e3d71f514811571c64589d72c66ec47fb2a3a1f6e986715ca41006`; 12 v2 triggers; integrity ok; journal delete; no sidecars | verify run 5 (2026-09-02 10:14:47 +03:00, PASS) |
| 0043 in the Operator repository, hash-verified: 10,918 B; sha256 `ab90576203d9f7946154ad4efd7a3d52bc98b91e328dbf2a4dca0b5049bda84b` = approved BE-4 manifest | SECTION 3B (runs 3–5) + `ITRGA-REV-V2-BE-4-DELIVERY-001` |
| Repository head `20260831_0043`; alembic **1.19.0** (summary-format `alembic check`) | SECTION 3B, run 5 |
| 0043 DDL: 3 tables + 2 unique constraints + 3 indexes + 6 deterministic guard triggers (exact R-2 pins) + 5 permission seeds + 3 computation-version seeds; zero references to V1 or BE-1–3 objects; symmetric downgrade | `ITRGA-REV-V2-BE-4-DELIVERY-001` (approved source review) |
| Expected drift after apply = exactly the 9 inherited V1 tokens (the BE-4 table/index set leaves the drift set) | run 1 itemized observation on the byte-identical predecessor state + 0043 content |
| Anchor pattern, apply-pack pattern, fail-atomic behavior | BE-3 P2 transition apply act (V5) + verify act (runs 1–5) |

## 5. Expected end state (carried into the plan/Build Order as the terminal-state contract)

`alembic current = 20260831_0043` · **18 v2 triggers** (12 inherited + 6 new, exact names/messages per R-2) · tables `v2_computation_version`, `v2_market_context_report`, `v2_chart_intelligence_report` with pinned columns/constraints/indexes · 5 permission seed rows (admin ×3, operator ×2) · 3 computation-version seed rows (`indicator_engine`, `market_context_engine`, `chart_intelligence_engine`) · integrity ok · journal delete · no sidecars · no authority variable involved · drift = exactly the 9 inherited V1 tokens.

## 6. Risk and mitigation

| Risk | Mitigation |
|---|---|
| Mutation of the working DB | Exactly one sanctioned mutation; file-level backup anchor **before** the mutation; fail-atomic pack (abort before mutation on any pre-check failure); DDL transactional on SQLite (failed upgrade rolls back fully); app must be stopped (live-connection precondition in the instruction card) |
| Environment (alembic 1.19.0, new venv since 2026-09-01) | Pack battery (PTN-V2-PACK-001 §2.1) includes a dry-run world replicating the recorded operator environment; the pack asserts `alembic current` = exactly `20260829_0042` pre-apply (abort if already at 0043 or any other state) |
| Wrong file / superseded instrument at the console | PTN-V2-PACK-001 §2.2/§2.5: embedded instruction card with the exact self-check hash and exact file name; superseded instruments marked "do not execute" |
| 0043 file altered in the repository before the run | The apply pack re-hashes 0043 (and the re-pinned 0038/0039/0041) on disk at runtime against the values above; abort on any mismatch |

## 7. Chain status

Stage 1 (scope) **complete**; precondition (re-pins) **satisfied**. Next: plan (instrument design + battery), then Build Order (terminal-state contract), then the sanctioned apply + verify instruments with the full battery. No Operator action is required until the instruments are presented.

— ITRGA, 2026-09-02
