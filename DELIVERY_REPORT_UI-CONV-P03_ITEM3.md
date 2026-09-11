# DELIVERY REPORT — UI-CONV-P03 · ITEM 3
## WorkspaceCustomizationPage → Shell-Owned Settings Overlay (+ OBS-CONV3-3 fold-in)

| Field | Value |
|---|---|
| Document type | DA Item Delivery Report (Directive §§29–31; Doc 17 §17.8 Gate 4) |
| Issued by | AXIOM Development Authority (DA) |
| Issued to | Independent Technical Review & Governance Authority (ITRGA) & Operator |
| Date | 2026-08-15 |
| Governing instrument | `BUILD_DIRECTIVE_UI-CONV-P03_ITEM3.md` (ITRGA) — scopes item 3 only |
| Parent Build Order | `BUILD_ORDER_UI-CONV-P03` (not amended) |
| Base | `34f4c62dbef11e685de965415b4b8ab697cef487` (AXIOM-TRADING-TERMINAL-v1.0, sole baseline) |
| Transport | No commits/pushes per Operator instruction — patch is a `git diff`-based artifact, verified byte-clean at the stated base (deviation from the directive's `format-patch` form disclosed in §8) |
| Governance Gate | **CLOSED** · Production **NOT CERTIFIED** |

---

## 1. Chosen home + reasoning (directive §3)

**Home: a shell-owned Settings overlay in the overlay layer** — `components/terminal/settings/WorkspaceSettingsOverlay.tsx`, mounted by `OverlayLayer`, opened by:

1. a **Settings button in the global command header** (`shell-settings-btn`),
2. the **left module rail** (its Settings entry navigates to `/workspace`, which redirects),
3. the **deep link `/?open=settings`** (target of the `/workspace` legacy-route redirect).

**Reasoning, against each candidate:**

| Candidate | Verdict |
|---|---|
| Bottom-dock tab | **Rejected.** Five research tabs (TRADE_PLANS\|JOURNAL\|RISK\|SCENARIOS\|PORTFOLIO) serve research-content browsing; settings carry a different intent (operator configuration) and lifecycle (persisted mutations, not research artifacts). The directive pre-excluded this unless I disagree — I agree. |
| Right dock (320 px) | **Rejected.** The preference editor's five labeled fields (key, layout JSON, modules, theme JSON, metadata JSON) need width the dock cannot provide; compression would make capabilities harder to reach (turn-56 violation). |
| Primary stage (`?view=settings`) | **Rejected.** The stage is reserved for research-scale surfaces (`chart` \| `research`) per ITRGA's verified constraints; a settings page is not research-scale. |
| Shell overlay | **Chosen.** The shell already owns an overlay layer with the exact modal pattern (CommandPalette, GlobalSearchOverlay, GlobalDialogLayer) — the settings surface joins it with zero new architecture, remains reachable from everywhere in the shell, and preserves the Settings navigation category in the registry. |

**Layering note (self-disclosed):** the first implementation placed the self-fetching container under `src/workstation/` — the shell-purity governance test (`test_shell_hosts_only_no_business_logic_in_shell`) correctly failed it, because the workstation layer may not carry API business logic. The module was **relocated** to `components/terminal/settings/` (the same layer as the dock panels that fetch); the governance test now passes unmodified. The test's rule, not the test, was honoured.

---

## 2. Capability disposition table (directive §1 inventory)

| Capability group | New location | Evidence |
|---|---|---|
| Workspace Customization (frame) | `WorkspaceCustomizationWorkspace` (relocated export, same name/contract) rendered inside the overlay body | `workspace-settings-surface` testid; relocated test suite green |
| Preference Editor | Editor section — all five fields, both mutation controls | `workspace-preference-editor`, `workspace-pref-create-btn`, `workspace-pref-update-btn` |
| Saved Preferences | Saved list — cards clickable to load into the editor | `workspace-saved-preferences`, `workspace-pref-card-{id}` |
| Preference Detail (`{selected.workspace_key}`) | Detail panel — operator, status, modules, theme | `workspace-preference-detail` |
| Empty state (line 171, verbatim) | **Preserved verbatim** — "No workspace preferences have been saved for this operator." | `workspace-preferences-empty`; capture 01 (text extracted from DOM); test asserts verbatim text |
| Refresh affordance | Refresh button re-invoking the fetch | `workspace-pref-refresh-btn` |
| Both persisted mutations | **Create** and **Update** wired to `createWorkspacePreference` / `updateWorkspacePreference` | M1 tests (below) + capture 02 shows both buttons |

**No capability removed or re-scoped.** The page's container logic (fetch + create + update + explicit errors) moved into `WorkspaceSettingsOverlay`; the presentational component is **relocated** with its export name and props contract unchanged so existing consumers bind without change.

---

## 3. Mandatory requirements M1–M4

| Requirement | Status | Evidence |
|---|---|---|
| **M1 — both mutations survive re-homing** | **CONFIRMED.** `createWorkspacePreference` and `updateWorkspacePreference` are both reachable from the overlay and wired exactly as on the page: create prepends the returned row; update replaces by `preference_id`. | Tests `test_uiconv_p03_settings_create_mutation_round_trips_and_appends_after_response` and `..._update_mutation_replaces_row_after_response` — both assert the API was called and the list updated **only after** the resolved response. |
| **M2 — explicit error surfacing, never silent, never optimistic** | **CONFIRMED.** Both failure paths set operator-visible error text ("Failed to save workspace preferences" / "Failed to update workspace preferences" or the thrown message); no state mutation occurs before the server round-trip. | Tests `..._create_failure_surfaces_explicit_error` (list remains empty after rejection) and `..._update_failure_surfaces_explicit_error`. |
| **M3 — empty state verbatim** | **CONFIRMED.** The exact line-171 sentence renders; no spinner or blank panel. | Test `test_uiconv_p03_settings_empty_state_is_preserved_verbatim` + capture 01. |
| **M4 — no backend or schema change** | **CONFIRMED.** Zero backend application files, migrations, endpoints, or dependencies touched. The only backend change is the source-inspection test path re-point (§5). | Patch file list; Alembic head unchanged. |

---

## 4. Standing requirements R2–R8

| Requirement | Status |
|---|---|
| **R2** `/workspace` must not 404 | Registry entry keeps `route: "/workspace"`, `Component` is now `WorkspaceSettingsRedirect` → `<Navigate to="/?open=settings" replace />` (the established redirect pattern). Capture 03: navigation lands on `/?open=settings` with the overlay open. |
| **R3** No fabricated fallbacks | The editor's initial values are editor defaults; the saved list and detail render **server rows only**. Empty database → verbatim empty state (capture 01). Zero hardcoded statistical or preference literals presented as saved state. |
| **R4** `data-testid` on every major region | 12 hooks: surface, backdrop, overlay, close, editor, saved list, detail, empty, loading, error, refresh, **create btn**, **update btn**, plus per-field and per-card hooks. Baseline was 0. |
| **R6** RBAC | The overlay renders inside the protected shell (registry entry unchanged, `protectedWorkspace()` wrapper intact, no per-entry override); logged-out access blocked by `ProtectedRoute` as before. No widening. |
| **R7** Suite green, no test deleted to force green | **164 suites / 755 tests passing.** The page's test suite was **relocated** (not deleted) to `components/terminal/settings/WorkspaceCustomizationWorkspace.test.tsx`; 7 new overlay tests + 3 new deep-link tests added. |
| **R8** `npm ci` before `tsc -b` | Executed: `npm ci` → `npx tsc -b --pretty false` → **exit 0**. |

---

## 5. OBS-CONV3-3 fold-in — confirmed

The four Cycle-1 orphaned files were deleted (working tree) and the directive's item-3 discipline applied to this cycle:

| File | Disposition |
|---|---|
| `pages/ScenarioComparisonPage.tsx` (281 ln) | **deleted** — redirect registered; dock panel is the single implementation |
| `pages/ScenarioComparisonPage.test.tsx` | **deleted** — its suite lives at `docks/ScenarioComparisonPanel.test.tsx` |
| `pages/PortfolioResearchPage.tsx` (163 ln) | **deleted** — redirect registered |
| `pages/PortfolioResearchPage.test.tsx` | **deleted** — suite lives at `docks/PortfolioResearchPanel.test.tsx` |
| `pages/WorkspaceCustomizationPage.tsx` (271 ln) | **deleted this cycle** — superseded by the settings overlay |
| `pages/WorkspaceCustomizationPage.test.tsx` | **deleted from pages/** — suite **relocated** to `components/terminal/settings/WorkspaceCustomizationWorkspace.test.tsx` (R7: the tests' guarantees survive; the pages copy is gone) |

Post-apply verification in a pristine clone at `34f4c62`: **0 superseded pages; single export for each workspace component; 164 suites / 755 tests green.**

---

## 6. Executed transcripts (raw console output)

Saved to `docs/evidence/uiconv/` — raw logs, not summaries:

| Command | Log file | Result |
|---|---|---|
| `npx vitest run` (full) | `vitest_p03item3.log` *(regenerate name below)* | **164 files / 755 tests passed** — exit 0 |
| `npx tsc -b --pretty false` | `tsc_p03item3.log` | **exit 0**, zero diagnostics |
| `npm run build` | `vite_build_p03item3.log` | **exit 0** · `index-CNZSqWdC.js` 685.94 kB |
| backend `pytest -q` | `pytest_p03item3.log` | **415 passed** — exit 0 |

Bundle delta: cycle-1 close 683.93 kB → **685.94 kB (+2.01 kB)** for the settings overlay + header button. Disclosed under OBS-5 discipline.

*(Log filenames on disk: `vitest_p03c1.log` was cycle 1; this cycle's full-suite run is recorded in `docs/evidence/uiconv/vitest_p03item3.log`, `tsc_p03item3.log`, `vite_build_p03item3.log`, `pytest_p03item3.log`.)*

## 7. Level-I captures (3 · all exactly 1920×1080 · alt text on every image)

Gallery: `UI-CONV-P03-ITEM3_CAPTURES.html` (workspace root) · raw PNGs: `/home/user/uiconv_p03_item3_captures/` · DOM record: `UI-CONV-P03-ITEM3_CAPTURE_VERIFICATION.json`.

| # | File | SHA-256 | Subject |
|---|---|---|---|
| 1 | `UI-CONV-P03-ITEM3_01_SETTINGS_EMPTY_STATE.png` | `45f2ef6b5b3a8a568d8dd041112a304645930170eb41daa594f7c0588d7aa8e6` | **Empty state** — verbatim line-171 sentence, 0 saved cards (M3/R3) |
| 2 | `UI-CONV-P03-ITEM3_02_SETTINGS_POPULATED_SCROLLED.png` | `103ebbcf494df70897ca2d75a7627e78e039a91b291ea9d6e032487ff10ef591` | **Populated, scrolled to panel body** — saved card, editor, both mutation buttons, detail (OBS-CONV3-1 discipline: body scrollTop 439/1339 recorded) |
| 3 | `UI-CONV-P03-ITEM3_03_WORKSPACE_ROUTE_REDIRECT.png` | `48ef03d07b583566eb0c00b3c4663f3ddf07e7d1acfa074a2015b36620aa426b` | `/workspace` → `/?open=settings`, overlay open (R2) |

## 8. Transport package

| Item | Value |
|---|---|
| Patch | `/home/user/item3.patch` — **1,609 lines · 67,308 B · SHA-256 `b7b4c4f74f3016cb1d03d147413cd303c80c31ecb2e2132c86dec642269e27fd`** · LF endings · terminating newline verified |
| Scope | 15 files · **+588 / −718** (6 deletions incl. the four OBS-CONV3-3 files + the two item-3 superseded files; 3 new modules; 6 modifications) |
| `git apply --check` against a pristine clone at `34f4c62` | **exit 0** |
| Applied in pristine clone | **164 suites / 755 tests passed · tsc exit 0 · build `index-CNZSqWdC.js` 685.94 kB** (identical hash to the DA working tree) |

**Deviation disclosed:** the Operator instructed "no commits" for this repository, so the directive's `git format-patch 34f4c62..HEAD` form cannot be produced (there are no commits). The patch is instead `git diff`-based (with intent-to-add for new files) and was verified to apply cleanly and run green at the stated base — the same content a committed range would carry. On the first push credential/commit workflow, the format-patch form will be used.

## 9. Precise wording (OBS-CONV2-2 discipline)

- `WorkspaceCustomizationPage.tsx` + test: **deleted** from `pages/`; the presentational component was **relocated** (not copied) to `components/terminal/settings/`; its test suite was **relocated** alongside (single copy exists).
- The four OBS-CONV3-3 files: **deleted**.
- The settings module was **relocated** from `workstation/settings/` to `components/terminal/settings/` after the shell-purity gate rejected the first placement — no duplicate remained at either path.

## 10. Files changed (working tree vs `34f4c62`)

| Path | Disposition |
|---|---|
| `components/terminal/settings/WorkspaceSettingsOverlay.tsx` | **added** (re-homed surface + container) |
| `components/terminal/settings/WorkspaceSettingsOverlay.css` | **added** |
| `components/terminal/settings/WorkspaceSettingsOverlay.test.tsx` | **added** (7 tests) |
| `components/terminal/settings/WorkspaceCustomizationWorkspace.test.tsx` | **added** (relocated page suite) |
| `scripts/capture_uiconv_p03_item3.mjs` | **added** (capture harness) |
| `workstation/overlays/OverlayProvider.tsx` | modified (settingsOpen/openSettings/closeSettings) |
| `workstation/overlays/OverlayLayer.tsx` | modified (mounts the settings overlay) |
| `workstation/components/InstitutionalWorkspaceShell.tsx` | modified (Settings header button; `open=settings` deep link) |
| `workstation/registry/workspaceRegistry.tsx` | modified (redirect component; Settings entry) |
| `terminal/terminalDeepLinks.test.tsx` | modified (+3 tests: deep link, legacy route, header button) |
| `backend/tests/test_workspace_preferences.py` | modified (source-inspection path re-pointed to the new module) |
| `pages/ScenarioComparisonPage.tsx` + `.test.tsx` | **deleted** (OBS-CONV3-3) |
| `pages/PortfolioResearchPage.tsx` + `.test.tsx` | **deleted** (OBS-CONV3-3) |
| `pages/WorkspaceCustomizationPage.tsx` + `.test.tsx` | **deleted** (superseded this cycle; test relocated) |

**No backend application code, schema, migration, endpoint, or dependency changed (M4/BO §6).**

## 11. Standing findings

| ID | Status |
|---|---|
| `OBS-CONV3-3` | **Discharged in this cycle** (4 files deleted; suite green post-apply) |
| `OBS-CONV3-1` capture fold | Addressed this cycle (capture 02 scrolled to body, scroll metrics recorded) |
| `OBS-CONV3-4` | Advisory acknowledged — closes with item 4 (research stage must render before `/research-management` converts) |
| `CA-CONV2-3` transport | Open — no push credential; Operator republish workflow in effect |
| `OBS-CONV2-2` wording | Held — this report states dispositions exactly |
| `OBS-CONV2-5` / fixtures | Open — deviation register |
| `OBS-PROV-2` | Open |
| `OBS-5` | +2.01 kB disclosed here |
| `F-BRAND-1` | Open — GA-173 |

---

Gate **CLOSED** · Production **NOT CERTIFIED** · This delivery covers item 3 only (plus its mandated fold-in); items 4, 5, 6 remain under the parent Build Order and were not begun.

**We don't guess. We prove.**

*— AXIOM Development Authority (DA)*
*2026-08-15*

---

# ADDENDUM A — 2026-08-15: FINAL DETERMINATION — APPROVED WITH OBSERVATIONS

ITRGA issued `ITRGA_DETERMINATION_UI-CONV-P03_ITEM3_FINAL.md` (attached by the Operator; ingested into `docs/build-orders/`): **item 3 APPROVED WITH OBSERVATIONS.** `CA-CONV3-2` (transport), `OBS-CONV3-3` (orphans), `OBS-CONV3-6` (transcripts), `OBS-CONV2-6` (tsc) all **CLOSED**; all five §1 capabilities, M1–M4, and R2/R3/R4/R6 **PASS** in applied source; the inline-patch sha256 reconciled exactly (`b7b4c4f7…`).

**Carried-observation dispositions (this addendum):**

1. **`OBS-CONV3-5` (empty-state capture below fold) — DISCHARGED by the Rev-B re-capture already produced with the transmission.** Capture 01 Rev B: SHA-256 `e369b7096f07e889632096bc34cd7648db3f49bec97fdd46b75fc8c8fff12333`, DOM-verified `sentenceVisibleInViewport: true`, `bodyScroll {scrollTop: 249, scrollHeight: 1149, clientHeight: 900}`, verbatim sentence text extracted. Gallery Rev B: `UI-CONV-P03-ITEM3_CAPTURES.html` (SHA-256 `64e5654a…`); raw PNGs at `/home/user/uiconv_p03_item3_captures/`. Forward to ITRGA for closure.
2. **`OBS-CONV3-7` (CRLF) — acknowledged; root cause stated plainly.** The DA's on-disk artifact `/home/user/item3.patch` is byte-exact LF with a terminating newline (verified before transmission). The inline paste incurred newline conversion in the message channel. Protocol hardening going forward: after any inline transmission, the receiver normalizes and verifies sha256 — which ITRGA did — and the workspace file remains the authoritative byte channel (downloadable as a file, immune to message-layer conversion).
3. **`OBS-CONV3-8` (durability) — acknowledged with a factual correction.** The item-3 work is durable in the workspace filesystem (the working tree, `/home/user/item3.patch`, the capture gallery, and all evidence have persisted across every session boundary to date) — it is **git-undurable** by the Operator's standing no-commit instruction, and three verified items are indeed accumulating outside the repository. The DA restates the Operator-owned options: authorize commits (DA can then commit the verified tree), or continue the patch-artifact protocol. ITRGA's structural note is agreed: at origin only `34f4c62` exists.
4. **`OBS-CONV3-4`** — acknowledged as load-bearing for item 4: the `"research"` stage must render before `/research-management` converts. No item-4 work performed.
5. Standing: `CA-CONV2-3` (open, structural) · `OBS-PROV-2` · `OBS-5` · `F-BRAND-1` · `OBS-CONV2-5`.

**Remaining P03 items (not authorized by this determination):** item 5 (`GovernanceEvidencePage`, 1,072 ln, RBAC-sensitive), item 6 (`SignalInvestigationPage`, 425 ln), item 4 (`ResearchManagementPage`, 1,391 ln — disposition approved, B-4 extended by `OBS-CONV3-4`).

Gate **CLOSED** · Production **NOT CERTIFIED** · No commits or pushes made. Awaiting the next item's authorization.

*— AXIOM Development Authority (DA)*
*2026-08-15*
