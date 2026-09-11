# DA TECHNICAL REVIEW — REQ-V2-BE-10-001 (input to the Operator adjudication)
# AXIOM-V2-BE-10-DA-REQREV-001 · v1.0.0 · 2026-09-06 · AXIOM Trading Terminal v2.0
# Object: REQ-V2-BE-10-001 "Signal-Against-Account Intelligence" (FOR ADJUDICATION)
# Author: Replacement Development Authority (DA)
# Reading rule: the adjudication is the OPERATOR'S (ADOPT/AMEND/REFUSE per
# section). This memo is DA-side technical input only — feasibility, prior-art
# fit, and one register observation. No ruling is made or implied here.

---

## §0 — One register observation the adjudication should settle (flagged, not argued)

**The REQ's "BE-10" is not the roadmap register's "BE-10."** The standing
registers carry:

- Roadmap `AXIOM-V2-BE-ROADMAP-001` §BE-10: **Controlled Live Execution
  Gateway** (order submission under heavy pins);
- `V2_CAPABILITY_MATURITY.md` rows 65–67: `Execution Gateway`, `Order
  Management`, `Position Management` — family Execution, band BE-10,
  state DESIGNED.

The REQ proposes a **read-only intelligence band** in that slot — a
materially SAFER insertion (zero execution verbs, zero broker writes,
zero vault contact) that defers live execution further down the ladder.
The DA has no objection to the substance; sequencing an analytics join
before any execution gateway is conservative and sound. But the register
consequence should be ruled explicitly at adjudication, one of:

- **(a)** renumber/insert (e.g. the REQ band becomes BE-9.5 or BE-10 with
  the execution ladder shifting to BE-11+, AI to BE-12), with a roadmap
  register amendment recorded; or
- **(b)** keep the name BE-10 for this REQ and re-title the roadmap's
  execution band at its future commissioning.

Either is lawful; silence is not — the maturity registry currently maps
BE-10 to execution capabilities, and a closeout under the same label
would collide. (Register discipline, not pedantry: the 22-pin corpus law
and census tattoos key off band ids.)

## §1 — Section-by-section technical assessment (DA feasibility input)

| Section | DA assessment |
|---|---|
| R-0 mission | Sound and buildable. The question "signals vs holdings" is answerable entirely from standing surfaces: BE-9 projections (positions/balances/orders/fills at last-complete-sync basis) × the BE-5 signal registry (`v2_signal` lineage, `SIGNAL_STATES = emitted/withheld/expired/refused`) × BE-4 chart-intelligence reads. No new authority needed |
| R-1.1 IN | Feasible as a pure read-side join. One design question to resolve: the instrument-id seam — BE-9 stores provider-named `instrument_ext_id` (e.g. `EURUSD`), the signal/research lineage uses the V2 instrument registry ids (e.g. `forex.eurusd`). The design must pin an explicit, auditable mapping law (a seeded mapping table or a declared normalization function — never string-guessing). This is the band's only genuinely new risk surface |
| R-1.2 IN | The alignment-verdict taxonomy is enumerable and testable. DA sketch for design: closed verdict set over (posture × signal-state) with `aligned / opposed / unsignalled_holding / signal_without_holding / flat_no_signal / indeterminate_stale` — exact vocabulary is design work, the closure law is the point (R-3.5 honored: FLAT ≠ NO-SIGNAL as named states) |
| R-1.3 OUT | Structurally enforceable with the standing machinery: no order verb in any type/route (BE-9 T-4-class census), no sizing-as-action vocabulary (scan class), refusal-typed surfaces. The "speaks analysis, never prescribes" line becomes a wording-law test on the response contract — the verdict field names describe STATE, never action |
| R-1.4 OUT | Trivially enforceable and the strongest feature of the REQ: no MetaTrader import, no vault import, no new broker leaves — the import-boundary scans from BE-9 invert cleanly (BE-10's banned set includes `providers.exness_mt5`, `vault`, network libs) |
| R-2 | Correct reuse law. The frozen `BrokerReadContract` is NOT the consumption seam though — BE-10 should consume the **projection tables** (read models), not the adapter contract (which contacts the terminal). The REQ's own R-1.4 says exactly this; the R-2 first bullet's "via the frozen broker_read CONTRACT" should read "via the frozen broker_read PROJECTIONS" at design time (wording nit, flagged for the freeze). One compver row (join engine) is the household law — recipe unchanged |
| R-3.1 | The S4.3-class determinism canon extends naturally: verdict digest over (sync_run_id basis + signal-set pins + join-engine version). ×3 attestation testable against fixtures |
| R-3.2/R-3.3 | Both are BE-9 laws generalized; the `_staleness` derivation and `broker.no_data`-class refusal port directly. Banner-carried-end-to-end is a response-contract assertion |
| R-3.4 | Zero-writes-to-broker-tables: enforceable at three layers — no writer routes (GET-only surface per R-4), import scan, and the standing DB triggers already guard all 9 broker tables against UPDATE/DELETE (INSERT-abstinence is the code-scan's job) |
| R-3.5 | Yes — and the design should also name the inverse: signal present + no holding is its own state, not an implied recommendation (ties to R-1.3's wording law) |
| R-4 | One or two GETs under the v2 router is right-sized. Permission: `v2.account_context.read` collides with the `account` forbidden marker — **a third literal-prefix exemption ruling will be needed** (the D-1/DECISION-1 mechanism, `v2.account_context.` with a boundary must-die), OR the design names it inside an existing exempt namespace. Flag it now so it is ruled at design acceptance, not discovered at build |
| R-5 | Consistent with the standing census law. DA notes the a-priori-no-tables posture is right: the flagship matrix is computable at read time from standing tables; materialization needs justifying, not assuming. Suite floor arithmetic: 1,077 + budget |
| R-6 | All four inherited constraints are already encoded DA-side (investor-posture health carrier exists on the BE-9 surface; no-echo law; P-2 enumeration; codec sovereignty) — nothing new to build for inheritance, only to not-break |

## §2 — DA readiness statement

If adjudication ADOPTS (with the §0 register ruling and the two flagged
wording items — R-2 contract→projections, R-4 permission namespace), the
DA is ready to receive the design request under the six-question
discipline. Projected shape at first sight (non-binding): one small
domain module (`join engine + api`), one migration (compver row + 1–2
permissions; possibly zero new tables), ~25–35 tests, no standing-law
edits beyond the permission-namespace ruling. The BE-9 fixture law
covers the broker side of every test; the BE-5 signal fixtures cover the
other side.

## §3 — Campaign-closeout register sync (executed with this memo)

Per `ITRGA-CAMPAIGN-BE9-CLOSE-001` (BE-9 OPERATING, 2026-09-06): maturity
v1.4.0 — `Broker Adapter` + `Broker Reconciliation` → **COMPLETE —
OPERATING** (fielded head `20260905_0049`; compver `bre-1.0.0 =
b0008cb9…` live on the working DB; first routine sync complete under
investor posture; F-E1-02 CLOSED). The operating-posture laws (investor
session only; sync-card cadence; `read_only_login_asserted == true` or
STOP; VR-D11 enumeration discipline) are adopted into the state document
as standing. The four lessons filed (codec sovereignty, paste-shape,
proxy fallback, N-O6/N-O7) are noted — two are DA-owned lapses caught by
STOP-LAWs; the discipline they teach is already encoded in §1 R-6.

**We don't guess. We prove.**

— AXIOM-V2-BE-10-DA-REQREV-001 · v1.0.0 · 2026-09-06
