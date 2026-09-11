# ITRGA REVIEW — BE-8 DESIGN (AXIOM-V2-BE-8-DESIGN-001 v1.0.0)
# ITRGA-REV-V2-BE-8-DESIGN-001 · v1.0.0 · 2026-09-04
# Artifact reviewed: AXIOM-V2-BE-8-DESIGN-001.md — 31,541 B — sha256
# ad72f3c472cb7fe1cb13a0b16d92d518e0900b001179f9f30f49a5b668debccc
# VERDICT: **SUBSTANTIVELY SOUND. TWO CLARIFICATIONS REQUIRED (C-1, C-2)**
# **TWO STANDING-LAW DECISIONS RULED (D-1 approved-scoped; D-2 approved).**
# Path: DA returns a v1.1.0 amendment answering C-1/C-2 -> ITRGA verifies ->
# DESIGN ACCEPTED. No code, no migration until acceptance (zero-code stands).

## §1 — Compliance with ITRGA-REQ-V2-BE-8-001 (complete)
- All 13 mandatory sections present (+§0 thesis, §14 honesty register, §15
  assumptions). Every roadmap scope bullet explicitly mapped (S1.1 tail).
- §2 controls honored: N1 (zero credentials — structural absence, S6.3),
  N2 (no adapter interface anywhere + frozen single-entry registry +
  typed seam + 10-row attack table, S6), N3 (mode/actor/account/correlation/
  idempotency on the intent; risk decision + audit lineage by FK/ledger, S3
  tail), N4 (single-value CHECK `('paper_simulated')` — the schema CANNOT
  express broker provenance, S4.4 — the strongest form we have shipped).
- §3 precedent law cited and correctly reused (envelope/errors, status-
  transition governance, replayable-snapshot price law, BE-7 queue/anchor/
  reused/time-basis patterns, PGF-021 environment law).
- §5 evidence plan mapped E1–E5 with concrete inventories; OBS-E (fail-first
  transcript) designed-in. §6 open questions ALL answered with rationale.
- §7 process honored: zero code, zero register mutation.

## §2 — Full-depth technical assessment (sound elements of record)
1. Data model: 8-table parallel `v2_paper_*` domain; zero-UPDATE regime
   (derivation law: current state = max event_index to_state) — the event-
   ledger discipline is exactly right for an order-lifecycle domain and
   stricter than any prior band; 16 guard triggers; census arithmetic
   42→58 / 49→57 / 8→10 internally consistent with the 0047 registers.
2. Exactly-once risk evaluation as a SCHEMA FACT (uq(intent_id) on
   v2_paper_risk_decision) — measured, not conventional; same class as the
   N4 fill-class wall. Idempotency anchor uq(account_id, idempotency_key).
3. Determinism: replay contract `(intent + snapshot hash + cost model +
   engine version) -> byte-identical ×3`, snapshot content re-verification
   before execution, full-precision TEXT-decimal money with presentation-
   only rounding, genesis-recompute reconciliation with PGF-012 content
   comparison.
4. Sealed routing: no ExecutionAdapter ABC "for later" — explicitly and
   correctly rejected as the substitution surface N2 forbids; frozen
   MappingProxyType registry; typed PaperOrderIntent-only entry.
5. Honesty: standing-law amendments DECLARED at the points they touch
   (mode vocabulary; permission-marker guard), each with narrowest-scope
   proposal and both-arms tests; assumptions register bounded.

## §3 — CORRECTION C-1 (required; mechanism at the hold/confirmation seam)
Sections S2.1, S2.2, S3, S6.4-row-8 and S7.2 are mutually under-specified
at exactly one seam. Facts as written: (i) decisions are immutable and
uq(intent_id) — one row per intent; (ii) the executing-transition writer
"requires the pass decision row"; (iii) `risk_hold` resolves ONLY by
operator confirm/cancel; (iv) confirmations consume a "single-use"
confirmation_ref — but nothing defines the mechanics of consumption.
The gap: when `risk_hold -> risk_passed` is confirmed, NO second decision
row may be written (uq). The executing-writer precondition must therefore
be restated precisely, e.g. as a DERIVED rule: decision='pass'
OR (decision='hold' AND a confirm event citing the exact
confirmation_ref exists). Specify ALL of the following in v1.1.0:
a) the executing-writer full precondition rule (derived, event-ledger
   based, single rule text — no duplicated logic between writers);
b) confirmation-ref lifecycle: creation, storage (NOT NULL columns),
   what "consumed" means structurally (derivable from the append-only
   ledger — preferred — no mutable marker anywhere), and the typed
   refusal on double-confirm / wrong-ref / stale-ref after cancel;
c) the exact event rows + audit events each confirmation act writes
   (class names), including hold->cancel;
d) how `risk_block` remains unreachable by any confirmation (typed
   terminal, no path — assert in tests both arms).
This is the one seam where E3's hold->confirm / hold->cancel tests could
otherwise not be authored deterministically. Fix by specification, not code.

## §4 — CORRECTION C-2 (required; wording precision)
S3's "pass/block are final" is ambiguous against the hold-resolution path
in S2.2. Replace with the exact intent: "decision rows are immutable and
exactly once; `block` is terminal with no confirmation path; `hold`
resolves only through the S7.2/C-1 confirmation mechanism; `pass` is the
only decision that can reach `executing` (possibly via the derived rule
C-1a)." One paragraph amendment; no structural change intended.

## §5 — DECISION D-1 (permission-marker scoped exemption): **APPROVED**
The BE-1 forbidden-marker law ('account','order','margin','position')
collides with the legitimate `v2.paper.*` domain vocabulary. The proposed
amendment — the guard exempts EXACTLY permissions with the prefix
`v2.paper.` and continues to reject the markers in every other namespace
— is the narrowest lawful form and keeps the anti-live-vocabulary wall
standing (live still cannot exist to be named). SANCTIONED with these
binding conditions: (i) the exemption is a single literal prefix test
(`v2.paper.`), nothing broader; (ii) tests assert BOTH arms, including a
negative (`v2.research.order.*` must die) and a boundary (`v2.paperwork.*`
must die); (iii) the amendment is recorded in the permission-contract
comment and the register line at BO.

## §6 — DECISION D-2 (VALID_MODES += "PAPER"): **APPROVED**
The mode contract defers PAPER to BE-8 by its own text; this design is
that act. Sanctioned as the narrowest extension: VALID_MODES becomes
("RESEARCH","SIMULATION","PAPER"); LIVE remains refused/deferred; paper
writers require mode=="PAPER" explicitly with typed refusal and the
negative-mode tests in S11/E4 carrying the proof.

## §7 — Non-blocking observations (register for BO, no action now)
- S5 average-cost P&L + USD single currency + presentation-only rounding:
  registered assumptions (A-1..A-5) accepted as v1 scope; FIFO/multi-
  currency stay debt.
- Test budget ~70 (new floor ≈ 972+70 at BO; exact count fixed at BO).
- `time_in_force` single-value 'replay_window' + manual `/run` invocation:
  coherent with Q3/Q4 determinism answers (they are the same decision).
- 0047 drift-test generational scoping at 0048 head: established law, cited.

## §8 — Next step
DA: return AXIOM-V2-BE-8-DESIGN-001 **v1.1.0** = the v1.0.0 text with the
C-1 specifications (a–d) and the C-2 paragraph folded in, a change-note
listing ONLY those edits, and the amended file's sha256 in the delivery
note. ITRGA verifies the two clarifications against the change-note; on
pass: **DESIGN ACCEPTED**, and the CN/PLAN track for implementation
opens (no code before BO).

**We don't guess. We prove.**
— ITRGA-REV-V2-BE-8-DESIGN-001 · v1.0.0 · 2026-09-04
