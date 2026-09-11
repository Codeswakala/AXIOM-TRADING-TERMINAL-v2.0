# REQ-V2-BE-10-001 — BE-10: SIGNAL-AGAINST-ACCOUNT INTELLIGENCE
`STATUS: FOR ADJUDICATION — 2026-09-06 — ITRGA vs OPERATOR — successor to BE-9 (now OPERATING)`

## R-0 — Mission
Answer, at any moment, one operator question with provenance:
**"What do my current signals say against what I actually hold?"
A read-only analytics band joining the BE-9 broker-read projection
(positions / balances / orders / fills) to the existing signal &
chart-intelligence engines. Zero execution verbs. Zero broker writes.
Pure intelligence surface.

## R-1 — Scope declarations
R-1.1 (IN): join of live-ish broker projection (last complete sync basis)
against signal_engine outputs for the instrument universe on file
(319 practice-book permissions witnessed at BE-9 closeout).
R-1.2 (IN): per-instrument alignment verdicts — e.g. held-long vs signal-up,
held-flat vs signal present, held vs no-signal — with staleness banners
carried end-to-end (Q7 law generalization from BE-9).
R-1.3 (OUT): any order verb, any sizing recommendation phrased as action,
any autopilot behavior. The band SPEAKS analysis; it never prescribes trades
(the paper bridge is a future band's spoils).
R-1.4 (OUT): new broker contact — BE-10 consumes the projection only
(N2/N4 generalization: BE-10 never touches MetaTrader, never the vault).

## R-2 — Prior-art reuse law (BE-9 precedent standing)
- Inputs ride BE-9 tables via the frozen broker_read CONTRACT — no new
  broker leaves, no shadow copies, no re-fetch paths.
- Envelope, provenance, staleness, fail-closed posture: inherited
  verbatim from BE-9 design laws (S2/S4.3/S9/Q7/Q9 analogs apply).
- computation_version gains ONE new component row for the join engine
  (name/version/SHA frozen at design; current 11-row set otherwise byte-stable).

## R-3 — Behavioural requirements (testable or it doesn't ship)
R-3.1: Given a complete sync basis B and signal set S(B) reproducible from
pinned bodies, the verdict for any instrument is DETERMINISTIC — same (B,S)
in, same verdict out (S4.3-class canon law).
R-3.2: Missing basis (no complete sync ever) → verdict surface refuses with
typed refusal (no_data), never synthesizes (fail-closed, E1-law class).
R-3.3: Stale basis (>24h, BE-9 _staleness law) → surface answers with the
explicit banner; never silently fresh.
R-3.4: Zero writes to any broker_* table from this band's codepaths —
structurally enforced (C3-class zero-verb scan, band census asserts).
R-3.5: Signal absence ≠ signal presence-of-opposite. FLAT basis and
NO-SIGNAL are distinct, named states in the taxonomy (enumeration law).

## R-4 — Surface sketch (design refines; REQ pins only the floor)
- One OR two new GET reads under the v2 router (envelope-inherited),
  permission-gated on a NEW v2.account_context.read-class permission
  (RBAC law: new verb requires new persm, seeded by migration).
- Flagship read: account-context alignment matrix for the held/account
  universe with per-row {instrument, posture, signal, alignment, basis_age}.

## R-5 — Budget & census laws
- Migration floor: exactly ONE new migration band (00xx) adding: join-engine
  compver row, new permission(s), any derived-materialization tables the
  design justifies (none assumed a priori — design decides).
- Band census: trigger/permission/compver counts recomputed at closeout;
  suite floor = 1,077 + new tests; register tattooed 22-pin corpus extended
  only by design-stage pins.

## R-6 — Findings & constraints inherited (lawful inheritance, not folklore)
- Investor posture law (F-E1-02 directive): any BE-10 consumption assumes
  projection produced under investor session; health assertion carriers.
- No-plaintext-secret law restated: passwords only at no-echo prompts.
- Enumeration-not-literals law (P-2): any sha comparisons enumerate fresh.
- Transcript/codec sovereignty: witness files decode by content.

## Adjudication request
Operator rules: ADOPT / AMEND / REFUSE each section. On ADOPTED, ITRGA
proceeds to DESIGN (DR-V2-BE-10-001) with the same six-question discipline
used through BE-9. Standing rule: nothing is designed, and certainly
nothing is built, beyond an unfrozen REQ.
