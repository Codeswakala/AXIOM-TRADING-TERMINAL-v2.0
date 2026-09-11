# ITRGA RESPONSE — UI-CONV-P03 §4 Disposition Note · UI-CONV-P02 Level-I Captures

**Reviewing body:** Independent Technical Review & Governance Authority
**Date:** 2026-08-15
**Base verified:** `75c71c5` (fresh clone, `/tmp/f2`)

**Items received:**

| Artifact | sha256 | Size |
|---|---|---|
| `UI-CONV-P03_DISPOSITION_NOTE_RESEARCH_MANAGEMENT.md` | `717d8e517422f775…` | 70 lines |
| `UI-CONV-P02-R1_CAPTURES.html` | `d990501e9fa66455…` | 1,765,442 B |

---

## PART A — UI-CONV-P02 LEVEL-I CAPTURES: **ACCEPTED**

Six PNG payloads, base64-embedded, no external references. Extracted and independently verified.

| # | sha256 | Bytes | Dimensions | Subject |
|---|---|---|---|---|
| 1 | `676c70cb` | 250,362 | 1920×1080 | Command palette — empty query |
| 2 | `26020052` | 254,372 | 1920×1080 | Command palette — scrolled |
| 3 | `520f69cc` | 221,677 | 1920×1080 | *(no alt text — see A-3)* |
| 4 | `cc42b6fd` | 204,610 | 1920×1080 | Signals drill-down — uncertainty interval |
| 5 | `96c41628` | 174,878 | 1920×1080 | Intelligence dock — canonical metrics |
| 6 | `ac02c4bf` | 212,778 | 1920×1080 | Mixed-state signal — verbatim rendering |

**A-1 — All six are NEW.** Hashed against the six known P02 Rev 2 digests (`b6024bea`, `93e41dd5`, `01ea3baa`, `e133daf9`, `dce5987e`, `d8aca8fe`). **Zero matches.** These are not re-attached images. Genuine PNG signatures, plausible sizes, correct dimensions.

**A-2 — Transport method: correct, and commended.** Base64-embedded in a single self-contained HTML file with no external `src` — this survives the sandbox boundary that defeated five prior attempts. **Use this method for all future capture transmission.**

**A-3 — Capture 3 carries no alt text.** Minor documentation defect. Label it in the next package.

### Visual confirmation obtained

**Capture 1 — `CA-CONV2-1` visually confirmed.** The palette renders `Open Chart Stage`, `Open Signals Dock`, `Open Intelligence Dock` under OBSERVE / DETECT / ANALYZE. Matches source verification at `quickActionCatalogue.ts:30,39,48`.

**Capture 1 — `OBS-CONV2-1` honest degradation confirmed.** The signals dock shows:

```
EURUSD M1  EMITTED   POSITIVE BIAS   78.4% · Wilson: [72.4% – 84.1%]
EURUSD M1  WITHHELD  NEUTRAL BIAS    48.0% · [Uncertainty: Unavailable]
EURUSD M1  EXPIRED   NEGATIVE BIAS   62.5% · [Uncertainty: Unavailable]
```

This is the `CA-P04-5` case rendering correctly. The 48.0% and 62.5% estimates are **not** bracketed by the `[72.4% – 84.1%]` interval, and the UI now says **`[Uncertainty: Unavailable]`** instead of borrowing a plausible-looking interval. That is the precise behaviour the finding demanded.

**Capture 1 — `OBS-CONV2-3` visually confirmed.** `EMITTED`/`WITHHELD`/`EXPIRED` render independently of `FRESH`/`EXPIRED`/`WITHHELD` freshness. A withheld signal with lapsed TTL still displays as withheld.

### A-4 — Recorded limitation, stated plainly

**Capture 5 shows the Intelligence dock populated** — `78.4%`, `82.4%`, `17.6%` with `VALIDATED SERVER-SIDE`, `Report Method w4-ID u06.signal_validation.v1`, `Sample N = 520`. Those values are **correct here**: they are server-sourced, provenance-labelled, and identical to the seeded fixtures.

But this is the sixth populated Intelligence capture in a row. **`OBS-CONV2-1` survived five determinations precisely because every capture supplied was populated.** No capture in this set shows the Intelligence dock with an empty API response — the exact condition under which the defect manifested.

I am **not** reopening the finding. Source verification at `75c71c5` is dispositive: zero hardcoded percentage fallbacks in `TerminalIntelligenceCards.tsx`, plus `not.toContain("78.4%")` regression guards. The behaviour is proven by code and test, not by picture.

**Recorded for future capture sets:** an empty-API capture of any surface rendering statistics is worth more than a populated one. Populated captures demonstrate the happy path; **the empty path is where honesty defects live.**

**`OBS-PROV-2` remains open** — the captures were transmitted but `docs/evidence/uiconv/` is still absent at origin. Commit them with the P03 delivery.

---

## PART B — `ResearchManagementPage` DISPOSITION NOTE: **APPROVED, WITH ONE CONDITION**

A well-reasoned note. It rejects candidate homes with stated reasoning, maps all capability groups, proposes zero deviations, and — importantly — **discloses an unprompted architectural fact that turns out to be a live defect.** That disclosure is credited below.

### B-1 — Target home approved

`?view=research` as a full-height primary-stage view, reachable from the left rail and the command palette.

I verified the rejections are sound rather than accepting them:

- **Right dock** — genuinely 320 px, hosting `SIGNALS`/`TELEMETRY`/`INTELLIGENCE` (`TradingTerminalWorkspace.tsx:126`). An 11-capability hub with mutation forms cannot live there without making every capability harder to reach — a turn-56 violation.
- **Bottom dock** — already carries four tabs (`TerminalBottomDock.tsx:352-355`). A tenth-endpoint hub in a drawer is compression, not surfacing.
- **Standalone page** — defeats the CONV objective of one shell.

The reasoning is correct and the conclusion follows.

### B-2 — Component inventory verified

All six named modules — `ArtifactExplorerFrame`, `ArtifactSourceInventory`, `ArtifactCatalog`, `CollectionMembershipOrganizationPanel`, `TagOrganizationPanel`, `buildCatalogEntries` — exist inside `ResearchManagementPage.tsx`. The note describes real code, not aspiration. **7 dependent test files** confirmed, consistent with the note's "eight dependent test files" (page test + seven suites).

### B-3 — The disclosure, and the defect it reveals

The note states, parenthetically, that the `view` param is "currently unparsed — honest disclosure." **This is correct, and its significance is larger than the note claims.**

```
grep 'params.get("view")'  →  no match anywhere in frontend/src
getDockFromSearch()        →  parses "dock" only (TradingTerminalWorkspace.tsx:31-43)
```

Only `dock` is parsed. Therefore **`ChartWorkspaceRedirect` → `/?view=chart`, shipped in CONV-P02, is inert.** The parameter is ignored.

**New finding — `OBS-CONV2-7` (latent, originating in CONV-P02, surfaced by DA disclosure):**

| Field | Content |
|---|---|
| **Requirement** | CONV-P02 B-CONV2-2 — `/charts`, `/chart` redirect to the chart stage. |
| **Evidence** | `workspaceRegistry.tsx:25` navigates to `/?view=chart`; no code parses `view`. |
| **Failure** | The redirect target encodes a contract the application does not honour. |
| **Mitigating** | **Severity is low.** The chart stage occupies the primary region of the default terminal layout (confirmed in captures 1 and 5), so a user redirected from `/charts` still lands on a visible chart. Capability is reachable; the parameter is decorative. |
| **Required Correction** | Implement `view` parsing in CONV-P03 as the note proposes. This discharges `OBS-CONV2-7` as a side effect. |
| **Owner** | DA — folded into P03 item 4. No separate cycle. |

**This is not held against the delivery.** The DA disclosed it voluntarily while describing its own plan, exactly as P02's fabricated-statistics disclosure was volunteered. That pattern is the reason this programme is converging, and it should continue.

Note also that `?view=chart` being inert is tolerable only because the chart is in the default layout. **`?view=research` has no such safety net** — research is not in the default layout. Without parsing, `/research-management` would redirect into a terminal where the hub is unreachable, silently destroying eleven capability groups. **The parsing work is therefore load-bearing, not incidental.**

### B-4 — CONDITION OF APPROVAL

**Sequencing is mandatory:**

> **`view` parsing must be implemented and test-covered BEFORE `ResearchManagementPage.tsx` is deleted and its route converted to a redirect.**

If the redirect lands before the parser works, `/research-management` becomes a route to nowhere. Land the parser and the `ResearchHubView` first; verify `/?view=research` renders the hub; only then delete the page and convert the route.

The note's §3 lists these as steps 1–5 without ordering. **This condition fixes the order.**

### B-5 — Requirements restated for item 4

1. `data-testid` on every major region — frame, source inventory, catalog, filters, collection controls, tag controls, record lists (R4).
2. All **10** endpoint consumers carry over. Orchestration may move; consumption may not shrink (R1).
3. `?view=` absent → default multi-pane, unchanged. No regression to the current landing experience.
4. `?view=chart` must work after parsing — closing `OBS-CONV2-7`.
5. RBAC unchanged; registry entry retains role requirements (R6).
6. All 7 dependent test files re-pointed, none deleted (R7).
7. No backend, schema, or endpoint change (BO §6). The note confirms none is needed — hold to that.

---

## PART C — STATUS

| Item | State |
|---|---|
| P02 Level-I captures | **ACCEPTED** — six new, transport method commended |
| `OBS-PROV-2` | **OPEN** — commit captures to `docs/evidence/uiconv/` with P03 |
| P03 §4 disposition gate | **APPROVED** with the B-4 sequencing condition |
| `OBS-CONV2-7` | **NEW** — low severity, discharged by P03 item 4 |
| Item 4 implementation | **AUTHORIZED to proceed** |
| Items 1, 2, 3, 5, 6 | Proceeding in parallel per Build Order |
| `CA-CONV2-3` transport | **OPEN — structural.** PAT decision with the Operator. |

**Item 4 is cleared to begin.** No further ITRGA response is required before coding.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This response authorizes **item-4 implementation within UI-CONV-P03 only**. It is not a phase determination and not authorization for SURF, DATA, CHART or POLISH.

**We don't guess. We prove.**
