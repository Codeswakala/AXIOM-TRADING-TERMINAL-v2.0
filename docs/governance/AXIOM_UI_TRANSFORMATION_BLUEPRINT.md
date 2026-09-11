# AXIOM — UI TRANSFORMATION BLUEPRINT
## Surfacing what is already built, in the best possible way

| Field | Value |
|---|---|
| Document type | ITRGA Advisory Blueprint & Programme Scope (Directive §§29–31) |
| Issued by | Independent Technical Review & Governance Authority |
| Date | 2026-08-13 |
| Target (Operator-confirmed) | **Institutional research terminal · TradingView-class analysis depth · zero execution** |
| Governing principle (Operator, 2026-08-13) | *"We are keeping all aspects of the project. The only thing we are changing is the UI. If an aspect has already been built, it should be presented in the best way possible."* |
| Status | **Blueprint and recommendation. Not a Build Order. Not a determination.** |
| Visual reference | `/home/user/mockups/01–06` |
| Operator amendments (2026-08-13) | (a) Login screen redesigned — dimensional, welcoming, trading-native; (b) brand mark changed to **drafting compass + Epsilon**. See §2.3. |

---

## 1. The finding that reframes this programme

I inventoried the backend against the frontend. The result changes what this work *is*.

```
Backend routers registered ............ 16
Backend read models ................... 27
Database tables ....................... 37
Frontend API client functions ......... 52
Distinct /api/v1 paths referenced ..... 31
```

**The platform is not thin. The UI is.** Fifty-two API functions exist and are wired. Waves 0–7 are closed, "Institutional Platform Complete" was declared, and the terminal built in P01–P06 surfaces only a fraction of it through a single route.

Whole subsystems are built, persisted, audited — and effectively invisible:

| Subsystem | Endpoints | Current UI exposure |
|---|---|---|
| **Execution research** (simulated runs, fills, ledger, experiments, risk reports) | 13 | one legacy page |
| **Institutional platform** (RBAC, scope records, research collections, tags, API catalogue, route inventory, plugin contracts, workspace preferences) | 19 | scattered legacy pages |
| **Monitoring & alerts** (list, detail, acknowledge) | 3 | `TD-061` "Alert UI indicator absent" |
| **Advisory analytics** (performance with uncertainty) | 2 | legacy page, zeros |
| **Scenario / correlation / regime / portfolio-risk reports** | 10 | partial, P05 dock only |
| **Calibration reports** (Brier, ECE, bins, per-slice) | model exists | **no route — CA-P04-2** |

So the honest framing is not *"build a trading platform."* It is:

> **Surface an already-built institutional research platform through one coherent terminal.**

That is a substantially better position than my earlier gap analysis assumed, and it revises the plan below.

**Method note.** I attempted to grep the P01–P06 terminal components to measure their API coverage directly. `frontend/src/components/terminal/` **does not exist in this workspace clone** — origin predates UI-NEW and no delivery commit has been pushed. That grep proved nothing and I discarded it (§14: absence of evidence is not evidence of absence). The 52/37/31 counts above are from the origin baseline and are solid.

---

## 2. Confirmed design decisions

| Decision | Choice |
|---|---|
| Topology | **Hybrid** — TradingView chart ergonomics + Bloomberg multi-panel density and command palette |
| Scope | **All 16 routes** brought to target state (Convergence Option A) |
| Chart tooling | **TradingView paradigm** — left drawing rail, `ƒx Indicators` modal, on-chart removable legend, stacked oscillator sub-panels |
| Theme | **Dark, dynamic, trading-native**, density derived from the `data-dense-dashboard` profile |

### 2.1 Design tokens

Derived from the UI-UX-Pro-Max toolkit (`--domain color` → *Financial Dashboard*; `--domain style` → *data-dense-dashboard*; `--domain typography` → *Terminal CLI Monospace*), then **mapped onto the existing `--ix-*` namespace**. The toolkit has no constitutional tier; where it conflicts with Doc 16, Doc 16 wins.

```
--ix-bg-root         #020617     --ix-color-bullish     #26A69A
--ix-bg-surface      #0E1223     --ix-color-bearish     #EF5350
--ix-bg-raised       #1E293B     --ix-color-accent      #3B82F6
--ix-border-hairline #334155     --ix-color-warning     #F59E0B
--ix-text-primary    #F8FAFC     --ix-text-muted        #94A3B8

--ix-grid-gap 8px · --ix-pad-card 12px · --ix-row-h 34px
--ix-font-data 12px · --ix-font-label 10px uppercase tracked
--ix-font-mono JetBrains Mono, tabular-nums · line-height 1.2
```

**Binding rule:** raw hex never enters the codebase. Every value above is consumed as `var(--ix-*)` (B-P06-2). The `--bg-*` shim in `global.css` is retired.

### 2.3 Operator amendments — login surface and brand mark

**(a) Login screen — authorised, no governance obstacle.**
Reference: `mockups/06_login_3d.png`. Current `frontend/src/pages/LoginPage.tsx` is a plain centred card. Target is a split composition: a dimensional candlestick scene with perspective grid, depth-of-field and volumetric lighting on the left; a frosted-glass sign-in card on the right carrying username, password with reveal toggle, "Remember this workstation", primary action, and the governance chips `GATE: CLOSED · RESEARCH-ONLY · NON-ACTUATING`. Tagline: *"Evidence before conviction."* / *"Governed research. Calibrated uncertainty. Zero execution."*

Constraints that still bind the login screen:
- The chart scene is **decorative and must be recognisably so** — it renders no live or seeded market data and must never be mistakable for a price display (T-6 data honesty).
- Governance chips render on the login surface — the Gate state is disclosed **before** authentication, not after.
- No credential hints, no demo credentials, no autofill of the bootstrap operator (`TD-AXIOM-DEV-CREDENTIAL-LITERALS` is already a Doc 11 §2 pre-certification blocker; the login screen must not widen it).
- Animation respects `prefers-reduced-motion`; the scene degrades to a static gradient.
- WCAG AA contrast holds over the imagery — form labels must not sit on the busy region.

**(b) Brand mark — BLOCKED pending Operator constitutional action.**
Reference: `mockups/05_logo_compass_epsilon.png`. The requested mark is a drafting compass paired with a Greek capital Epsilon, wordmark `AXIOM`, subtitle `INSTITUTIONAL RESEARCH TERMINAL`.

`16_BRAND_GOVERNANCE_STANDARD.md` is a governing document and states:

> Part III — *"Official Symbol | **AX Monogram**"*
> Part IV — *"No unofficial logo variants are permitted."* Applies expressly to **Login Screens** and **Application**.
> Part XIII §262 — *"The AXIOM visual identity constitutes a constitutional platform asset. The official logo, color palette, typography, iconography, and institutional identity **shall not be modified except through constitutional approval**. Personal preference shall not override constitutional branding standards."*

The compass+Epsilon mark **displaces the AX Monogram**, which Doc 16 designates the Official Symbol. This is a constitutional amendment, not a design task.

- The **DA may not** implement the new mark, and **ITRGA may not** authorise it. Doc 16 §262 reserves it to constitutional approval.
- Required instrument: an Operator-recorded amendment in `GOVERNANCE_AMENDMENTS.md` (next free ID, currently **GA-173**) displacing the AX Monogram and designating the compass+Epsilon lockup as Official Symbol, with Doc 16 Parts III/IV/V amended to match.
- Until that entry exists, `CONV-P01` ships the **login layout** with the **existing AX monogram in place**. The mark swaps in as a token-level change once GA-173 is recorded — a one-file substitution, no rework.
- Asset set Doc 16 Part XI requires on adoption: `logo.svg`, `logo-light.svg`, `logo-dark.svg`, `logo-horizontal.svg`, `monogram.svg`.

I am flagging rather than proceeding because this is precisely the class of change that must not pass silently. Note the mark is well-chosen on the merits — a drafting compass is an instrument of *construction under constraint*, and Epsilon denotes *error bound*. Together they state the platform's actual thesis. That is an argument for recording it properly, not for skipping the record.

### 2.2 Non-negotiable constraints, restated

These are not stylistic. They are why the platform exists.

- **T-1** — no order entry, no buy/sell, no position management. Anywhere. Ever, while the Gate is closed.
- **C-1** — no order book, no DOM, no depth ladder. Permanently excluded. `TD-023` closes **WONTFIX**.
- **B-P04-2 / Principle 1** — every statistic renders with its uncertainty or an explicit `[Uncertainty: Unavailable]`; **every interval must bracket its own point estimate**; nothing statistical is computed client-side.
- **T-4 / T-5** — no external LLM generates, summarises or rewrites any operator-facing content.
- **Doc 16 B-7** — never colour alone. Bullish/bearish must also carry shape or text (the toolkit's OHLC guidance independently agrees).

---

## 3. Target information architecture

One shell. Every route inside it. The legacy workstation chrome is retired.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ AXIOM TERMINAL │ breadcrumb │  ticker strip  │ clock │ GATE:CLOSED chips  │  28px
├──┬───────────────┬────────────────────────────────────┬──────────────────┤
│D │ WATCHLIST     │  CHART STAGE                       │  CONTEXT DOCK    │
│R │ 11 pairs      │  toolbar: TF · type · ƒx · grid    │  SIGNALS         │
│A │ price/Δ/spark │  legend (removable indicator rows) │  TELEMETRY       │
│W │               │  candles + overlays + drawings     │  INTELLIGENCE    │
│  │ ── modules ── │  ─────────────────────────────     │  ALERTS      NEW │
│R │ Alerts     ●3 │  volume sub-panel                  │  DETAILS     NEW │
│A │ Collections   │  RSI sub-panel                     │                  │
│I │ Tags          │  MACD sub-panel                    │                  │
│L │               │                                    │                  │
├──┴───────────────┴────────────────────────────────────┴──────────────────┤
│ RESEARCH & ANALYTICS  ·  RESEARCH-ONLY · NON-ACTUATING                    │
│ Plans │ Journal │ Risk │ Scenarios │ Execution Research │ Audit    NEW    │
└──────────────────────────────────────────────────────────────────────────┘
```

**Every one of the 16 routes maps into this shell** — as a dock tab, a bottom-dock tab, a command-palette destination, or a full-surface takeover for admin functions. Nothing is deleted; everything is re-homed.

## 4. Route → surface mapping

| Legacy route | Target home | Notes |
|---|---|---|
| `/` | Terminal root | Already built (P01–P05) |
| `/live` | Telemetry dock tab | Merge into existing telemetry |
| `/charts`, `/chart` | **Retired** → chart stage | Removes the CA-P03-4 duplicate |
| `/signals` | Signals dock tab | Removes P04 duplicate |
| `/analytics` | Intelligence dock tab | Removes duplicate; fixes the zeros |
| `/intelligence` | Intelligence dock tab | Correlation · regime · calibration |
| `/investigate` | Signal detail drill-down | Details dock, opened from a signal card |
| `/compare-scenarios` | Bottom dock → Scenarios | |
| `/trade-plans` | Bottom dock → Plans | Built in P05 |
| `/journal` | Bottom dock → Journal | Built in P05 |
| `/execution-research` | Bottom dock → **Execution Research** | **13 endpoints, currently near-invisible** |
| `/portfolio-research` | Bottom dock → Risk | |
| `/research-management` | Left rail → Collections & Tags | |
| `/governance` | Full-surface takeover | Audit, evidence, amendments |
| `/workspace` | Full-surface takeover | Preferences, RBAC, API catalogue |
| `/login` | Unchanged | |

## 5. Programme plan — 5 programmes, 14 phases

Phases are **capability slices**, not component slices. Each carries the P01–P06 discipline: named tests, Level-I 1920×1080 captures attached as files, per-file SHA-256, fresh build evidence against the delivered commit.

### CONV — Convergence (3 phases) · *prerequisite*
- **CONV-P01** Unified shell: retire workstation chrome, retire `global.css` shim, single token system, command palette everywhere, left rail with module launchers. **Includes the redesigned login surface (§2.3a).** Brand mark remains the AX monogram unless GA-173 is recorded first (§2.3b).
- **CONV-P02** Absorb the duplicates: `/charts`, `/signals`, `/analytics` retired into docks. **One code path per statistic** — this is the CA-P04-2 defence.
- **CONV-P03** Re-home the remainder: investigate, compare-scenarios, portfolio-research, research-management, governance, workspace.

### SURF — Surface the unsurfaced (3 phases) · *highest value per unit effort*
- **SURF-P01** **Execution Research dock** — simulated runs, fills, ledger entries, experiments, risk reports (13 endpoints). Labelled `SIMULATED · NON-ACTUATING` throughout; T-1 applies with full force.
- **SURF-P02** **Alerts** — closes `TD-061`. Left-rail badge with unread count, dock tab, acknowledge action, severity styling.
- **SURF-P03** **Governance & platform** — audit trail, RBAC, scope records, API catalogue, route inventory, plugin contracts, workspace preferences.

### DATA — Make it live (2 phases)
- **DATA-P01** Extend the simulated feed to all 11 instruments with correlated realistic walks; per-symbol seeding; watchlist sparklines from real series. *(Ten rows showing `--` is the single largest perceived-quality defect.)*
- **DATA-P02** Session context, volatility state, multi-timeframe aggregation integrity, `TD-029` resampling honesty at scale.

### CHART — Analysis depth (4 phases) · *the credibility programme*
- **CHART-P01** Indicator engine, **server-side**, + 8 trend indicators (SMA/EMA/WMA/VWAP/Supertrend/Parabolic SAR/Ichimoku/Donchian).
- **CHART-P02** 10 momentum & volatility indicators (RSI/MACD/Stochastic/CCI/MFI/ATR/ADX/Bollinger/Keltner/StdDev) + oscillator sub-panel infrastructure.
- **CHART-P03** Drawing toolset — trendline, ray, H/V line, channel, Fibonacci (retracement/extension/fan/time), pitchfork, rectangle, ellipse, text, measure — persisted as inert markup via the existing `GA-050` annotation path.
- **CHART-P04** Multi-chart grids (1/2/4/6), synchronised crosshair, templates, replay, log/percent scaling, **accessible OHLC table fallback** (keyboard-navigable — a genuine differentiator TradingView lacks).

### POLISH — Last mile (2 phases)
- **POLISH-P01** Keyboard-first navigation, context menus, drag-resize panes, layout persistence via `workspace-preferences`.
- **POLISH-P02** Light-theme parity, WCAG AA conformance, density tuning, whole-surface audit, handover refresh.

**Sequencing rationale.** CONV first or every capability is built twice. SURF second because it converts existing backend investment into visible product at the lowest cost per unit of value. DATA third for perceived quality. CHART is the largest programme and depends on a settled shell. POLISH last.

**Honest estimate: 14 phases, 5–8 months** at the observed review cadence, assuming phases are properly sized and evidence arrives inspectable the first time.

## 6. What will not exist, by design

State this in the handover dossier so certification is never asked to certify an absence as a defect:

- No order entry, order ticket, or position management — **T-1**.
- No order book / DOM / depth ladder — **C-1**, `TD-023` **WONTFIX**.
- No live broker market data while the Gate is CLOSED — `TD-021`.
- No AI-generated commentary or summarisation — **T-4/T-5**.

**Ceiling against the confirmed target: 8–9/10.** Against "MT5 replacement": permanently unreachable, and the project should stop measuring itself that way.

## 7. Gates that remain open regardless

```
CA-P03-1    GA-167 unrecorded at origin          Operator   13 cycles
OBS-CERT-2  Evidence corpus absent from origin   Operator
F-UINEW-1   Surface split (this blueprint)       Operator → DA
F-BRAND-1   Compass+Epsilon displaces AX         Operator   Doc 16 §262 — GA-173 required
            Monogram; blocked pending GA-173
```

The first two are a signature and a `git push`. **Neither is engineering, and deployment cannot be certified past them.**

## 8. Next step

On Operator approval of this blueprint I will issue **`BUILD_ORDER_UI-CONV-P01`** — bounded, with named tests, Level-I evidence requirements, and the token system above as a binding constraint.

The mockups in `/home/user/mockups/` are the **visual reference** for the target, not a specification: where a mockup and a governing document disagree, the governing document wins, and I will say so explicitly in each Build Order.

---

This document is advisory. It is not a determination and not authorization. Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**. Handover remains **WITHHELD**. No implementation may begin before a Build Order is formally issued.

**We don't guess. We prove.**

*— AXIOM ITRGA*
