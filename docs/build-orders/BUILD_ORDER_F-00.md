# AXIOM — BUILD ORDER F-00
## Design-System Foundation, Six-Theme System & Animated Wave Login

| Item | Value |
|------|-------|
| Build Order ID | `BO-F-00` |
| Programme | Frontend Operationalization (per Visual Blueprint, Operator-approved 2026-08-21) |
| Authorizing authority | **Operator** (Blueprint approval + three decisions: wave login · all six themes · simulated live) |
| Predecessors | Backend B-00 → B-07 + X-01 Backend Tier (complete) · Visual Blueprint (approved) |
| Governing documents | `VISUAL_BLUEPRINT.md` (this order's design authority) · `08_UI_UX_SPEC.md` · `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` · `16_BRAND_GOVERNANCE_STANDARD.md` · `FRONTEND_ROADMAP_v2.md` §F-00 |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and framing

This is the **first frontend unit** and it establishes the design foundation that every later F-unit builds on. It implements the Operator's three approved decisions:

1. **Six-theme system** (Midnight default, Light, Slate, Teal, Amber, High-Contrast) — token-level color overrides, per-operator preference, brand identity unchanged.
2. **Animated "wave" login** — the decorative scene animates via CSS 3D/keyframes, `prefers-reduced-motion`-frozen, decorative-only (no market data).
3. **Hygiene** carried from the earlier review: favicon, landing `<h1>`, React Router future-flags, supply-chain bump.

The existing frontend already provides the **correct foundation** (verified): the `--ix-*` token system in `src/workstation/design/tokens.css`, a `.theme-light` override, the blue/amber color tokens, and a static login decorative scene (`deco-candle` elements). This order **extends and completes** that foundation — it does not replace the working terminal shell.

---

## 1. Objective

1. Deliver a complete six-theme system (token-level, per-operator, accessible).
2. Deliver the animated wave login (decorative, reduced-motion-safe, performant).
3. Close the carried hygiene items (favicon, `<h1>`, router flags, supply chain).

---

## 2. Scope

### F-00.1 — Six-theme system

- **Themes:** Midnight (default) · Light · Slate · Teal · Amber · High-Contrast.
- **Mechanism:** each theme is a **token-level override** in `tokens.css` (colors only). Layout, density, typography, and governance framing are identical across themes. The existing `.theme-light` pattern is the template; add `.theme-slate`, `.theme-teal`, `.theme-amber`, `.theme-high-contrast`, and keep Midnight as the root default.
- **Palette (binding, Blueprint §6):**
  - Midnight — `#0b0e14` bg / `#111822` panels / `#3b82f6` accent.
  - Light — `#f8fafc` surfaces / dark text / same blue accent.
  - Slate — mid-gray panels, *reduced* blue accent.
  - Teal — navy/teal, `#22d3ee` accent for active states.
  - Amber — warm dark, `#f59e0b` accent for active states (presentation-only, Operator-authorized).
  - High-Contrast — `#000`/`#fff`, full-saturation semantics, WCAG AAA.
- **Persistence:** per-operator theme preference via the existing workspace-preferences path (not a global switch). Default Midnight for unset.
- **Accessibility:** every theme meets WCAG AA; High-Contrast meets AAA. Theme switch must not break contrast or keyboard/focus states.

### F-00.2 — Animated wave login

- **Composition:** the approved "wave" concept — candles flowing across the lower third in perspective, drifting particles, glow pulse.
- **Technique:** CSS 3D transforms + keyframes (no WebGL, no new dependency — Doc 09 §12). Animate the existing `deco-candle`/scene elements into a wave motion with depth (translate/rotate + perspective), plus particle drift and an ambient glow pulse.
- **Binding constraints (Blueprint §4):**
  1. **Decorative only** — zero real/seeded market data (no prices, axes, timestamps).
  2. **`prefers-reduced-motion: reduce`** freezes to a static frame (the existing global rule in `tokens.css` is honored; the login must not override it).
  3. **Performance** — no sign-in delay; ≤ ~1MB asset budget; animation off the main thread (transform/opacity only, GPU-composited).
  4. Governance chips ("GATE CLOSED · RESEARCH-ONLY · NON-ACTUATING") remain on the login surface.

### F-00.3 — Hygiene (carried)

- Favicon wiring (currently 404 — Doc 16 §XI).
- Landing `<h1>` on the operations surface (heading-outline gap).
- React Router v7 future-flags: **explicit Option A or B** — opt in (`v7_startTransition`, `v7_relativeSplatPath`) **or** record as explicit technical debt. State the choice.
- Frontend supply-chain: resolve the `react-router-dom`/`react-router`/`postcss` advisories (severity/exception policy per B-00.2), re-run audit to the documented standard.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** re-architecture of the working terminal shell, registry, or routing (the design language is applied via tokens/themes, not by rebuilding structure).
- **No** implementation of F-01 → F-06 (assistant input, intelligence/alerts/lineage presentation) — those are separate orders.
- **No** pixel-matching of AI-generated images — the prototypes are the *direction*; the design language (§2 tokens/colors/density/framing) is the spec.
- **No** new primary brand colors in brand identity (theme accents are presentation-only, per Blueprint §3).
- **No** real broker/feed integration (live layer stays simulated; per Blueprint §7).
- **No** weakening of non-actuation, RBAC, or accessibility.
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. Six-theme token overrides + theme switcher (per-operator persistence).
2. Animated wave login (reduced-motion-safe).
3. Favicon + `<h1>` + router-flag decision + supply-chain resolution.
4. Tests (new/churn): theme token presence per theme, contrast, theme persistence, reduced-motion freeze, login scene has no data strings.
5. Delivery Report (§8) with relay-accurate transmission manifest.

---

## 5. Dependencies

- **Upstream:** Visual Blueprint (approved) · existing frontend shell + token system (verified present).
- **Downstream:** F-01 → F-06 inherit this design language and theme system.

---

## 6. Allowed files / components

- `frontend/src/workstation/design/tokens.css` (theme overrides).
- `frontend/src/workstation/design/theme.ts` (if a TS theme registry is used).
- `frontend/src/pages/LoginPage.tsx` + `LoginPage.css` (wave animation).
- `frontend/src/workstation/persistence/*` + theme-preference plumbing (if needed).
- `frontend/index.html` (favicon link).
- `frontend/public/branding/*` (favicon asset).
- `frontend/package.json` + lockfile (supply-chain bump only).
- `frontend/src/**` (the landing `<h1>` fix).
- `frontend/src/test/**` + relevant `*.test.tsx` (new/churn tests).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- No secrets/credentials; no new external runtime dependency (the wave login is CSS-only).
- Supply-chain changes follow the B-00.2 severity/exception policy (no unaccepted critical/high; exceptions documented).
- Accessibility and non-actuation invariants unchanged; the login scene must not fetch or render any market data.
- Theme system must not introduce a mechanism for arbitrary third-party styling (themes are a fixed, enumerated set).

---

## 8. Acceptance criteria

- [ ] Six themes defined as token overrides; each theme's token presence test-pinned.
- [ ] Theme switcher works; per-operator persistence verified (re-login restores theme).
- [ ] All themes meet WCAG AA (High-Contrast AAA) — contrast asserted.
- [ ] Wave login animated; `prefers-reduced-motion: reduce` freezes it (test-pinned).
- [ ] Login scene contains **no** market-data strings/values (test-pinned).
- [ ] Favicon wired (no 404); landing `<h1>` present; router-flag decision stated; supply chain resolved to the documented standard.
- [ ] Full frontend suite green (`npm test`) + typecheck (`tsc -b`) green; executed output supplied.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1, hard gate)

**Binding (CA-TRANSMIT-1):** artifacts uploaded and confirmed against the review channel. A declared-but-untransmitted artifact is an automatic CORRECTION REQUIRED.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed frontend test output + typecheck | Level II | run transcript |
| Screenshot captures: each theme + wave login (frozen + motion frame) | Level I | images |
| Theme-persistence probe (re-login) | Level I | probe output |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Theme system description (each theme's token set + persistence mechanism)
4. Wave-login implementation (animation approach + reduced-motion + performance)
5. Hygiene items closed (favicon / H1 / router-flag decision / supply chain)
6. Screenshot evidence (themes + login)
7. Test evidence (executed)
8. Deviations register
9. Transmission manifest (relay-accurate)
10. Known limitations / technical debt

---

## 11. Rollback / containment

- Theme overrides and the login animation are CSS/component changes; revert = revert patch.
- No backend change, no schema change, no new runtime dependency.
- A theme can be disabled via config if it regresses accessibility.

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified, the Delivery Report submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of F-00, **F-01 (assistant input surface)** may be issued — the backend seam (`POST /collaboration/assistant-respond`) already exists from B-06.

---

**End of Build Order F-00**
