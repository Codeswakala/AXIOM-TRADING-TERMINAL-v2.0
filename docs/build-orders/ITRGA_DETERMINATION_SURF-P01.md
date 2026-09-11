# ITRGA DETERMINATION — SURF-P01

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** Execution Research dock — surfacing the unsurfaced
**Date:** 2026-08-16
**Base:** `34f4c62` + item3 (`b7b4c4f7…`) + item5 (`4c03910c…`) + item6 (`f65da5c3…`) + item4 Rev B (`a516c2c1…`)
**Verification:** `/tmp/surf` — pristine clone → CONV chain → SURF-P01 applied

| Artifact | sha256 | Size |
|---|---|---|
| `surf_p01.patch.txt` | `62c4d021e5b6f0a0` | 2,804 lines · 16 files |
| `DELIVERY_REPORT_SURF-P01.md` | `e65dae772e59dd63` | 215 lines |
| `SURF-P01_CAPTURES.html` | `4e5c9cf839010fb0` | 5 PNGs |
| `SURF-P01_CAPTURE_VERIFICATION.json` | `8fdcce6050a59b4a` | 139 lines |

---

## 1. DETERMINATION

# APPROVED WITH OBSERVATIONS

Every mandatory requirement is met, including the hard exclusion. One observation concerns a capture that does not evidence its claim.

**Transport:** sha256 `62c4d021e5b6f0a0…` matches the declared hash exactly; `git apply --check` exit 0 on the stated base chain; base declared explicitly. **Fifth consecutive hash-reconciled delivery.**

---

## 2. THE HARD EXCLUSION — RESPECTED

The five POST endpoints were the live risk in this phase: reachable, trivially surfaceable, in a *surfacing* phase.

```
grep createSimulatedRun|createSimulatedLedger|createExecutionRisk|
     createExecutionExperiment|createSimulatedAnalytics   →  0 matches
POST to execution-research anywhere in frontend           →  0 (one comment only)
create/new/submit affordance in the new surface           →  0
```

The only reference is a code comment in `api/client.ts:1064` documenting that the backend has 17 endpoints (12 GET + 5 POST) and that the POSTs are deliberately unsurfaced. **Documenting a boundary rather than crossing it is the correct behaviour**, and it leaves the next authority a record of why the gap exists.

**M3 — no execution affordance, real or implied — holds.** The surface reads `Display-only workspace for server-persisted SIMULATED execution research artifacts… the browser performs no authoritative analytics rerun.`

---

## 3. MANDATORY REQUIREMENTS

### M1 — Frontend T-1 guard ✓ — the gap I identified is now closed

`test_execution_research_ui_module_has_no_live_execution_controls` added at `test_execution_research_safety.py:181`, pinning `components/terminal/execution/ExecutionResearchView.tsx` with **three non-vacuity anchors**:

```python
assert "execution research workspace" in text
assert "simulated" in text
assert "non-actuating" in text
forbidden = ("place_order", "submit order", "go live", "connect broker",
             "broker_account", "order_ticket", "account_id",
             "execute_order", "live_trade")
```

The docstring states the reasoning: *"this suite previously pinned none… the positive assertions fail loudly if the path is ever re-pointed at a wrapper or barrel that does not contain the surface."*

The platform's most execution-adjacent surface now carries a frontend constitutional guard. **Backend suite: 415 → 416 passed.**

### M2 — `SIMULATED · NON-ACTUATING` per artifact group ✓

A `SimulatedGroupBadge` component rendered at **all six** groups — `runs` :359, `fills` :370, `ledger` :381, `risk` :394, `experiments` :405, `analytics` :422 — each with its own `execution-sim-badge-{family}` testid. Verification JSON records `capture01_sim_badges: 6`.

Not a single header label. Per group, as required.

### S1–S4

| Req | Result |
|---|---|
| **S1** re-homed | `/?view=execution` stage view; `ExecutionResearchRedirect` :69, registry :343 |
| **S2** six detail GETs surfaced | All six present in `api/client.ts` — `{run_id}` :1123, `{fill_id}` :1131, `{ledger_entry_id}` :1141, risk `{report_id}` :1151, `{experiment_id}` :1161, analytics `{report_id}` :1171 |
| **S3** fills truncation | **Removed.** `runs.map(...)` replaces `runs.slice(0, 5)`, with a comment naming it *"a quiet inaccuracy (OBS-CONV2-1 family)"* |
| **S4** testids | **27** (baseline 0) |

### R1 — Capability preservation ✓

All seventeen checked strings present, including every honesty surface: `Replay scope`, `Assumptions`, `Limitations`, `Pre-registration plan`, `As-of window`, `Replay lineage`, `Included scope`, `Request evidence`, `Metrics`. New additions — `Source Status`, `Detail record`, `Fills (n)`.

*(`Analytics & Comparison` is present as `Analytics &amp; Comparison` — HTML entity encoding, not a gap.)*

### R2–R7

`/execution-research` redirects · **six independent error states** (`runsError`, `fillsError`, `ledgerError`, `riskError`, `experimentsError`, `analyticsError`) with a Source Status panel stating the contract in-UI · 6 absence markers · RBAC 16/16 unchanged · `ExecutionResearchPage.tsx` and its test **deleted**.

### Execution evidence

```
Test Files  167 passed (167)
     Tests  785 passed (785)      ← +10
tsc exit: 0
pytest      416 passed  (+1: the M1 guard)
build       index-SwOPTjUM.js 697.62 kB │ gzip 188.09 kB
```

**1,201 tests green.** Bundle 687.85 → 697.62 kB (**+9.77 kB**) for six new client functions, a detail-record panel and per-source state. Proportionate; `OBS-5` / POLISH-P01 owns code-splitting.

---

## 4. OBSERVATION — `OBS-SURF1-1`: capture 04 does not evidence its claim

| Field | Content |
|---|---|
| **Requirement** | Build Order §6.8 — a single-seam failure capture showing independent degradation. |
| **Evidence** | Capture 04 is declared *"ONE seam (paper ledger) aborted; exactly 1 error row."* The frame shows the `SOURCE STATUS` **heading and description**, then the section is **clipped** — the six source cards, including the `Paper ledger / Failed to fetch` row, are below the visible fold. What is in frame is `PERSISTED SIMULATED ARTIFACTS` showing Runs 3 · Fills 0 · Ledger 0 · Risk reports 0. |
| **Failure** | The error row the capture exists to prove is not visible. `capture04_scroll_metrics` records `scrollTop: 0` with `scrollHeight 2822` against `clientHeight 798` — the container was **not scrolled**, despite the filename `..._DEGRADATION_SCROLLED.png`. |
| **Contradiction** | The JSON asserts `capture04_errorRowVisibleInViewport: true`. **That assertion is inconsistent with the image.** The measurement is checking a different geometry than the rendered frame — the same class of instrument flaw the DA itself disclosed for item 4's pre-scroll hit-test, and it went undetected here. |
| **Mitigating** | The underlying behaviour is verified by other means: `capture04_single_seam_failure` records `errorRows: 1, readyRows: 5, hubStillRenders: true, ledgerErrorText: "Paper ledgerFailed to fetch"`; six independent error states exist in source; `Ledger 0` renders honestly in frame rather than showing a fabricated count. |
| **Required Correction** | Re-capture with the inner scroll container actually scrolled to the Source Status cards. Review the viewport-visibility check — it returned `true` for a region that is not in the frame. |
| **Owner** | DA |

**Not blocking.** R4 is verified in source and by machine record. But this is the fifth cycle in which a capture has been offered for a region below the fold, and here the verification instrument *affirmed* visibility that the image contradicts. **A measurement that can return `true` for an invisible element cannot discharge a visual requirement.** That is worth fixing before it certifies something less well-corroborated.

Captures 01, 02, 03 and 05 are sound — including `capture03_emptyMarkerVisibleInViewport` with four named absence markers, and `capture01_hitTestDetailButtonOwnsPointerBeforeClick: true` supplying the interaction trace.

---

## 5. STATUS

| Item | State |
|---|---|
| **SURF-P01** | **APPROVED WITH OBSERVATIONS** |
| M1 frontend T-1 guard | **CLOSED** — gap identified pre-phase, now guarded |
| M2 per-group labelling | Verified — 6/6 |
| M3 no execution affordance | Verified |
| POST exclusion | **Respected — 0 client functions** |
| S2 six detail GETs | Surfaced |
| S3 silent truncation | **Removed** |
| `OBS-SURF1-1` capture 04 + viewport check | **NEW** |
| `OBS-5` bundle 697.62 kB | Open — POLISH-P01 |
| `OBS-CONV2-5` seeded fixtures | Open |
| `F-BRAND-1` | Open — GA-173 |
| CONV closures | Verified intact |

**Artifacts of record** (`/home/user/uploads/`), chain applies clean in order:

```
item3.patch.txt      b7b4c4f74f3016cb
item5.patch.txt      4c03910c76fdcbf2
item6.patch.txt      f65da5c3ce8433ec
item4.patch (1).txt  a516c2c144c1f2f6
surf_p01.patch.txt   62c4d021e5b6f0a0
```

**Next:** SURF-P02 — Alerts, closes `TD-061`; left-rail badge with unread count, dock tab, acknowledge action, severity styling. **Not authorized.**

Note for SURF-P02 scoping: an *acknowledge* action is a **write**. Unlike the five POSTs excluded here, it is named in Blueprint §5 as part of the phase. I will inventory the endpoint and its guard requirements before issuing the Build Order.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination approves **SURF-P01 only**. Not authorization for SURF-P02, SURF-P03, DATA, CHART or POLISH.

**We don't guess. We prove.**
