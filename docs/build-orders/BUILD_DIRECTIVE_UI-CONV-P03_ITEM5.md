# BUILD DIRECTIVE — UI-CONV-P03 · ITEM 5

**Issuing authority:** Independent Technical Review & Governance Authority
**Date:** 2026-08-15
**Scope:** Item 5 only — `GovernanceEvidencePage` → governance view
**Base:** `34f4c62` **+ the verified item-3 patch** (`b7b4c4f74f3016cb…`, workspace copy `item3_verified.patch`)
**Parent Build Order:** `BUILD_ORDER_UI-CONV-P03` — this directive scopes one item; it does not amend the Build Order.

---

## 1. THE SURFACE — verified inventory

`frontend/src/pages/GovernanceEvidencePage.tsx` · **1,072 lines** · **0 `data-testid`** · **3 endpoints**

`fetchAuditEvents` · `fetchInstitutionalIntelligenceBundle` · `fetchPlatformOperationsEvidence`

### Capability groups — every one must survive

| Group | Sub-surfaces |
|---|---|
| **Audit Explorer** | event list · `{selectedEvent.action}` · Details payload · **Refusal reason-code viewer** |
| **Evidence Viewer** | `{record.id}` · **Validation Summary Panels** · `{storedText(record.id)}` |
| **Platform Health, Readiness & API Posture** | Runtime liveness · Runtime readiness · Checks as returned · **Production certification boundary** · Observability metrics · Persistence statistics · Version & system identity · Route, RBAC, API & plugin posture · Readiness posture records & residual honesty |
| **Governance & Evidence frame** | Governance Workspace Frame · Governance Status · **Certification Status** · **Standing Residuals** · **Read-Only Governance Boundary** · Governance Data-Source Inventory · **Inert Display Rules** · Gate state · Production state · Audit state |

**This is the constitutional conscience of the platform.** It renders the gate state, the certification boundary, standing residuals, refusal reason codes, and the read-only boundary declaration. A capability lost here is not a UI regression — it is the platform losing the ability to state its own limits.

---

## 2. ⚠ ITEM 5 IS A COUPLING PROBLEM, NOT A LAYOUT PROBLEM

Items 1–3 were self-contained. This one is not.

### 2.1 Seven modules import from this page

```
workstation/governance/AuditExplorer.test.tsx              → GovernanceEvidenceWorkspace, reasonCodeFor
workstation/governance/EvidenceValidationPanels.test.tsx   → UI007_EVIDENCE_MANIFEST
workstation/governance/GovernanceEvidenceCompletion.test.tsx
workstation/governance/GovernanceStatusDisplay.test.tsx
workstation/governance/GovernanceWorkspaceFrame.test.tsx   → UI007_GOVERNANCE_SOURCES
workstation/governance/PlatformOperationsPosture.test.tsx  → UI007_READINESS_POSTURE_RECORDS
workstation/registry/workspaceRegistry.tsx                 → GovernanceEvidencePage
```

**Six test suites and the registry.** Every one breaks on a naive move. All six must be re-pointed in the same patch.

### 2.2 The page exports seven governance constant tables

```
UI007_GOVERNANCE_SOURCES        :26
UI007_GUARDRAILS               :101
UI007_GOVERNANCE_STATUS        :124
UI007_CERTIFICATION_STATUS     :142
UI007_STANDING_RESIDUALS       :165
UI007_EVIDENCE_MANIFEST        :407
UI007_READINESS_POSTURE_RECORDS:601
```

Roughly **lines 26–839 are hardcoded governance data**, not presentation. Four of these tables are imported by external test suites as the source of truth.

**These constants are declared governance state, not fabricated statistics.** They are the correct kind of hardcoding — a static record of gate posture, evidence manifest and standing residuals. `R3` is **not** an instruction to make them dynamic. Do not "fix" them into API calls; that would be scope expansion and would invent a requirement.

**But their location matters.** Governance constants living inside a page component is why six external suites import from `pages/`. Relocating them to a dedicated module — e.g. `components/terminal/governance/governanceRecords.ts` — is the natural disposition. **The DA decides**; state the choice and reasoning.

### 2.3 `reasonCodeFor` is constitutional logic

```ts
export function reasonCodeFor(event: AuditEvent): string {
  const direct = details.reason_code;
  if (typeof direct === "string" && direct.trim()) return direct;
  const refusal = Object.values(details).find(v => /^[A-Z0-9_]+_REFUSED$/.test(v));
  return typeof refusal === "string" ? refusal : "—";
}
```

Returns `"—"` when no reason code exists — **an honest absence marker, not a fabricated code.** Preserve this exactly. It must keep its named export; `AuditExplorer.test.tsx` imports it directly.

---

## 3. MANDATORY REQUIREMENTS

**M1 — All six governance test suites re-pointed, none deleted.** They are the regression guard for the constitutional surface. Re-point imports; do not rewrite assertions to accommodate a new shape. If an assertion genuinely cannot hold, **stop and report** — do not weaken it.

**M2 — `reasonCodeFor` preserved verbatim**, named export retained, `"—"` fallback intact.

**M3 — The four constitutional declarations must remain visible**, not collapsed behind interaction: **Production certification boundary** · **Read-Only Governance Boundary** · **Inert Display Rules** · **Standing Residuals**. These may not be relegated to a tooltip, an accordion default-closed, or a secondary tab. The platform must state its limits without the operator hunting for them.

**M4 — No backend or schema change.** Three read endpoints, unchanged. No backend source-inspection test references this page — verified — so no backend re-point is expected. If one appears necessary, **stop and report**.

**M5 — Preserve per-section error and loading states.** The container holds nine state variables across three independent fetches (`auditLoading/auditError`, `validationLoading/validationError`, `platformOperationsLoading/platformOperationsError`). **Each section degrades independently.** Do not collapse them into one global spinner — a failed audit fetch must not blank the certification boundary.

---

## 4. TARGET HOME — DA proposes

Blueprint §4: governance view / left-rail launcher. Verified constraints:

- **1,072 lines with four major capability groups.** The right dock is 320 px — too narrow, on the same reasoning that rejected it for item 4.
- The bottom dock holds five research tabs; governance is not a research artifact.
- `StageViewName = "chart" | "research"` — a third stage value is available if the DA wants stage treatment.
- The registry has `navigationCategory: "Govern"` with `route: "/governance"`.

A dedicated stage view (`?view=governance`), a full-height overlay like item 3's settings surface, or a left-rail launcher are all defensible. **A bottom-dock tab is not.** State the choice and reasoning in the report; no separate disposition note required.

**If a stage view is chosen, `OBS-CONV3-4` applies** — see §6.

---

## 5. STANDING REQUIREMENTS

**R2 — `/governance` must not 404.** Extend the established pattern (`WorkspaceSettingsRedirect` at `workspaceRegistry.tsx:47-48` is the current model).

**R3 — No fabricated fallbacks.** Per §2.2: the `UI007_*` tables are declared governance state and stay. What is prohibited is inventing *runtime* values — a health metric, a readiness check, or an audit count must never render a plausible-looking number when the API returns nothing. Absence renders as absence.

**R4 — `data-testid` on every major region.** Baseline 0. Items 1–3 delivered 8, 10, 20. Cover: frame, audit explorer, event detail, details payload, refusal viewer, evidence viewer, validation panels, each platform-posture subsection, and every constitutional declaration in M3.

**R6 — RBAC.** 16/16 entries inherit `ALL_AUTHENTICATED_ROLES = ["admin","operator"]`; **no per-entry override exists** — governance is not specially gated today. Do not widen. Do not invent a gate.

**R7 — Suite green.** Current verified state: **755 frontend / 415 backend = 1,170**. New surface requires new tests. **Never delete a failing test to reach green.**

**R8 — `npm ci` before `tsc -b`.**

**Deletion discipline.** When `GovernanceEvidencePage.tsx` is superseded, delete it in the same cycle. `OBS-CONV3-3` is closed; do not reopen the pattern. Re-homing is complete when exactly one implementation exists.

---

## 6. ⚠ `OBS-CONV3-4` — READ BEFORE CHOOSING A STAGE VIEW

```
TradingTerminalWorkspace.tsx:54  type StageViewName = "chart" | "research"
                           :95   const [stageView] = useState(...)
                           :155  data-stage-view={stageView ?? "default"}
```

`stageView` appears at **only two sites** — the state hook and the DOM attribute. **No stage view is actually rendered.** `?view=research` parses, sets the attribute, and displays the default multi-pane.

If item 5 adopts `?view=governance`, the rendering branch must be **built and proven**, not merely parsed. Parsing without rendering is the `OBS-CONV2-7` failure one layer up — a URL that looks like it works while the capability is unreachable.

**Verification standard:** a named test asserting the governance stage **renders its content**, not merely that the attribute is set.

---

## 7. DELIVERY REQUIREMENTS

**Transport — the item-3 method worked; repeat it exactly.**

```bash
git diff 34f4c62 --stat        # confirm scope
git diff 34f4c62 > item5.patch  # include intent-to-add for new files
git apply --check item5.patch ; echo "exit=$?"
sha256sum item5.patch
```

Paste the **entire patch inline in the message body**, then the transcripts below it. Item 3's transmission reconciled to `b7b4c4f74f3016cb…` — that is the standard.

**LF endings, terminating newline** (`OBS-CONV3-7` — item 3 arrived CRLF; repairable but avoidable).

**Note on base:** item 3 is verified but **not committed** — origin is still `34f4c62`. State plainly whether item5.patch is cut against `34f4c62` **alone** or against `34f4c62 + item3`. I hold the item-3 patch and can reconstruct either; ambiguity is what caused the `5ef6c4e` stale-baseline regression.

**Report must contain:**

1. Chosen home + reasoning.
2. Capability disposition table — every §1 group mapped to its new location.
3. Confirmation all six governance suites re-pointed and green (M1).
4. **Raw console transcripts** — `vitest`, `tsc -b` after `npm ci`, `vite build`, `pytest`. Item 3 supplied these correctly; maintain it.
5. Level-I captures, single self-contained HTML, base64-embedded:
   - Audit Explorer with an event selected, **refusal reason-code visible**
   - The four M3 constitutional declarations, **in frame**
   - Platform posture section
   - **An empty/error-state capture scrolled to the affected region** — `OBS-CONV3-5`: across two cycles every empty-state capture has been cut above the empty state. **Scroll to the region the claim depends on.**
   - `/governance` redirect landing
6. Exact wording: *deleted* / *relocated* / *copied*.

---

## 8. ACCEPTANCE

1. Every §1 capability present and reachable.
2. M1 six suites re-pointed, green, assertions intact.
3. M2 `reasonCodeFor` verbatim with `"—"` fallback.
4. M3 four constitutional declarations visible without interaction.
5. M5 per-section independent error/loading states.
6. `/governance` resolves.
7. `data-testid` on every major region.
8. Suite green ≥ 1,170; nothing deleted to force green.
9. `tsc -b` clean; `vite build` succeeds.
10. RBAC not widened.
11. `GovernanceEvidencePage.tsx` deleted once superseded.
12. If a stage view is used: rendering branch proven by named test (`OBS-CONV3-4`).
13. Captures incl. a correctly scrolled empty/error state.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This directive authorizes **item 5 only**. It is not authorization for items 4 or 6, or any later programme.

**We don't guess. We prove.**
