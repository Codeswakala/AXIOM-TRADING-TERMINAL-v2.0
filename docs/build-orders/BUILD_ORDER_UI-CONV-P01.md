# BUILD ORDER — UI-CONV-P01
## Unified Shell, Command Layer & Operator Sign-In Surface

| Field | Value |
|---|---|
| Instrument type | ITRGA Build Order (Directive §§29–31) — **first phase of the CONVERGENCE programme** |
| Issued by | Independent Technical Review & Governance Authority |
| Issued to | AXIOM Development Authority (DA) |
| Date | 2026-08-13 |
| Authorization | Operator, 2026-08-13 — *"the blueprint is ok … you are authorized to issue the build order"* |
| Governing blueprint | `AXIOM_UI_TRANSFORMATION_BLUEPRINT.md` |
| Confirmed target | **Institutional research terminal · TradingView-class analysis depth · zero execution** |
| Baseline of record | commit `6d98b9f4…` · tag `UI-NEW-P06_DELIVERY` · 160 suites / 704 frontend / 415 backend / **1,119 total** · `index-CVVoXKT4.js` 712.99 kB · Alembic `20260717_0037` |
| Governance Gate | CLOSED · Production NOT CERTIFIED |

---

## 1. Preconditions

**1.1 CA-P03-1 (GA-167) — carried, Operator-owned.** Origin head `GA-166`, `grep -c "GA-167"` = 0. Binds **delivery approval**, not implementation. Work may begin immediately. The DA is **not** to create, edit, or transcribe GA-167.

**1.2 OBS-CERT-2 — corpus at origin.** P05 §10.1 disclosed push rights are Operator-held; that discharged the DA. If unchanged at delivery, state so plainly in §10 and name the holder.

**1.3 F-BRAND-1 — the brand mark is BLOCKED. Read this before touching any logo asset.**

`16_BRAND_GOVERNANCE_STANDARD.md` Part III designates the **AX Monogram** the Official Symbol; Part IV states *"No unofficial logo variants are permitted"* expressly covering **Login Screens**; Part XIII §262 states the visual identity *"shall not be modified except through constitutional approval."*

The Operator-requested compass+Epsilon mark **displaces** the Official Symbol. Therefore:

> **The DA shall NOT implement, substitute, or ship the compass+Epsilon mark in this phase.**
> The existing **AX monogram** is retained in the new login layout and the terminal shell.

Closure requires an Operator-recorded amendment (next free ID **GA-173**) displacing the AX Monogram and amending Doc 16 Parts III/IV/V. On record, the mark becomes a token-level asset swap — one file, no rework. The DA may **prepare** the asset set (`logo.svg`, `logo-light.svg`, `logo-dark.svg`, `logo-horizontal.svg`, `monogram.svg`) **unreferenced and unmounted**, so the swap is instant; preparing files is not adopting them.

---

## 2. Purpose & scope

CONV-P01 establishes the single shell every later phase builds inside, and replaces the sign-in surface.

**IN scope**
1. Unified application shell — one chrome for all authenticated routes; legacy workstation chrome (nav rail, `WORKSPACE CONTEXT` / `RELATED WORKFLOW NAVIGATION` panels, `ACTIVITY TELEMETRY` footer) retired.
2. Single token system — `global.css` `--bg-*` shim retired, all consumption via `var(--ix-*)`.
3. Command palette available on every authenticated route, with route + action targets.
4. Left module rail — icon rail with launchers and badge affordance (badges wire up in SURF-P02).
5. **Operator sign-in surface** redesigned per blueprint §2.3a.
6. `uiconv_p01_shell.test.tsx` + `uiconv_p01_security_invariants.test.ts`.

**OUT of scope — held**
- Absorbing `/charts`, `/signals`, `/analytics` into docks — that is **CONV-P02**.
- Re-homing investigate / scenarios / portfolio-research / research-management / governance / workspace — **CONV-P03**.
- Any indicator, drawing tool, or chart capability — CHART programme.
- Any new backend endpoint, schema, migration or dependency. Alembic stays `20260717_0037`.
- **The compass+Epsilon mark** (§1.3).
- Order entry, order book, depth ladder — permanently excluded (T-1, C-1).

---

## 3. 🔴 B-CONV-1 — One shell, one token system

- Every authenticated route renders inside the unified shell. No route may present the legacy workstation chrome.
- `frontend/src/styles/global.css`: the parallel `--bg-*`, `--border*`, `--text-*`, `--accent` declarations are **retired**; any surviving declaration re-binds to `var(--ix-*)`. This closes the finding I raised in Build Order P06 §4 and advances `TD-005`.
- **Zero ad-hoc hex outside `tokens.css`** across all files this phase touches. Report the whole-frontend count honestly — P06 established the baseline at two files; if others remain untouched by this phase, say so rather than reporting a scoped zero.
- The token values in blueprint §2.1 are binding as `--ix-*` definitions. Raw hex never enters a component.

## 4. 🔴 B-CONV-2 — The sign-in surface is a governance surface

Reference `mockups/06_login_3d.png`. Layout is authorised; the following are requirements, not styling suggestions.

- **The decorative chart scene renders no market data.** It is generated ornament and must be recognisably decorative. It must never read as a live or seeded price display (T-6). No axis labels, no price values, no timestamps, no symbol names in the artwork.
- **Governance chips render pre-authentication**: `GATE: CLOSED · RESEARCH-ONLY · NON-ACTUATING`. The Gate state is disclosed before sign-in.
- **No credential hints.** No demo credentials, no placeholder usernames resembling real accounts, no bootstrap-operator autofill. `TD-AXIOM-DEV-CREDENTIAL-LITERALS` is a Doc 11 §2 pre-certification blocker; this surface must not widen it.
- **`prefers-reduced-motion` honoured** — animation degrades to a static gradient.
- **WCAG AA** contrast for all form labels, inputs, and the tagline over imagery. Labels must not sit over the busy region.
- Password reveal toggle is keyboard reachable with a discernible accessible name.
- Failed authentication renders an explicit error. Never an optimistic or ambiguous state (the B-P05-4 rule, applied to auth).
- **AX monogram only** (§1.3).

## 5. 🔴 B-CONV-3 — The command palette is the navigation spine

The hybrid topology depends on it, since the legacy nav rail is being retired.

- Reachable from every authenticated route by keyboard (`Ctrl/Cmd-K`) and by the header control.
- Targets **all 16 registered routes** plus in-app actions, each with a category and keyboard hint.
- Fully keyboard operable: open, filter, arrow-navigate, enter, escape. Focus returns to the invoking element on close.
- **No actuating target may ever appear** — no execute, no order, no broker, no position (T-1). Palette entries are navigation and research actions only.
- Empty-state and no-match states are explicit.

## 6. 🔴 B-CONV-4 — Retire, do not orphan

Retiring the legacy chrome must not strand functionality. This is the CA-P03-4 lesson at programme scale.

- Every capability reachable from the legacy chrome must remain reachable in the new shell — via rail, dock, palette, or full-surface route.
- Produce a **reachability table**: legacy affordance → new location → evidence. Any capability with no new home is a **deviation** and must be recorded, not dropped.
- No route may 404 or render blank. Routes awaiting CONV-P02/P03 render inside the new shell with their existing page content — visually unified even if not yet re-homed.
- Deep links and browser back/forward continue to work.

## 7. 🔴 B-CONV-5 — Constitutional constraints, unchanged

- **T-1** — zero actuation affordance anywhere in shell, palette, rail, or login.
- **C-1** — no order book, depth ladder, bid/ask size. Permanently excluded.
- **T-4 / T-5** — no external LLM generates, summarises or rewrites any operator-facing content, including palette suggestions.
- **Doc 16 B-7** — never colour alone; status carries text or shape.
- **Principle 1** — no statistic rendered without its uncertainty; **every interval brackets its own point estimate**. No new statistic is introduced this phase, but the invariant test must continue to pass.

## 8. Conditions carried

| ID | Condition | Status in CONV-P01 |
|---|---|---|
| CA-P03-1 | GA-167 unrecorded | **Blocks delivery approval** — Operator |
| OBS-CERT-2 | Corpus not at origin | Declare status in §10 — Operator |
| F-BRAND-1 | Compass+Epsilon mark | **Blocked pending GA-173** (§1.3) |
| OBS-CERT-3 | `global.css` shim, `PriceChart.tsx` fallbacks | `global.css` closes here; `PriceChart.tsx` in CONV-P02 |
| OBS-P06-3 | Surface `updated_at`, not only `[EDITED]` | Recommended, not required |
| OBS-5 | Cumulative bundle +62.97 kB | Disclose delta; justify if > +30 kB |

## 9. Mandatory named tests

Seven, displayed **passing by name** under the Vitest verbose reporter, in `uiconv_p01_shell.test.tsx`:

1. `test_uiconv_p01_all_authenticated_routes_render_in_unified_shell_without_legacy_chrome`
2. `test_uiconv_p01_zero_adhoc_hex_outside_tokens_css_in_all_touched_files`
3. `test_uiconv_p01_command_palette_reaches_every_registered_route_by_keyboard`
4. `test_uiconv_p01_command_palette_exposes_no_actuating_or_order_target`
5. `test_uiconv_p01_login_renders_governance_chips_and_no_credential_hints`
6. `test_uiconv_p01_login_decorative_scene_renders_no_market_data_values`
7. `test_uiconv_p01_every_legacy_affordance_remains_reachable_in_new_shell`

Plus `uiconv_p01_security_invariants.test.ts` (T-1, T-4, T-5, T-6, T-7, S-1…S-5, C-1) and the carried programme invariant `every_rendered_interval_brackets_its_own_point_estimate`.

**Floors, not targets.**

## 10. Mandatory evidence

(a) Delivery commit + annotated tag `UI-CONV-P01_DELIVERY`, `git rev-parse` output; state origin-push status plainly (§1.2).
(b) SHA-256 for **every** created and modified file. No placeholders.
(c) Suite counts against **the delivered commit**, fresh transcript. Bundle hash **must** differ from `index-CVVoXKT4.js` / 712.99 kB. Every named test claimed must appear in the transcript.
(d) Raw whole-frontend grep transcripts: T-1, T-4/T-5, C-1, secrets, `dangerouslySetInnerHTML`/`eval`/`new Function`, ad-hoc hex. Honest counts — a scoped zero will be treated as incorrectly scoped.
(e) **B-CONV-4 reachability table** — legacy affordance → new location → evidence.
(f) **Level-I captures at 1920×1080, attached as image files**: (i) login surface; (ii) login with a failed-auth error; (iii) terminal root in the unified shell; (iv) a previously-legacy route rendering in the new shell; (v) command palette open with results; (vi) reduced-motion or light-theme variant of the login.
(g) Deviation register — if zero, state zero and mean it. **Any orphaned capability from §6 belongs here.**
(h) Technical debt reconciliation, verbatim quotations, correct line numbers; `TD-005` status updated.
(i) Explicit statement that the compass+Epsilon mark was **not** implemented, per §1.3.

## 11. Acceptance criteria

Approvable when: B-CONV-1…B-CONV-5 satisfied; seven named tests display passing; the 1,119-test baseline maintained or grown with zero regression; `tsc -b` and `vite build` exit 0 against the delivered commit; Alembic head unchanged; evidence (a)–(i) complete; **and CA-P03-1 closed by the Operator.**

## 12. Authorization

The DA is authorized to implement UI-CONV-P01 as scoped above, effective immediately.

Where a mockup and a governing document disagree, **the governing document wins** — the mockups in `/home/user/mockups/` are visual reference, not specification. This Build Order is not an approval of any future delivery. Correction is not approval. The DA may not self-approve. The Governance Gate remains **CLOSED**; production remains **NOT CERTIFIED**; no CONV-P02 implementation may begin before its Build Order is formally issued.

**We don't guess. We prove.**

*— AXIOM ITRGA*
