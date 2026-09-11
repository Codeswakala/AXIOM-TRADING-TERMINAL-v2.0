# ITRGA DETERMINATION — UI-CONV-P03 · ITEM 3 (FINAL)

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** `WorkspaceCustomizationPage` → shell-owned settings overlay · `OBS-CONV3-3` fold-in
**Date:** 2026-08-15
**Base:** `34f4c62` · **Patch verified applied in pristine clone `/tmp/ap`**
**Supersedes:** the BLOCKED determination on item 3. **The blocker is resolved — the DA transmitted the patch inline.**

| Artifact | sha256 | Content |
|---|---|---|
| `OPERATOR RESULTS.md` (DA transmission) | `0e6c39ac8e89bbd4…` | 1,653 lines — **1,609-line patch + four raw transcripts** |

---

## 1. DETERMINATION

# APPROVED WITH OBSERVATIONS

**Item 3 is verified in applied source. `OBS-CONV3-3` is CLOSED. `CA-CONV3-2` is CLOSED.** Every mandatory requirement is met, including the two that were specific to this being the phase's only write-capable surface.

**My prior BLOCKED determination was correct on the evidence I had and is now discharged.** The patch was transmitted; I misattributed the submission to the Operator when it was the DA's. Correction noted.

---

## 2. TRANSPORT — SUCCEEDED, AND HASH-CONFIRMED

```
extracted diff ......... 1,609 lines · 15 diff --git headers
sha256 ................. b7b4c4f74f3016cb…   ← EXACT match to DA's declared hash
git apply --check ...... exit 0   (pristine 34f4c62 clone)
git apply .............. APPLIED OK
```

**The sha256 reconciles exactly** after LF normalisation and appending the terminating newline. That is the strongest transport evidence this programme has produced: the bytes I verified are provably the bytes the DA generated.

The transmission carried the known CRLF-without-terminating-newline condition. **This did not obstruct verification** — the repair is documented (`sed 's/\r$//'` + `printf '\n'`) and was applied mechanically. Recorded, not held against the delivery.

The `git diff` substitution for `git format-patch` is **accepted** — with no commits in the working tree there is no commit range, and the DA's reasoning was correct. The directive's omission of a fallback form was mine.

---

## 3. VERIFIED IN APPLIED SOURCE

### `OBS-CONV3-3` — **CLOSED**

All four Cycle-1 orphans deleted, plus item 3's own superseded pair:

```
pages/ScenarioComparisonPage.tsx ........... gone
pages/ScenarioComparisonPage.test.tsx ...... gone
pages/PortfolioResearchPage.tsx ............ gone
pages/PortfolioResearchPage.test.tsx ....... gone
pages/WorkspaceCustomizationPage.tsx ....... gone
pages/WorkspaceCustomizationPage.test.tsx .. gone
```

**Re-homing is now complete by the standard this authority set: exactly one implementation exists.** The third-occurrence pattern is broken.

### Item 3 requirements

| Req | Verification | Result |
|---|---|---|
| **§1 capabilities ×5** | `Workspace Customization` · `Preference Editor` · `Saved Preferences` · `Preference Detail` · `{selected.workspace_key}` all present in `WorkspaceSettingsOverlay.tsx` | **PASS** |
| **M1 — both mutations** | `createWorkspacePreference` :330 · `updateWorkspacePreference` :340 · `fetchWorkspacePreferences` :319 | **PASS** |
| **M2 — explicit errors** | `setError(err instanceof Error ? err.message : "Failed to save workspace preferences")` :333, load :321, update path likewise. No silent catch, no optimistic update on a persisted write. | **PASS** |
| **M3 — empty state verbatim** | `:253` — *"No workspace preferences have been saved for this operator."* Rule also stated in the module docblock at `:36`. | **PASS** |
| **M4 — no backend/schema change** | Only `backend/tests/test_workspace_preferences.py` touched — a source-inspection path re-point, `-1/+1`. No endpoint, model or migration. | **PASS** |
| **R2 — `/workspace` no 404** | `WorkspaceSettingsRedirect` :47-48 → `/?open=settings`; registry `Component:` :387. Shell consumes it: `InstitutionalWorkspaceShell.tsx:91`, `OverlayLayer.tsx:18`. | **PASS** |
| **R3 — no fabricated fallbacks** | 0 hardcoded percentage literals in the new module | **PASS** |
| **R4 — testids** | **20 hooks** (baseline 0; items 1–2 delivered 8 and 10) | **PASS** |
| **R6 — RBAC** | 16/16 `protectedWorkspace()` wrappers; `ALL_AUTHENTICATED_ROLES = ["admin","operator"]` unchanged; no `unprivileged` grant | **PASS** |

**The chosen home is sound.** A shell-owned overlay reached from top chrome and `/?open=settings` — not a bottom-dock tab beside research tabs, as the directive required. `WorkspaceSettingsOverlay` is mounted in `OverlayLayer`, correctly separating settings lifecycle from research surfaces.

---

## 4. EXECUTION EVIDENCE — `OBS-CONV3-6` CLOSED

Raw console output supplied for all four suites. This is what was required and it discharges the finding.

```
Test Files  164 passed (164)
     Tests  755 passed (755)
  Duration  150.01s

npx tsc -b --pretty false → (no diagnostics printed — exit code 0)

vite v8.1.4 · 150 modules transformed
dist/assets/index-CNZSqWdC.js   685.94 kB │ gzip: 184.46 kB
✓ built in 447ms

415 passed, 1 warning in 112.14s
```

**1,170 tests green** (755 frontend + 415 backend), up from the 34f4c62 baseline. `tsc -b` **exit 0** — this also discharges **`OBS-CONV2-6`**, the `@types/node` environment defect, in the DA's environment. The Operator's local environment may still need `npm ci`; that is separate and no longer blocks delivery evidence.

The `index-CNZSqWdC.js` hash matches the DA's §8 claim of an identical build from a pristine-clone application. Independent corroboration of reproducibility.

Bundle 685.94 kB — +3.83 kB vs the 682.11 kB of record. Consistent with a new overlay module and CSS. **POLISH-P01** owns code-splitting; not an item-3 defect.

---

## 5. OBSERVATIONS

### `OBS-CONV3-5` — capture 01 does not evidence M3 — **CARRIED, downgraded**

Capture 01 is declared *"Empty state — verbatim line-171 sentence, 0 saved cards."* The frame terminates at `Save preferences`; the SAVED PREFERENCES region and the sentence are **below the fold**.

**Downgraded, not withdrawn.** M3 is now proven in source at `:253`, so the *behaviour* is verified. What remains unevidenced is the *rendering* of the empty state. Capture 02 correctly discharged `OBS-CONV3-1` for the populated view — apply the same scroll discipline to the empty view next cycle.

**Pattern worth naming:** across two cycles, every capture offered as empty-state proof has been cut above the empty state, while populated captures render fully. Empty states sit at the bottom of these panels. **Scroll to the region the claim depends on.**

### `OBS-CONV3-7` — CRLF line endings — **NEW, minor**

The transmission was CRLF throughout with no terminating newline. `git apply` rejects this raw (`corrupt patch at line N+1`). Repaired mechanically; verification unaffected. Transmit LF with a terminating newline, as the directive specified.

### Carried forward

`OBS-CONV3-4` (`"research"` stage inert — **load-bearing for item 4**) · `OBS-PROV-2` (`docs/evidence/` absent) · `OBS-5` (bundle) · `F-BRAND-1` (GA-173) · `OBS-CONV2-5` (seeded fixtures).

---

## 6. CREDIT WHERE DUE

1. **Patch transmitted inline with a hash that reconciles exactly** — the transport standard this programme needed.
2. **Raw transcripts supplied** — `OBS-CONV3-6` closed in one cycle.
3. **`OBS-CONV3-3` fully discharged**, including item 3's own page without being asked twice.
4. **Self-disclosed internal correction:** the settings module was relocated from `workstation/settings/` to `components/terminal/settings/` "after the shell-purity gate rejected the first placement — no duplicate remained at either path." Volunteered, precisely worded.
5. **Wording discipline observed** — *deleted*, *relocated*, *copied* used exactly, per `OBS-CONV2-2`.
6. **Patch pre-verified against a pristine clone** before submission, with exit code reported.

---

## 7. STATUS

| Item | State |
|---|---|
| **UI-CONV-P03 item 3** | **APPROVED WITH OBSERVATIONS** |
| `CA-CONV3-2` transport | **CLOSED** — inline patch, hash reconciled |
| `OBS-CONV3-3` orphan pages | **CLOSED** — all six files deleted |
| `OBS-CONV3-6` transcripts | **CLOSED** — raw output supplied |
| `OBS-CONV2-6` `tsc -b` | **CLOSED** in DA environment (exit 0) |
| `OBS-CONV3-1` capture fold | **CLOSED** for populated captures |
| `OBS-CONV3-5` empty-state capture | Carried — downgraded |
| `OBS-CONV3-7` CRLF | **NEW** — minor |
| `OBS-CONV3-4` `"research"` stage inert | Open — **blocks item 4 route conversion** |
| `CA-CONV2-3` transport structural | **Open** — but the inline protocol now works |
| P02 closures ×4 | Verified intact |

**Remaining P03:** item 5 (`GovernanceEvidencePage`, 1,072 ln), item 6 (`SignalInvestigationPage`, 425 ln), item 4 (`ResearchManagementPage`, 1,391 ln — disposition approved, **B-4 extended by `OBS-CONV3-4`**).

**Note on origin:** this determination verifies the patch as applied in a scratch clone. Origin `main` remains `34f4c62`. Per Operator instruction, commits are deferred; the verified patch is the artifact of record. **`OBS-CONV3-8`:** the item-3 work now exists only in the DA sandbox and in `/tmp/ap`, neither durable. Three items of verified work are accumulating outside the repository.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination is **not authorization** for the next item.
**No implementation** beyond `BUILD_ORDER_UI-CONV-P03` scope.

**We don't guess. We prove.**
