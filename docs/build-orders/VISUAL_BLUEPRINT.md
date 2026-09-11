# AXIOM — Visual Blueprint (Approved)
## Institutional Terminal Design Language, Theme System & Login Experience

| Item | Value |
|---|---|
| Document class | **Design plan / approved visual target** (governing instrument for all frontend F-units) |
| Approval | **Operator** — "I approve the blueprint" (2026-08-21), with two refinements: multi-theme + 3D-animated login |
| Status | **APPROVED** — basis for frontend Build Orders; still subject to ITRGA review per lifecycle before implementation |
| Prototype set | `review/prototypes/01…15` (15 screens, single design language) |
| Governance Gate | CLOSED · Production NOT CERTIFIED (unchanged) |

---

## 1. Purpose

This document converts the approved prototype set into a **concrete, reviewed visual target** so that "professional" is a signed-off artifact, not a feeling at the end of a build. Every frontend unit (F-00 → F-06) must conform to this language.

## 2. Design language (from the approved prototypes)

| Dimension | Rule |
|---|---|
| Background | Midnight Black `#0b0e14` |
| Panels | Graphite Gray `#111822`, thin `#172131` borders |
| Accent | Electric Blue `#3b82f6` (single accent) |
| Typography | Sans-serif UI (Segoe UI / Inter); **monospace numerals** (JetBrains Mono) for every price/metric/hash |
| Density | Institutional terminal density (Bloomberg / TradingView / MT5), not consumer dashboard |
| Semantic color | Green up / red down / amber warning — used for *meaning only*, never decoration |
| Governance framing | "GATE CLOSED · RESEARCH-ONLY · NON-ACTUATING", "SIMULATED", "HYPOTHETICAL", "NOT FINANCIAL ADVICE" are **part of the visual language** |
| Non-actuation | **No** buy/sell/order/execution controls appear anywhere in the UI |

This language maps to the existing `--ix-*` design-token system (verified in `frontend/src/workstation/design/tokens.css`), which already implements Tier-5 runtime theme overrides — so the multi-theme requirement below is architecturally supported, not a rework.

## 3. Theme system (multi-theme — refinement #1)

**Approved requirement (Operator, 2026-08-21):** all six proposed themes — "let's go with all of them."

| Theme | Character | Basis |
|---|---|---|
| **Midnight** (default) | The approved prototype look — deep black, graphite, electric-blue accent | Prototypes |
| **Light** | White/silver panels, dark text, same blue accent | Already implemented (`.theme-light` in `tokens.css`) |
| **Slate** | Softer "graphite-pro" dark — mid-gray panels, *reduced* blue accent, for long-session eye comfort | New |
| **High-Contrast** | Pure black/white, semantic colors at max contrast, for accessibility (WCAG AAA) | New |
| **Teal** | Navy/teal "pro dark" — cyan-teal accent (`#22d3ee`) for active states | New |
| **Amber** | Warm "terminal" dark — amber/gold accent (`#f59e0b`) for active states | New |

Each theme is a **token-level override** (colors only) — layout, density, typography, and governance framing are identical across themes. Theme is a per-operator preference (persisted via the existing workspace-preferences mechanism), not a global switch.

**Governance note (Operator-authorized, recorded):** Teal and Amber accents are **presentation-level theme variants, not brand colors** — the brand identity (logo, monogram, default Midnight palette) remains unchanged per Doc 16. This is an Operator-approved interpretation: theme accent colors are user-selectable presentation, while the constitutional brand palette governs *brand identity* (logo, official platform colors, documentation). If a future audit disputes this reading, a formal Doc 16 amendment would then apply — but for the current theme set, the Operator's authorization stands.

## 4. Login experience (3D-animated — refinement #2)

**Approved requirement (Operator, 2026-08-21):** the login scene is 3D-animated, using the **"wave" composition** — candles flowing like a wave across the lower third, particles drifting, glow pulse.

**Technical approach (recommended):**
- **CSS 3D transforms + keyframe animation** — the wave layers (candles, particles, glow) animated with perspective and drift. Zero dependencies, fast first paint, hardware-accelerated.
- WebGL/Three.js is **not** recommended unless richer geometry is later required — it is a dependency and the project has been deliberately dependency-frugal (Doc 09 §12).

**Binding constraints (unchanged from the existing LoginPage discipline):**
1. **Decorative only** — the scene carries **zero real/seeded market data** (no prices, axes, or timestamps); it is ambient brand motion.
2. **`prefers-reduced-motion: reduce`** must freeze the animation to a static frame (the existing `tokens.css` already handles this globally).
3. **Performance** — the login scene must not delay sign-in or cost more than ~1MB of asset budget.
4. The governance chips ("GATE CLOSED · RESEARCH-ONLY · NON-ACTUATING") remain visible on the login surface.

## 5. Screen inventory (approved prototypes)

| # | Screen | Prototype |
|---|---|---|
| 01 | Login (3D animated — §4) | `01_login.png` |
| 02 | Terminal Home | `02_terminal_home.png` |
| 03 | Chart Workspace | `03_chart_workspace.png` |
| 04 | Live Market | `04_live_market.png` |
| 05 | Institutional Intelligence | `05_intelligence.png` |
| 06 | Advisory Signals | `06_signals.png` |
| 07 | Scenario Comparison | `07_scenario_comparison.png` |
| 08 | Trade Planning | `08_trade_planning.png` |
| 09 | Execution Research | `09_execution_research.png` |
| 10 | Portfolio Research | `10_portfolio_research.png` |
| 11 | Research Journal | `11_journal.png` |
| 12 | Artifact Explorer | `12_artifact_explorer.png` |
| 13 | Governance & Evidence | `13_governance.png` |
| 14 | Settings | `14_settings.png` |
| 15 | Contextual Assistant | `15_assistant.png` |

## 6. Governance constraints (binding on all F-units)

- **Brand (Doc 16):** colors, typography, and logo usage conform to the constitutional palette and monogram. New primary colors require constitutional approval.
- **Accessibility (Doc 12 / UI-010):** WCAG AA minimum (AAA in High-Contrast theme); keyboard navigation; focus management; reduced-motion honored.
- **Non-actuation:** the UI reflects the platform's actual posture — no execution controls, honest "SIMULATED"/"HYPOTHETICAL" labeling, no fabricated data (the UI "renders absence, not an improvised series").
- **Data honesty:** structural (deterministic) vs predictive (ML, gated) signals are visually distinct — never collapsed into one "AI signal" (Reconciliation Determination §13).
- **Theme persistence:** per-operator, via the existing workspace-preferences path.

## 7. Live data presentation decision (Operator, 2026-08-21)

**Approved: Option A — simulated live, clearly labeled, with real broker integration later.**

- The live layer uses the **deterministic simulated feed**, labeled `LIVE:SIMULATED` everywhere (watchlist, chart, live-market dashboard).
- Historical/research data is **real** (B-DATA corpus — OKX + Kraken, hash-pinned, independently verified).
- **No placeholders**: real data, labeled-simulated data, or honest empty states only.
- A **real broker/feed connection is a future governance-gated integration** (deferred since Wave 1); when authorized, the live layer switches from simulated to real with the same honesty discipline (no unlabeled switching).

## 8. Next steps (governance sequence)

1. **ITRGA review** of this blueprint (lifecycle).
2. **Frontend Build Orders** begin — F-00 (hygiene + design-system/theme foundation + wave login) and F-01 (assistant input surface), per the Frontend Roadmap v2.

---

**Approved — Operator (2026-08-21).**
