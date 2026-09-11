# REQ-V2-BE-11-001 — BE-11: PAPER-EXECUTION BRIDGE TO LIVE PRACTICE-BOOK TRUTH
`STATUS: FOR ADJUDICATION — 2026-09-06 — successor to BE-9 (OPERATING) + BE-10 (OPERATING)`
`Register note: band-id offered as BE-11; roadmap execution-family renumbers to BE-12+
at its future commissioning (ruling (b) convention from BE-10).`

## R-0 — Mission
Close the loop your stack has been building toward:
**paper orders sized against the LIVE practice-book state** (BE-9 projection:
balance, margin, held positions) evaluated by the standing
paper_risk_gateway (prg-1.0.0 pinned), and then **reconciled against
broker truth** — the paper ledger's own veracity math against what
the account actually shows after each sync. Everything BE-9/BE-10 brought
home starts earning: paper P&L drift vs broker truth, sized by real balance.

## R-1 — Scope declarations
R-1.1 (IN): consume BE-9 projection basis (positions/balances at last-complete sync),
reuse paper_execution_simulator (pxs) + paper_risk_gateway (prg) engine bodies
(exactly what they are — compver rows already pinned), and write genuine
PAPER-ONLY records: intents, gateway decisions, ledger entries, balance snapshots
(the v2_paper_* standing tables, presently all zero rows on the working DB — survey).
R-1.2 (IN): a paper-vs-broker reconciliation surface (drift math), producing
STATE answers in the BE-10 vocabulary discipline: divergent_state nouns,
never action language (R-1.3 law inherited verbatim from BE-10 REQ).
R-1.3 (OUT): any real order verb anywhere; any terminal contact; any vault
contact; any order SUBMISSION EVEN TO THE PRACTICE ACCOUNT (the practice
account is reached ONLY by BE-9 sync reads; this band never travels the other
direction). Zero broker writes is not relaxed; it is strengthened by the
account-context bridge law (banned-import set grows: no providers, no MT5).
R-1.4 (OUT): fill simulation requiring market-price feeds this band does not have
(candles/universe feeds are a design question to be answered IN THE DR,
defaulting to a conservative projection: intents and gateway decisions only;
fill simulation deferred if evidence does not supply lawful price basis —
fail-closed on insufficient inputs, DR decides, REQ forbids guessing).

## R-2 — Prior-art reuse law
- All inputs from PROJECTIONS (BE-9 law), never contracts/adapters.
- pxs/prg bodies consumed as-is (compver-pinned); the bridge is a THIN join,
  not a reimplementation — census tattoo law inherited (one migration band,
  compver +1 component max, permission floor minimal, zero new tables unless
  design justifies).
- Verdict/taxonomy discipline: inherited BE-10 closed-set law and wording law.

## R-3 — Behavioural requirements (testable or no-ship)
R-3.1: Determinism canon (per-world, per N-O13 law): given basis B, intent
payload, pxs/prg versions → identical gateway decision + ledger math.
R-3.2: Fail-closed arms: no basis → typed refusal; stale basis → banner-carried;
insufficient lawful price basis for any fill simulation → refusal, never
synthesized prices.
R-3.3: Gateway decisions are RECORDS OF STATE with reason codes
(accept-with-notes / deferred / refused-under-policy), never executions —
and the tables' own naming keeps the word FREE of broker-order verbs.
R-3.4: Reconciliation drift answers in state nouns; tolerance bands
explicit, seeded, audited (never defaults hidden in code).
R-3.5: The band cannot place the same ledger entry twice (idempotency law;
attempt-duplicate refusal typed).

## R-4 — Surface floor (design refines)
- POST intents + POST evaluate (risk gateway), GET ledger/positions/drift —
  with RBAC additions in the v2.paper.* namespace already standing
  (D-1/DECISION-1-prefix convention; exact permission set is DR work).
- Zero binding to BE-10 reads beyond vocabulary.

## R-5 — Budget & census laws
- One migration band at design graduation (00xx), census re-tattooed;
  corpus extends only by design/BUILD pins; suite floor = 1,121 + band budget.

## R-6 — Inheritances
Investor-posture law (any downstream sync still investor-only); no-plaintext-secret
law; enumeration-not-literals law (now strengthened to three-layer); transcript
codec sovereignty; file-invoked act scripts; ASCII-only console strings;
interpreter pretense check (N-O12) before any act.

## Adjudication request
Operator rules: ADOPT / AMEND / REFUSE per section. On ADOPTED, DR proceeds
under the six-question discipline, with R-1.4's fill-simulation question as
the DR's FIRST evidence act (a survey of lawful price-basis availability on
the working DB). Nothing is designed beyond an unfrozen REQ.
