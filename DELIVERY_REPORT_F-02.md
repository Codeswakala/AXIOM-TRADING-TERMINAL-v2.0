# DELIVERY REPORT — BO-F-02
## Signal Presentation — Two Families (Structural + Predictive)

| Item | Value |
|------|-------|
| Build Order | `BO-F-02` (Operator directive 2026-08-21: "authorized") |
| Predecessors | F-01 CLOSED (ITRGA 2026-08-21) · B-03 gated/deferred · CA-RECON-2 §11/§13 |
| Implementer | Development Authority (DA) |
| Deliverable class | Frontend implementation unit (chain position 33) |
| Governance Gate | CLOSED · Production NOT CERTIFIED (unchanged) |
| Determination | Awaiting ITRGA independent determination (BO §12) |

---

## 1. Claimed scope vs. this Build Order

Executed exactly BO-F-02 §2: F-02.1 two-family framing, F-02.2 structural
signal family (the new work), F-02.3 predictive family completion, F-02.4
non-actuation + honesty. §3 exclusions honored: no backend change (pure
consumer of the existing indicator-series and advisory-signal read APIs), no
predictive generation (B-03 stays gated), no family collapsing, no actuation
controls, no external LLM, no design-language weakening, no repo publication.
§6 allowed files plus one disclosed addition (D1). Register rows ship in the
patch per the standing append-only convention (BO §9 binding).

## 2. What changed (files + SHAs + chain position)

Patch `f02.patch` — **chain position 33**, 5 files (3 modified + 2 new), zero
backend files. Applies clean onto `34f4c62` + elements 1–32; post-apply cmp
5/5; register hunk proven to apply onto a drifted (baseline-era) register with
the code at chain-32. Patch sha256:
`7f6a0931f166cefb17010c4f0e828c25703706a12751cf0c72e65354e7242c60`.

| File | Change |
|---|---|
| `frontend/src/components/terminal/StructuralSignalStream.tsx` | **New** — the structural family: `deriveStructuralEvents` (pure transcription of non-null indicator-series markers) + the event surface with descriptive framing, timeframe selector, provenance line, honest empty/unavailable states |
| `frontend/src/components/terminal/TerminalSignalStream.tsx` | Family tab bar (STRUCTURAL \| PREDICTIVE (ML)), predictive family label, deferral-honest empty state, structural mount; all existing predictive behavior preserved |
| `frontend/src/components/terminal/TerminalMultiPane.css` | F-02 styles (family tabs, family label, structural event cards, provenance line) — pure token consumption (D1) |
| `frontend/src/test/f02_signal_families.test.tsx` | **New** — 14 tests (§7) |
| `docs/governance/TECHNICAL_DEBT_REGISTER.md` | This unit's rows + F-01/X-01 CLOSED status rows — pure-addition hunk in the patch (§9) |

## 3. Two-family framing description

The signal stream (right dock, SIGNALS tab) now opens with an explicit family
tab bar — **STRUCTURAL** and **PREDICTIVE (ML)** — a labeled, keyboard-
accessible `tablist` (test-pinned `aria-selected`). The predictive header
carries a `PREDICTIVE (ML)` family chip. The two families are never visually
indistinguishable, and the distinction is data-origin-derived, exactly as
CA-RECON-2 §13 binds: structural events come from the indicator layer;
predictive entries come from `GET /signals/history` (persisted advisory
signals). No third category exists. Default family is predictive (the
pre-F-02 behavior; existing surface pins preserved).

## 4. Structural-signal derivation (indicator series → event list)

`deriveStructuralEvents(envelope)` is a **pure transcription**: every non-null
point on the server-computed SMC/ICT series (`BOS55`, `CHOCH55`, `FVG3`,
`STRUCT55`, `SWINGS55`) becomes one discrete event — type (BOS / CHoCH / FVG /
STRUCTURE / SWING), direction (up / down / zone), time, symbol, timeframe,
level. Unknown line names are skipped (never invented); FVG top/bottom edges
sharing a timestamp are paired into one zone event (the backend emits both
edges at the detection bar); all-null or unavailable series yields zero
events. Events are sorted newest-first and capped at 24. Every event renders a
descriptive label ("Break of structure upward", "Higher-high structure
point"…) — never a prediction — under the surface framing
"**DETERMINISTIC · DESCRIPTIVE — NOT A PREDICTION**", with a provenance line
stating symbol/timeframe/series kind. Timeframe selector M1–D1.

## 5. Predictive deferred-empty state description

The predictive family is labeled **PREDICTIVE (ML)** and, with no promoted
model (the tracked deferral), its empty state now states the truth instead of
a bare list: *"No predictive signals — the predictive track is deferred (no
eligible model). Deterministic structural signals remain available in the
Structural family."* All existing predictive behavior is preserved: state
filters (ALL/EMITTED/WITHHELD/EXPIRED/SUPERSEDED), verbatim `signal_state`,
the canonical CalibratedConfidenceBadge, rationale/eligibility drill-down,
RESEARCH-ONLY · NON-ACTUATING framing.

## 6. Screenshot evidence (Level-I, `docs/evidence/f02/`)

| Capture | File | Result |
|---|---|---|
| Predictive deferred-empty | `f02_predictive_deferred.png` | PREDICTIVE (ML) label + honest deferral text |
| Structural honest empty | `f02_structural.png` | EUR/USD 1h over the 80-bar M1 seed — insufficient for the 55-lookback structure indicators; honest "unavailable" empty (no fabrication) |
| Structural over REAL data | `f02_structural_real.png` | **24 EVENTS** over BTCUSD H1 native series (real corpus); first event "Fair value gap zone", 2026-07-31 23:00 UTC; provenance line "Derived from server-computed indicator series · BTCUSD H1 · series kind: native" |
| Structural unavailable empty | `f02_structural_empty.png` | EUR/USD 1d — honest unavailable state |
| Probe log | `f02_capture_log.txt` | Family-tab states, framing text, counts, no-actuation scan (violations: none) |

**Capture fixture disclosed (same class as F-01's seeding):** the terminal's
crypto symbol key is BTC/USD (`BTCUSD`) while the corpus ingest label is
`BTCUSDT`; the same real OKX bars were ingested under the platform's symbol
key (`source=historical:real`) so the terminal's structural view derives over
REAL data with an honest label. Local dev DB only; no code path changed.

## 7. Non-actuation + no-fabrication evidence

- Derivation tests: all-null series → 0 events; unavailable envelope → 0
  events; unknown line names → skipped; cap at 24; FVG pairing is timestamp-
  exact transcription.
- No-actuation: unit test + browser scan over the structural surface — zero
  occurrences of buy/sell/order/broker/execution/account; the only controls
  are family tabs, timeframe buttons, and signal-card expanders.

## 8. Test evidence (executed)

- Workspace full frontend suite: **920 passed / 176 files** (906 floor + 14
  new), 180.60s, exit 0 — `f02_vitest_fullsuite.log`.
- Typecheck: `tsc -b` exit 0 — `f02_tsc.log`.
- Production build: green (chunk-size warning pre-existing).
- Clone-side (gold standard): pristine `34f4c62` → 33 elements → `npm ci` →
  tsc clean → **920 passed** — `f02_cloneside_vitest.log`.

## 9. Deviations register

| ID | Deviation | Assessment |
|----|-----------|------------|
| D1 | `TerminalMultiPane.css` edited — the stylesheet home of the dock components (not named in §6) | Same accepted class as F-00/F-01 stylesheet deviations; pure `var(--ix-*)` token consumption, no hex literals; design-governance scans pass. |
| D2 | Structural view holds its own timeframe state (default 1h) | The terminal context shares the symbol but not the chart timeframe; a local selector is the minimal honest mechanism (no context re-architecture per §3). |
| D3 | Capture fixture: real bars re-ingested under the terminal's `BTCUSD` symbol key | Disclosed in §6; local dev DB only; honest labels preserved. |
| D4 | Default family = predictive | Preserves pre-F-02 behavior and the existing surface pins (filters visible at mount); the framing tabs make both families one click apart. |

## 10. Register rows in patch (confirmed) + transmission manifest (relay-accurate)

The patch's register hunk is a zero-context pure-addition (12 appended lines):
TD-F01-UNIT-STATUS (CLOSED — APPROVED WITH OBSERVATIONS),
TD-X01-UNIT-STATUS (CLOSED — recorded per the ITRGA predecessor lines),
TD-F02-UNIT (this unit). Verified to apply onto the chain-32 register (cmp
byte-identical) AND onto a baseline-era drifted register (DRIFT-PROOF OK).

All files newly transmitted with this delivery; byte-identical copies in
`/home/user/f02_transmission/`, cmp-verified; hashes mechanically verified
against the folder before this message (sha256sum -c MANIFEST.txt exit 0). This
report's own sha256 is declared in the DA's closing message; `MANIFEST.txt`
carries it.

| # | File | sha256 |
|---|---|---|
| 1 | `f02_transmission/f02.patch.txt` | `7f6a0931f166cefb17010c4f0e828c25703706a12751cf0c72e65354e7242c60` |
| 2 | `f02_transmission/f02_applycheck_transcript.txt` | `97d1128bdc7c285f13a2245b06a6d09a99aa7a8e3af5ee101966c1639dc47dd5` |
| 3 | `f02_transmission/f02_capture_log.txt` | `b1c5066a3083785c27fa708a0205cfd51efb0a822c189084d2bc7469b0736c00` |
| 4 | `f02_transmission/f02_cloneside_vitest.log.txt` | `9952461a20d04464700922f8ddb3f06a7bc405ce19f6769435fcad2c0cf21305` |
| 5 | `f02_transmission/f02_predictive_deferred.png` | `6f8e2b8b9abd76b9e262b2208f2eeba0d23215621602a0d3d5c67bde8e68b63f` |
| 6 | `f02_transmission/f02_structural.png` | `4fbc060f2010442ffe2684f99450c9f3603117e88497a9e8ab471a8a122313ed` |
| 7 | `f02_transmission/f02_structural_empty.png` | `d708eae1c7f4c6aeb7ed687809475086c77d6bfdba45bf1ea9ba356b9c49f56d` |
| 8 | `f02_transmission/f02_structural_real.png` | `bc7556a3600adfc95b650fc552d5bb26297b53c4fb8fc6e878fefc0b6d9336b3` |
| 9 | `f02_transmission/f02_tsc.log.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 10 | `f02_transmission/f02_vitest_fullsuite.log.txt` | `bc5718d080bb2e2249681809b4722f7a121f7ee767bd61cf97aceed37735f5a3` |

---

**Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.**
