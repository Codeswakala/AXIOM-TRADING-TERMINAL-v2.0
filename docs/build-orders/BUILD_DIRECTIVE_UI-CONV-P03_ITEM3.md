# BUILD DIRECTIVE — UI-CONV-P03 · ITEM 3

**Issuing authority:** Independent Technical Review & Governance Authority
**Date:** 2026-08-15
**Scope:** Item 3 only — `WorkspaceCustomizationPage` → Settings surface
**Base:** `34f4c62` (`AXIOM-TRADING-TERMINAL-v1.0`)
**Parent Build Order:** `BUILD_ORDER_UI-CONV-P03` — this directive scopes one item; it does not amend the Build Order.

---

## 1. THE SURFACE — verified inventory

`frontend/src/pages/WorkspaceCustomizationPage.tsx` · **271 lines** · **0 `data-testid`**

| Capability group | Must survive |
|---|---|
| Workspace Customization (frame) | Yes |
| Preference Editor | Yes |
| Saved Preferences | Yes |
| Preference Detail (`{selected.workspace_key}`) | Yes |
| Empty state — *"No workspace preferences have been saved for this operator."* (line 171) | Yes |

**Exports:** `WorkspaceCustomizationWorkspace` (line 60, presentational) · `WorkspaceCustomizationPage` (line 216, container). The same two-export split as items 1–2 — re-home the presentational component and let the container become a redirect.

---

## 2. ⚠ ITEM 3 IS NOT LIKE ITEMS 1–2 — IT WRITES

Items 1 and 2 were **read-only** surfaces. This one performs **persisted mutations**:

```
api/client:  createWorkspacePreference(payload)
             updateWorkspacePreference(preferenceId, payload)
             fetchWorkspacePreferences()

page:214-253  async createPreference()  → setPreferences([created, ...current])
              async updatePreference()  → replaces by preference_id
              error paths set explicit messages, never silent failure
```

**Mandatory requirements specific to this:**

**M1 — Both mutations must survive re-homing.** `createWorkspacePreference` and `updateWorkspacePreference` must remain reachable from the new surface. A settings surface that can display preferences but not save them is a capability regression, not a re-homing.

**M2 — Preserve explicit error surfacing.** Lines 239 and 253 set operator-visible error text on failure. **Never fail silently, never optimistically update.** Optimistic update on a persisted write is a data-honesty defect in the same family as `OBS-CONV2-1`.

**M3 — Preserve the empty state verbatim.** Line 171 is a genuine, honest empty state. Do not replace it with a spinner or a blank panel.

**M4 — No backend or schema change.** `OperatorWorkspacePreferenceWrite` and `OperatorWorkspacePreference` contracts are unchanged. If re-homing appears to need an endpoint change, **stop and report**.

---

## 3. TARGET HOME — DA proposes, ITRGA does not dictate

Blueprint §4 says: *"Settings surface, reachable from the shell, not a dock tab."*

Verified constraints:

- The bottom dock has five tabs (`TRADE_PLANS | JOURNAL | RISK | SCENARIOS | PORTFOLIO`). **A settings panel does not belong beside research tabs** — different intent, different lifecycle.
- The right dock is 320 px and holds `SIGNALS | TELEMETRY | INTELLIGENCE`.
- `StageViewName = "chart" | "research"` — the stage is reserved for research-scale surfaces.
- The registry already has `navigationCategory: "Settings"` (line 374) with `route: "/workspace"`.

**The DA selects the home and states its reasoning**, as it did for item 4. A modal/overlay reached from shell chrome, a dedicated stage view, or a left-rail settings launcher are all defensible. **A bottom-dock tab is not** — state a reason if you disagree rather than silently doing it.

**No disposition note is required for item 3** — at 271 lines with one endpoint family it does not carry item 4's risk. State the choice and the reasoning in the delivery report.

---

## 4. STANDING REQUIREMENTS

**R2 — `/workspace` must not 404.** Extend the established pattern: registry entry keeps `route: "/workspace"`, `Component` becomes a redirect to the new home. Follow `ScenarioComparisonRedirect` / `PortfolioResearchRedirect` (`workspaceRegistry.tsx:39,43`).

**R3 — No fabricated fallbacks.** No invented defaults presented as saved operator state. If no preference exists, say so (M3).

**R4 — `data-testid` on every major region:** frame, editor form, saved-preferences list, detail panel, empty state, and **both mutation controls**. Baseline is 0; items 1–2 delivered 8 and 10.

**R6 — RBAC.** All 16 registry entries inherit `ALL_AUTHENTICATED_ROLES = ["admin","operator"]` via `protectedWorkspace()`; **no entry carries a per-entry override.** Do not widen. There is no elevated gate here to preserve — this corrects an implication in the parent Build Order's R6.

**R7 — Suite green.** Baseline `34f4c62`: 165 frontend test files, 65 backend. New surface requires new tests. **Never delete a failing test to reach green.**

**R8 — `npm ci` before `tsc -b`** (`OBS-CONV2-6`).

---

## 5. FOLD IN: `OBS-CONV3-3` — FOUR FILES TO DELETE

Cycle 1 left superseded pages behind. Remove them in this cycle:

```
frontend/src/pages/ScenarioComparisonPage.tsx        (281 ln, unrouted)
frontend/src/pages/ScenarioComparisonPage.test.tsx   (5,626 B)
frontend/src/pages/PortfolioResearchPage.tsx         (163 ln, unrouted)
frontend/src/pages/PortfolioResearchPage.test.tsx    (4,540 B)
```

Nothing imports them outside their own tests; their registry entries already point at redirects. The dock replacements and their tests exist. **Verify the suite stays green after deletion** — that is the whole check.

Apply the same discipline to item 3: when `WorkspaceCustomizationPage.tsx` is superseded, delete it and its test in the same cycle. **Re-homing is complete when exactly one implementation exists.**

---

## 6. ⚠ ADVISORY FOR ITEM 4 — a live trap

Not item-3 work. Recording it now so it is not discovered late:

```
TradingTerminalWorkspace.tsx:54   type StageViewName = "chart" | "research"
                            :62-63  ?view=research  →  returns "research"
                            :95   const [stageView] = useState(...)
                            :155  data-stage-view={stageView ?? "default"}
```

`stageView` appears at **only two sites** — the state hook and the DOM attribute. **Nothing renders a research stage.** So `?view=research` currently parses successfully, sets the attribute, and displays the default multi-pane.

This is the `OBS-CONV2-7` failure mode reappearing one layer up: the *parser* is no longer inert, but the **`"research"` branch is**. It is harmless today because `/research-management` still routes to its page. **It becomes destructive the moment item 4 converts that route to a redirect** — eleven capability groups would silently vanish behind a URL that looks like it works.

**The B-4 condition therefore extends:** render the research stage and prove it before converting `/research-management`. Parsing alone does not satisfy B-4.

Recorded as **`OBS-CONV3-4`** — advisory, closes with item 4.

---

## 7. DELIVERY REQUIREMENTS

**Transport.** `CA-CONV2-3` remains open; the DA has no push credential. Until a PAT exists:

```bash
git format-patch 34f4c62..HEAD --stdout > item3.patch
git apply --check item3.patch ; echo "exit=$?"
```

Paste the **entire patch inline in the message body**. LF endings, terminating newline, report the exit code. A path plus a hash is not transmission.

**Report must contain:**

1. Chosen home + reasoning (§3).
2. Capability disposition table — each §1 group mapped to its new location.
3. **Explicit confirmation that create and update both work** in the re-homed surface (M1).
4. **Raw console transcripts** — `npm test`, `npx tsc -b` after `npm ci`, `npx vite build`. **A summary line is not execution evidence**; Cycle 1 supplied only a summary and that is not repeatable.
5. Level-I captures, single self-contained HTML with base64-embedded PNGs — the method that has now worked twice. Include:
   - **an empty-state capture** (no saved preferences),
   - a populated capture **scrolled to the panel body** (`OBS-CONV3-1` — Cycle 1's captures cut off above the content),
   - the `/workspace` redirect landing correctly.
6. Confirmation the four `OBS-CONV3-3` files are deleted and the suite is green.
7. Exact wording: **deleted**, **relocated**, **copied** — never *moved* when the original remains (`OBS-CONV2-2`).

---

## 8. ACCEPTANCE

1. All five §1 capabilities present in the re-homed surface.
2. **Create and update both functional** (M1); errors surfaced explicitly (M2); empty state preserved (M3).
3. `/workspace` resolves, does not 404.
4. `data-testid` on every major region including both mutation controls.
5. Suite green — no test deleted to force green.
6. `tsc -b` clean after `npm ci`; `vite build` succeeds.
7. Four `OBS-CONV3-3` files deleted; `WorkspaceCustomizationPage.tsx` + test deleted once superseded.
8. RBAC not widened.
9. Captures incl. empty state and scrolled body.
10. Report wording precise.

Verification: fresh clone + `verify_conv_p03.sh` + manual review of the non-machine-checkable items.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This directive authorizes **item 3 only**, within `BUILD_ORDER_UI-CONV-P03`. It is not authorization for items 4, 5, 6 or any later programme.

**We don't guess. We prove.**
