# ITRGA ACCEPTANCE — BE-8 DESIGN (AXIOM-V2-BE-8-DESIGN-001 v1.1.0)
# ITRGA-ACC-V2-BE-8-DESIGN-001 · v1.0.0 · 2026-09-04 · AXIOM Trading Terminal v2.0
# Artifact accepted: AXIOM-V2-BE-8-DESIGN-001.md v1.1.0 — 39,778 B — sha256
# 76e718c42ce6f9ecd58f8281fc9ba41e5500c1e844a4809873adf1531dccc073
# VERDICT: **DESIGN ACCEPTED** (C-1 and C-2 answered in full; D-1/D-2 rulings
# of ITRGA-REV-V2-BE-8-DESIGN-001 stand with their binding conditions).

## §1 — Verification of the two required clarifications (full-depth)
C-1 (hold/confirmation seam) — answered by new S2.6, verified section-by-section:
- (a) executing-writer precondition is a SINGLE derived rule
  (`may_execute(intent)`), owned once, consumed by the transition writer and
  tests: `decision='pass'`, OR (`decision='hold'` AND ledger `hold.confirmed`
  citing the exact ref AND no `hold.cancelled`); all other cases typed refusal.
  The decision row stays `hold` forever — no second decision row can exist
  (uq(intent_id)); effective pass is derivation output. Current-state
  derivation (max event_index) coherent.
- (b) ref lifecycle specified end-to-end: minted exactly once at `hold.issued`,
  stored on the decision row with the iff-CHECK in both directions
  (`confirmation_ref` NOT NULL iff decision='hold'; NULL otherwise),
  consumption = LEDGER-DERIVED fact (no mutable marker anywhere), single-use
  enforced by the append-only uq `(intent_id, event_index)` + writer refusal.
- (c) exact event/audit class table closed: `hold.issued/hold.confirmed/
  hold.cancelled` with from→to rows and audit twins; refused confirmations
  leave the ledger UNCHANGED and audit durably (commit-before-return law);
  four typed refusal classes named (already_consumed, ref_mismatch,
  cancelled, not_confirmable).
- (d) `risk_block` is structurally confirmation-proof: no ref minted (CHECK),
  not_confirmable on attempt, no event class from `risk_blocked`
  (exhaustive-table absence = refusal), both-arms tests incl. forged-append
  refusal and vocabulary content-assertion.
C-2 (S3 wording) — verified verbatim: decisions immutable & exactly-once;
`block` terminal with no confirmation path; `hold` resolves only via S2.6/S7.2;
`pass` the only route to `executing` (directly or via C-1a).
Consequential cross-edits verified where declared (change-note §16): S1.1 row 3
DDL, S2.2 two rows, S6.4 row 8, S7.2 single-mechanism statement, S11/E3
row-exact expectations incl. the four refusal classes and C-1d arms.
Integrity: untouched sections (incl. S13 Q1–Q8, §14 honesty register, §15
assumptions) spot-verified as carrying the v1.0.0 wording — no silent edits.

## §2 — Standing rulings carried into implementation
- D-1 (marker-law scoped exemption): binding conditions — single literal
  prefix test (`v2.paper.`), both-arms tests (`v2.research.order.*` must die;
  `v2.paperwork.*` must die), permission-contract comment, register line at BO.
- D-2 (VALID_MODES += "PAPER"): narrowest form; LIVE remains refused; negative
  mode tests in the E4 inventory carry the proof.
- Assumptions A-1..A-5 stand as BO-phase review surfaces (risk-limit defaults,
  single-operator reality, average-cost P&L, USD-only, ~70-test budget).
- Zero-code rule: no code, no migration, no DB touch until BO amendment.

## §3 — Register & line of record (DA-owned edits; exact text)
In V2_CURRENT_STATE.md (next version): BE-8 row — status **DESIGN ACCEPTED
(ITRGA-ACC-V2-BE-8-DESIGN-001, 2026-09-04)**; baseline head 20260903_0047;
next phase: implementation planning (PLAN) under ITRGA review; DECISION-1/2
conditions carried. REQ line ITRGA-REQ-V2-BE-8-001 = CLOSED.

## §4 — What happens next (phase opening)
1. ITRGA issues the implementation PLAN skeleton (phases: contract/domain
   modules -> migration 0048 plan -> test harness & worked-sample ANNEX-P ->
   integration -> BO for code delivery -> apply/verify instrument pair under
   the PGF-020..024 statutes + CB-001 lesson battery).
2. DA prepares the ANNEX-P worked cost sample elaboration and the concrete
   test-module split inside the PLAN review (no code).
3. Implementation BO follows PLAN acceptance; the working-DB application act
   for 0048 reuses the proven 0047 pack chassis with the new screening laws.

**We don't guess. We prove.**
— ITRGA-ACC-V2-BE-8-DESIGN-001 · v1.0.0 · 2026-09-04
