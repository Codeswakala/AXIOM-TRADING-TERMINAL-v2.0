# DELIVERY REPORT — BO-F-00
## Design-System Foundation, Six-Theme System & Animated Wave Login

| Item | Value |
|------|-------|
| Build Order | `BO-F-00` (Operator-authorized; Blueprint approved by the Operator 2026-08-21 with refinements: all six themes · wave login · simulated live) |
| Predecessors | B-00 → B-07 CLOSED · X-01 Backend Tier delivered · `VISUAL_BLUEPRINT.md` APPROVED |
| Implementer | Development Authority (DA) |
| Deliverable class | Frontend implementation unit (chain position 30) |
| Governance Gate | CLOSED · Production NOT CERTIFIED (unchanged) |
| Determination | Awaiting ITRGA independent determination (BO §12) |

---

## 1. Claimed scope vs. this Build Order

Executed exactly BO-F-00 §2: F-00.1 six-theme system, F-00.2 animated wave login,
F-00.3 hygiene (favicon, `<h1>`, router-flag decision, supply chain). §3
exclusions honored: no shell re-architecture, no F-01 → F-06, **no pixel-matching
of the AI-generated prototypes** (the Blueprint §2 token language is the spec —
executed from the token table, not from the PNGs), no new brand colors (Teal/Amber
accents are presentation-only per Blueprint §3), no broker integration, no gate
weakening, no repo publication. §6 allowed-files: every touched file is in the
allowed set except the three plumbing files disclosed in §8 (D3).

## 2. What changed (files + SHAs + chain position)

Patch `f00.patch` — **chain position 30**, 16 files (15 modified + 1 new), zero
backend files. Applies clean onto `34f4c62` + elements 1–29 (transcript
`f00_applycheck_transcript.txt`). Post-apply `cmp` 16/16. Patch sha256:
`50d0e6558a490d169022f0eeac28de8be59bebc221292b33238abcb52a1c76b9`.

| File | Change |
|---|---|
| `frontend/src/workstation/design/tokens.css` | Tier-5 override blocks: `.theme-slate`, `.theme-teal`, `.theme-amber`, `.theme-high-contrast` (token-level, colors only) + light-theme focus-ring fix |
| `frontend/src/workstation/design/theme.ts` | BO-F-00 six-theme registry: `THEME_IDS`, `THEME_META` (RGB-triple form), `normalizeThemeId`, `nextThemeId`, `themeClassName`, `rgbToHex` |
| `frontend/src/workstation/overlays/OverlayProvider.tsx` | Theme state widened to the six-theme vocabulary; `toggleTheme` = fixed cycle; new `setTheme(id)` |
| `frontend/src/workstation/persistence/shellPreferences.ts` | `themeMode: ThemeId`; read-boundary normalization (legacy `dark` → `midnight`) |
| `frontend/src/workstation/components/InstitutionalWorkspaceShell.tsx` | Restore path uses `setTheme`; header toggle labels current theme (`Theme: Midnight`, `data-theme-id`) |
| `frontend/src/pages/LoginPage.tsx` + `.css` | Wave composition: two perspective candle rows (16 candles), 12-particle drift field, glow pulse; CSS-only transform/opacity keyframes; reduced-motion freeze covering every animated layer |
| `frontend/index.html` | Favicon link → `/branding/axiom-logo.png` (the shipped brand asset; no new asset) |
| `frontend/src/components/terminal/TradingTerminalWorkspace.tsx` | Visually-hidden landing `<h1>` (`operations-landing-h1`) — OBS-CAPASSESS-H1 closed |
| `frontend/src/main.tsx` | Router future flags **Option A** (both flags opted in) |
| `frontend/package.json` + `package-lock.json` | `overrides: {"nanoid": "^3.3.18"}` → nanoid 3.3.18; HIGH cleared |
| `frontend/src/test/f00_design_system.test.tsx` | **New** — 29 tests (registry, CSS pinning, contrast, persistence round-trip, switcher cycle, wave pins, hygiene pins) |
| `frontend/src/workstation/navigation/WorkspaceNavigationSeam.test.tsx`, `frontend/src/workstation/persistence/shellPreferences.test.ts` | 2 spec-driven churns: `"dark"` → `"midnight"` with inline BO-F-00 supersession comments |
| `docs/governance/TECHNICAL_DEBT_REGISTER.md` | TD-F00-UNIT + OBS-F00-1/2/3 rows; TD-UI-CAPASSESS-NANOID-HIGH CLOSED; OBS-CAPASSESS-H1 CLOSED |

## 3. Theme system description

- **Vocabulary:** Midnight (default) · Light · Slate · Teal · Amber · High-Contrast.
- **Mechanism:** Tier-5 token overrides on `.ix-shell.theme-*` — colors only;
  layout/density/typography/governance framing identical across themes. Midnight
  is the `:root` default (no override block). The `.theme-light` pattern was the
  template; the four new blocks mirror its token set exactly (surfaces, borders,
  text tiers, input/table backgrounds, shadow/elevation, plus accent/focus
  overrides where the Blueprint defines them).
- **Palette (binding, Blueprint §2/§3):** Midnight `#0b0e14`/`#111822`/`#3b82f6`;
  Light `#f8fafc` surfaces, same blue accent; Slate mid-gray panels, reduced blue
  accent (`#60a5fa`); Teal navy/teal with `#22d3ee` active states; Amber warm dark
  with `#f59e0b` active states (presentation-only, Operator-authorized);
  High-Contrast `#000`/`#fff`, full-saturation semantics (`#34d399`/`#fbbf24`/
  `#f87171`), yellow focus.
- **Registry:** `theme.ts` carries the values as **RGB triples** (never hex/rgba
  string literals) so the constitutional "no ad-hoc color literals outside
  tokens.css" rule holds mechanically; tests convert triples via `rgbToHex` and
  pin them 1:1 against the CSS blocks. The theme set is a closed enumerated
  record — arbitrary third-party styling is impossible by construction.
- **Persistence:** per-operator via the existing workspace-preferences path
  (`theme_config.mode`, normalized at the read boundary; legacy `dark` →
  `midnight`; unknown → `midnight`). The header toggle cycles the fixed order;
  the command palette action reuses the same cycle. **Level-I probe:** Slate
  survives a reload AND a full sign-out/sign-in (server-side
  `PUT /institutional-platform/workspace-preferences` observed in the backend
  log); all six themes verified in-browser with the computed `--ix-bg-root`
  sampled (`#0b0e14`, `#f8fafc`, `#1f2733`, `#0c1520`, `#14120c`, `#000000`).
- **Accessibility:** every theme ≥ WCAG AA from the registry values (contrast
  asserted per theme in tests); High-Contrast meets AAA (≥7:1 all text tiers);
  the light theme additionally gained a focus-ring fix (`--ix-color-focus:
  #2563eb` — the inherited `#8cc2ff` is ~1.6:1 on light surfaces, below the 3:1
  non-text floor).

## 4. Wave-login implementation

- **Composition:** two candle rows in perspective (far row: deeper/dimmer/slower,
  near row: larger/brighter/faster; 16 candles total, each riding its own phase)
  drifting across the lower third; a 12-particle ambient drift field; an ambient
  glow pulse on the horizon.
- **Technique:** CSS 3D + keyframes only — every animation animates
  transform/opacity/translate (GPU-composited), zero WebGL, zero new
  dependencies (Doc 09 §12 respected), zero asset budget.
- **Binding constraints:** (1) decorative only — the scene subtree's textContent
  is empty (test-pinned) and carries no `data-price`/`data-timestamp`; (2)
  `prefers-reduced-motion: reduce` freezes every animated layer via the
  dedicated block (test-pinned; no later rule re-enables animation);
  (3) performance — no sign-in delay, no layout churn; (4) governance chips
  remain on the login surface (capture-verified: `GATE: CLOSED · RESEARCH-ONLY ·
  NON-ACTUATING`).
- **Motion evidence:** two motion frames 700ms apart differ (animation runs);
  two reduced-motion frames 700ms apart are byte-identical (frozen) —
  `f00_login_wave_t1/t2.png`, `f00_login_frozen_t1/t2.png` (sha256 pairs in the
  capture log).

## 5. Hygiene items closed

1. **Favicon** — `index.html` links `/branding/axiom-logo.png` (the Operator-
   supplied brand asset already shipped; no new asset, brand-exact). Level-I:
   `link[rel=icon]` present, asset fetch → **HTTP 200**.
2. **Landing `<h1>`** — the `/` operations surface now carries a visually-hidden
   `<h1>` ("AXIOM Institutional Trading Terminal — Operations") so the heading
   outline is complete without changing terminal density. OBS-CAPASSESS-H1
   CLOSED (test-pinned + capture).
3. **Router-flag decision — Option A (opt-in).** Both `v7_startTransition` and
   `v7_relativeSplatPath` are explicitly enabled on the `BrowserRouter` in
   `main.tsx`, with the rationale comment. Source-pinned by test. (Not Option B:
   no new technical debt created.)
4. **Supply chain** — nanoid HIGH (GHSA-2v37-7h3g-55p8) resolved via
   `overrides` → 3.3.18 (lockfile regenerated; `npm ls nanoid` shows
   `3.3.18 overridden`); **`npm audit --audit-level=high` exit 0** — the
   remediation gate (TD-UI-POSTCSS-HIGH standard) restored;
   TD-UI-CAPASSESS-NANOID-HIGH CLOSED. Remaining: react-router +
   react-router-dom **MODERATE** (CVE-2025-68470 bypass — fixed only in
   ≥7.18.0; GHSA-jjmj — 6.30.2–6.30.4) — **accepted exceptions per the B-00.2
   severity/exception policy** (OBS-F00-2): a react-router 6→7 major migration
   is a framework-level activity deferred to a dedicated order; in-product
   exposure is nil (internal registry paths only, no user-controlled navigation
   targets).

## 6. Screenshot evidence (Level-I captures, `docs/evidence/f00/`)

| Capture | File | Result |
|---|---|---|
| Wave motion t1 / t2 | `f00_login_wave_t1.png` / `_t2.png` | sha256 **differ** → animation runs |
| Wave frozen t1 / t2 | `f00_login_frozen_t1.png` / `_t2.png` | sha256 **identical** → frozen under reduced-motion |
| Theme: Midnight | `f00_theme_midnight_home.png` | `--ix-bg-root` = `#0b0e14` |
| Theme: Light | `f00_theme_light_home.png` | `--ix-bg-root` = `#f8fafc` |
| Theme: Slate | `f00_theme_slate_home.png` | `--ix-bg-root` = `#1f2733` |
| Theme: Teal | `f00_theme_teal_home.png` | `--ix-bg-root` = `#0c1520` |
| Theme: Amber | `f00_theme_amber_home.png` | `--ix-bg-root` = `#14120c` |
| Theme: High-Contrast | `f00_theme_highcontrast_home.png` | `--ix-bg-root` = `#000000` |
| Persistence re-login | `f00_persistence_relogin.png` | Slate restored after full sign-out/sign-in |
| Probe log | `f00_capture_log.txt` | All assertions + frame hashes |

The DA cannot visually inspect imagery (no vision capability this session);
per BO §3 the prototypes are excluded from conformance and the token language is
the spec, so every visual claim above is machine-verified (computed token
values, class application, pixel-hash motion/freeze comparisons) rather than
eye-checked — stated for honesty.

## 7. Test evidence (executed)

- Workspace: **889 passed / 176 files** (860 floor + 29 new F-00 tests),
  168.16s, exit 0 — `f00_vitest_fullsuite.log`.
- Typecheck: `tsc -b` exit 0, zero diagnostics — `f00_tsc.log`.
- Production build: `npm run build` exit 0 (chunk-size warning pre-existing).
- **Clone-side (gold standard):** pristine baseline clone → 30 elements applied →
  `npm ci` from the patched lockfile → `tsc -b` exit 0 → **889 passed / 176
  files** → `npm audit --audit-level=high` exit 0. The patch and lockfile are
  self-consistent from zero.
- New tests cover every BO §8 acceptance line: theme token presence (CSS ↔
  registry hex pinning), switcher cycle + setTheme, persistence round-trip +
  legacy normalization, WCAG AA (AAA for High-Contrast) contrast per theme,
  wave composition + zero-data-strings + reduced-motion freeze + transform-only
  motion, favicon link + asset existence, router-flag pin, landing `<h1>`.

## 8. Deviations register

| ID | Deviation | Assessment |
|----|-----------|------------|
| D1 | Light-theme focus token changed (`#2563eb`) | Spec-driven (Blueprint §3: every theme meets WCAG AA); the inherited `#8cc2ff` focus fails 3:1 on light surfaces. Disclosed in the CSS comment + register. |
| D2 | Two test pins churned (`"dark"` → `"midnight"`) | Spec-superseded by the six-theme vocabulary; inline BO-F-00 supersession comments; stricter (normalization tested). |
| D3 | Three plumbing files outside the §6 allowed list were touched: `OverlayProvider.tsx` (theme state), `InstitutionalWorkspaceShell.tsx` (restore/button), and the two existing test files (churn sites) | Required by the acceptance criteria ("theme switcher works; per-operator persistence") — the theme state's only home is the overlay controller, which the shell consumes. Minimal diffs, no behavior beyond theming. |
| D4 | Registry stores colors as RGB triples, not hex strings | Required by the binding "no color literals outside tokens.css" tests; exact values preserved, conversion tested. |
| D5 | `frontend/tsconfig.tsbuildinfo` excluded from the patch | Tracked-but-ignored build cache regenerated on every tsc run; not an artifact-chain file. |
| D6 | The DA cannot view the prototype PNGs | Non-issue for conformance: BO §3 excludes pixel-matching; the Blueprint token language is the spec; all visual claims are machine-verified (computed tokens, pixel-hash comparisons). |

## 9. Transmission manifest (relay-accurate, CA-TRANSMIT-1)

All files newly transmitted with this delivery; byte-identical `.txt` copies in
`/home/user/f00_transmission/`, cmp-verified; hashes mechanically verified
against the folder before this message (sha256sum -c MANIFEST.txt exit 0). This
report's own sha256 is declared in the DA's closing message (self-referential
hash rule); `MANIFEST.txt` carries it.

| # | File | sha256 |
|---|---|---|
| 1 | `f00_transmission/f00.patch.txt` | `50d0e6558a490d169022f0eeac28de8be59bebc221292b33238abcb52a1c76b9` |
| 2 | `f00_transmission/f00_applycheck_transcript.txt` | `661d32b970513a89889e922fb814118d87b77936c459b5fa0b5b7f3437fd1b82` |
| 3 | `f00_transmission/f00_audit.log.txt` | `587affec4489105f9e9be73b63c54472b01fc16f7e95c995bd6f94af8a9c03c7` |
| 4 | `f00_transmission/f00_capture_log.txt` | `d5691ace752c6dfd15cf90668cac15fdb2a1deb763b745beef24d23ba3bc2987` |
| 5 | `f00_transmission/f00_login_frozen_t1.png` | `6db184cb246fe0dce847dd711b7308c36b5c0238f49bff995e8ed972c68910ec` |
| 6 | `f00_transmission/f00_login_frozen_t2.png` | `6db184cb246fe0dce847dd711b7308c36b5c0238f49bff995e8ed972c68910ec` |
| 7 | `f00_transmission/f00_login_wave_t1.png` | `84251c06b06f8c862f65618ce5fd7cf0d34fbd39132cfed9deba0902b48d4550` |
| 8 | `f00_transmission/f00_login_wave_t2.png` | `eca2e88b1471b4906466860bf069d4a6cb23d444d6816ec6ec88b862988ca64b` |
| 9 | `f00_transmission/f00_persistence_relogin.png` | `e36d414bff2863cd5f28e63669376031afa70cc3d59cd5d7462f80ec9616ed0e` |
| 10 | `f00_transmission/f00_theme_amber_home.png` | `4b2a38ea0ced2980947a9c2e019ed18994a1119ed7199681e87bcd592b6755a2` |
| 11 | `f00_transmission/f00_theme_highcontrast_home.png` | `bd63df9ab823b1943e7855767a7b15cf2f82ae90bd054d444cfb0445199c37d8` |
| 12 | `f00_transmission/f00_theme_light_home.png` | `f3caec81cd0cc8f4be50c8aa15b88f71ac7f9010f13160c7c2b0f9fa35a53056` |
| 13 | `f00_transmission/f00_theme_midnight_home.png` | `70557576724b9d7e3a3808fecdd1c4ce2f474da57dcdebf9c313cb644e70a278` |
| 14 | `f00_transmission/f00_theme_slate_home.png` | `a9725d58444bc889aa99d0e4bbdef7f344df538a04f881b023d803253195db9c` |
| 15 | `f00_transmission/f00_theme_teal_home.png` | `f950c7375c3dfe8238920e01b83380b625091f64710d224d58451ea5587315d3` |
| 16 | `f00_transmission/f00_tsc.log.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 17 | `f00_transmission/f00_vitest_fullsuite.log.txt` | `5317c2190bafc4dfc134cf9cff97aa3a6c295700a4c0e21831f3ace5b7fc71a4` |

## 10. Known limitations / technical debt

- **OBS-F00-1 (backend, carried):** under the capture probe's concurrent dev
  load, two `audit append failed … no such savepoint` lines appeared
  (ws-ticket audit rows lost, endpoints still 200). Pre-existing, out of F-00
  scope (frontend-only unit); recorded for Operator/ITRGA routing — candidate
  for a future backend hardening order.
- **OBS-F00-2:** the two react-router MODERATE advisories are accepted
  exceptions pending a dedicated RR7 migration order.
- **OBS-F00-3 (custody):** the remote repository history was rewritten to a
  single commit `7e4d993` (Operator-published snapshot of the delivered state;
  its register is an older version missing delivered rows). The DA baseline
  declaration (`34f4c62` + chain) is unchanged; verification continues against
  the local object database. The Operator may wish to reconcile the remote's
  register copy.
- The theme switcher is a cycle button + settings JSON field (six steps max);
  a dedicated theme picker menu is a possible future polish item (not
  requested in BO-F-00).
- Per-operator theme persistence shares the existing shell preference record
  (`institutional-shell-v1`); the write is debounced 250ms server-side.

---

**Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.**
