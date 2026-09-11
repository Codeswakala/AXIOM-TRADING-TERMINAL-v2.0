# ITRGA_ASSESSMENT_V2_0046_APPLY_SCOPE_V1 — Scope assessment + commissioning record: 0046 working-DB application act

| Item | Value |
|---|---|
| Date | 2026-09-03 |
| Commission | Operator's directive 2026-09-03 ("lets proceed with 0046 working-DB application") |
| Instrument contract | Fixed in `ITRGA-DET-V2-BE-6-FINAL-001` §7.3 (restated fully below) |
| Delivery lineage applied | `AXIOM-V2-BE-6-DR-001` v1.0.1 + Rev-2 evidence (hash-pinned in `ITRGA-DET-V2-BE-6-ACCEPT-001` §3) |

## 1. Exact sanctioned scope

Apply alembic chain **one step** on the working lineage (`backend\axiom_dev.db`, operator machine): `20260902_0045` → **`20260903_0046`** (migration `backend\alembic\versions\20260903_0046_v2_be6_portfolio_research.py`, manifest SHA-256 `1e95ce499ec…52156962`). Executed exactly once, by the Operator console, under the ITRGA-issued instruments only. **Nothing else**: no second revision, no app restart during the window, no manual SQL, no Git, no other file touched.

Deliverables to land: 2 tables (`v2_portfolio_definition`, `v2_portfolio_risk_report`), 4 guard triggers, 6 permission grants, 1 compver row, 0 data seeds — with pins **triggers 32 · permissions 41 · compver 6 · drift = the 9 inherited V1 tokens, zero BE-6 tokens · prior V2/V1 state byte-exact**.

## 2. Instrument contract (the accumulated discipline)

1. **REM-Rev-2 literals as the recompute source**: all 11 new + 4 modified files re-pinned by SHA-256 pre-upgrade (the 15 manifest hashes I already proved byte-consistent with the literal bodies).
2. **Provenance closed loop (C-2 law):** the four engine files pinned pre-upgrade; post-upgrade compver row asserted equal to runtime recomputation on the machine AND to the ITRGA-side pin — pre-computed from the literals to:
   `pre-1.0.0 portfolio_risk_engine source_hash = 5c6d8f08809680506694032a5580616d6e15c13ecfa7a59a1d4a0fd869cec90a`
3. **Behavioral proof, never catalog guesswork:** `uniqprobe` insert-duplicate-refuse-rollback for both UNIQUE anchors (`(portfolio_id, record_seq)`; the determinism triple); live INSERT→UPDATE/DELETE probes firing all 4 guard messages verbatim; behavioral CHECK probes (single-value `basis` refusing foreign inserts; six-state `status` CHECK refusing; `basis_label` single-value refusing).
4. **Census pins itemized:** 32 trigger names (28 inherited + 4 added, delta-proven); 41 permission rows with the 6 new grants content-exact; 6 compver rows (5 prior content-exact + new row pinned as §2.2); both new tables present and empty.
5. **No-touch digests:** BE-3 provider rows, BE-4/BE-5 compver content, and the 28 prior triggers name-exact; prior guard messages spot-refused; BE-5 tables observed (rolling counts recorded — operational use after the 0045 record is lawful, so counts are RECORDED, not gated; see §3 anchor policy).
6. **Chain/drift:** pre-state exactly `20260902_0045 (head)` single head; post-state exactly `20260903_0046 (head)` single head; drift at the new head itemized = 9 inherited V1 tokens, zero BE-6 tokens (no `v2_portfolio*` or new-index tokens may appear).
7. **Tri-binding rollback anchor**, integrity/journal/sidecar checks, final size + SHA-256 **RECORDED only** (never pre-asserted — the PGF post-hash non-determinism rule).
8. **Fail-closed everywhere**; `sqlite_master` name-scoped introspection only (PGF-015 grammar); provenance reads never on forbidden catalog columns.
9. **Simulation-before-production**: both instruments exercised against a reconstructed simulator first (pack validation must execute the embedded probe helper and every SQL string the pack sends — the PGF-015 coverage law); a pack is issued only after its own validation transcript is green.
10. Chain-of-custody: independent SHA-256 index on all packs; Operator-run transcripts returned and re-hashed by the ITRGA before any verdict; no commits by DA or ITRGA anywhere.

## 3. Pre-act disclosures and anchor policy

- **Operational write since the 0045 record:** the post-BE-5 application restart created the dev bootstrap operator row (documented at the 0045-era ACCEPT addendum; sanctioned app behavior, authenticated dev escape hatch). Consequence: the working DB no longer byte-equals the 0045-verify closing hash — the **anchor is therefore as-is** (captured at the apply instrument, tri-bound to what it captured), and the inherited guard rails are the *protected V2 objects* (compver contents, permission roster, trigger registry, inherited guard texts, inheritance lineage), which the restart does not touch.
- **BE-5 business tables** (`v2_ml_*`, signals, diagnostics): RECORD-only counts pre/post. Empty-or-not is operational state; the no-touch proof is their definition/registry state, which the assertive census covers.
- **Precondition of record (transmitted to the Operator):** application **stopped** before pack 1 starts (kill the uvicorn/terminal process) and **not restarted** until pack 2 (verify) prints its closing verdict — the 0045-era restart-before-verify ordering administered identically (the restart comes after).

## 4. Act sequence (as established in 0043/0045)

1. ITRGA authors the apply instrument + verify instrument for 0046-gate adaptation; local simulation on a reconstructed database at 0045-plus-0046 state; pack AST/py_compile/functional validation green; pin packs (MD5 + SHA-256).
2. **Issuance note** (instrument register, pins, run contract, evidence envelope, expected PASS profile) → Operator.
3. Operator runs the apply instrument → returns its transcript → ITRGA re-hashes and fully reviews; only then is the verify run authorized.
4. Operator runs the verify instrument → returns transcript → ITRGA full-depth review of both + independent recomputations → **act determination** (gate-by-gate; verdict; the band correction register updated).
5. On PASS: app restart permitted; register update of the working-lineage state (DA-owned content, ITRGA content-supplied); the BE-6 chain then terminates wholly.

**INSCRIBED as `ITRGA_ASSESSMENT_V2_0046_APPLY_SCOPE_V1`. No code yet authorized to touch the working DB — only the instruments, when issued.**
