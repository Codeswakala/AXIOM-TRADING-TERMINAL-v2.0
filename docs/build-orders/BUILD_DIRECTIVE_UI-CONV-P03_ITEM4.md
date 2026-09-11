# BUILD DIRECTIVE — UI-CONV-P03 · ITEM 4

**Issuing authority:** Independent Technical Review & Governance Authority
**Date:** 2026-08-15
**Scope:** Item 4 only — `ResearchManagementPage` → `?view=research` full-height stage
**Base:** `34f4c62` + item-3 (`b7b4c4f7…`) + item-5 (`4c03910c…`) + item-6 (`f65da5c3…`)
**Authorized by:** Operator, 2026-08-15
**Prior artifact:** `item4.patch.txt` (`f50fd70eb345ec56`, 1,138 lines, 19 files) — submitted ahead of authorization; **remains the candidate**, to be reviewed against this directive. No re-work is implied by its issuance.
**Disposition note:** `UI-CONV-P03_DISPOSITION_NOTE_RESEARCH_MANAGEMENT.md` — **APPROVED with the B-4 sequencing condition**, which this directive extends per `OBS-CONV3-4`.

---

## 1. THE SURFACE

`frontend/src/pages/ResearchManagementPage.tsx` · **1,391 lines** · **0 `data-testid`** · **10 endpoints**

The largest and most coupled surface in the phase, and the last item of the CONV programme.

```
fetchAdvancedResearchReport        fetchAdvisorySignals
fetchChartResearchAnnotations      fetchExecutionResearchBundle
fetchInstitutionalIntelligenceBundle   fetchJournalEntries
fetchPortfolioResearchDashboard    fetchResearchManagementBundle
fetchScenarioReports               fetchTradePlans
```

### Eleven capability groups — all must survive

Unified Research Artifact Explorer · Governed Data-Source Inventory · Unified Artifact Catalog · Collection Organization Controls (create collection · add artifact reference · existing member references) · Source ids · Stored lineage · Scope, samples, uncertainty, limitations · Stored relationships · Stored detail fields · Tag Organization Controls (create tag) · Existing Research Organization Records

### Exports

```
UI006_ARTIFACT_EXPLORER_SOURCES        :42    declared source inventory
assertCollectionOrganizationPayload   :185    ← write guard
assertMemberReferencePayload          :195    ← write guard
assertTagOrganizationPayload          :206    ← write guard
ArtifactExplorerFrame                 :581
ResearchManagementWorkspace          :1144
ResearchManagementPage               :1262
```

---

## 2. 🔴 M1 — THE THREE FIELD-ALLOWLIST WRITE GUARDS

**This is the highest-risk element of item 4 and the reason it warranted a directive.**

Item 4 performs persisted writes — `createResearchCollection` (:1327), `createResearchTag` (:1357) — and every write payload passes a field allowlist first:

```ts
export function assertCollectionOrganizationPayload(payload) {
  const unknown = Object.keys(payload).filter(k => !COLLECTION_WRITE_FIELDS.has(k));
  if (unknown.length > 0) throw new Error(`COLLECTION_ORGANIZATION_FIELD_NOT_ALLOWED:${unknown.join(",")}`);
  return payload as ResearchCollectionWrite;
}
```

Call sites: `:818`, `:825`, `:1029`. Two suites assert the throw behaviour — `CollectionMembershipMutation.test.tsx`, `TagOrganizationMutation.test.tsx`.

**Requirements — all mandatory:**

- **M1a** — All three functions preserved **verbatim**, named exports retained. `throw`-on-unknown-field semantics unchanged. Never soften to a filter, a warning, or a silent drop.
- **M1b** — All three must remain **wired into the write paths** at the equivalent of `:818`, `:825`, `:1029`. A preserved-but-unreferenced guard is a removed guard.
- **M1c** — The `*_FIELD_NOT_ALLOWED:` error strings are preserved. The two mutation suites assert them.

These guards are the client-side enforcement that a research-organization write cannot smuggle an out-of-contract field. Losing them during a re-home would be silent and severe.

---

## 3. 🔴 M2 — THE BACKEND CONSTITUTIONAL GUARD (vacuous-pass hazard)

```python
# backend/tests/test_research_management.py:482
def test_research_management_page_has_no_forbidden_controls() -> None:
    page = root / "frontend" / "src" / "pages" / "ResearchManagementPage.tsx"
    text = page.read_text(encoding="utf-8").lower()
    forbidden = ("place_order", "submit order", "go live", "connect broker",
                 "account_id", "order_ticket", "broker_account")
    assert all(item not in text for item in forbidden)
```

**Identical hazard to item 6's guard.** Re-point it to the module that **actually renders the research hub**. If it is aimed at a thin wrapper, a barrel file, or an index that does not contain the UI, the T-1 assertion passes vacuously and the platform silently loses a constitutional check.

Item 6 handled this correctly, including restating the hazard in a code comment. Apply the same standard.

---

## 4. M3 — SIX ARTIFACT SUITES + REGISTRY, RE-POINTED NOT DELETED

```
workstation/artifacts/ArtifactCatalogMetadata.test.tsx
workstation/artifacts/ArtifactExplorerCompletion.test.tsx
workstation/artifacts/ArtifactExplorerFrame.test.tsx
workstation/artifacts/ArtifactLineageRelationshipsFiltering.test.tsx
workstation/artifacts/CollectionMembershipMutation.test.tsx      ← asserts M1 guards
workstation/artifacts/TagOrganizationMutation.test.tsx           ← asserts M1 guards
workstation/registry/workspaceRegistry.tsx
pages/ResearchManagementPage.test.tsx                            ← relocate with subject
```

Re-point imports. **Do not rewrite assertions to accommodate a new shape.** If an assertion genuinely cannot hold, stop and report — do not weaken it.

---

## 5. 🔴 M4 — B-4 EXTENDED: RENDER BEFORE CONVERT

The approved disposition note chose `?view=research` as a full-height stage. The original B-4 condition required the parser to land before route conversion. **`OBS-CONV3-4` extends it:**

```
TradingTerminalWorkspace.tsx:54  type StageViewName = "chart" | "research"   ← parses
                           :95   const [stageView] = useState(...)
                           :155  data-stage-view={stageView ?? "default"}
```

Before item 4, `stageView` appeared at **two sites only** — state and attribute. **Nothing rendered a research stage.** `?view=research` parsed successfully and displayed the default multi-pane.

`?view=chart` survives that inertness because the chart is in the default layout. **`?view=research` has no such safety net.** If `/research-management` converts to a redirect while the stage does not render, **eleven capability groups vanish behind a URL that looks like it works.**

**Required:**

- **M4a** — The `"research"` branch must **render** `ResearchHubView`, not merely set an attribute.
- **M4b** — Proven by a **named test asserting rendered content**, not merely that `data-stage-view="research"` is present. A DOM attribute is not a rendered capability.
- **M4c** — Ordering: stage rendering lands **before or in the same patch as** the route conversion. Never after.
- **M4d** — `?view=chart` must continue to work; `?view=` absent must still render the default multi-pane. Both are regression surfaces.

---

## 6. M5 — TEN-ENDPOINT DEGRADATION

Ten independent fetches. **No single failure may blank the hub.** Each region degrades independently with its own loading and error state, following the M5 pattern established in item 5 (nine state variables, three fetches, verified).

**Fabricated fallbacks are prohibited** (R3). With ten endpoints the temptation to substitute a plausible-looking count or summary is highest here. Absence renders as absence — the `"—"` and *"No reports returned."* discipline from items 5 and 6.

---

## 7. STANDING REQUIREMENTS

**R2 — `/research-management` must not 404.** Convert to a redirect per the established pattern (`SignalInvestigationRedirect` :58 is the current model), **subject to M4c**.

**R4 — `data-testid` on every major region.** Baseline 0. Deliveries so far: 8, 10, 20, 17, 23. Cover all eleven capability groups and both mutation controls.

**R6 — RBAC.** 16/16 `protectedWorkspace()` wrappers, `ALL_AUTHENTICATED_ROLES = ["admin","operator"]`, no per-entry override. Do not widen.

**R7 — Suite green.** Current verified: **770 frontend / 415 backend = 1,185**. New surface requires new tests. **Never delete a failing test to reach green.**

**R8 — `npm ci` before `tsc -b`.**

**Deletion discipline.** Delete `ResearchManagementPage.tsx` and its test in the same cycle once superseded, after M2/M3 re-pointing. Items 3, 5 and 6 all held this standard.

**`UI006_ARTIFACT_EXPLORER_SOURCES`** is declared source inventory — the same class as item 5's `UI007_*` tables. **Relocate; do not convert to API calls.** That would be scope expansion.

---

## 8. DELIVERY REQUIREMENTS

**Transport — three consecutive hash-reconciled successes; repeat exactly.**

```bash
git diff <base> > item4.patch
git apply --check item4.patch ; echo "exit=$?"
sha256sum item4.patch
```

Inline in the message body. **LF endings, terminating newline.** **State the base explicitly:** `34f4c62 + item3 + item5 + item6`.

**Report must contain:**

1. Capability disposition table — all **eleven** groups mapped.
2. **M1 confirmation** — three guards preserved verbatim, still wired at their call sites, error strings intact, both mutation suites green.
3. **M2 confirmation** — backend guard re-pointed at the module that renders the hub, passing **non-vacuously**.
4. **M3 confirmation** — six artifact suites + registry re-pointed, assertions unweakened.
5. **M4 confirmation** — named test asserting the research stage **renders content**; `?view=chart` and default-layout regressions green.
6. Raw console transcripts — vitest, tsc -b, vite build, pytest.
7. **Level-I captures — ATTACHED.** `OBS-CONV3-9` is open two cycles; items 5 and 6 shipped none. Required:
   - the research stage rendered at `/?view=research`,
   - **an empty-state capture scrolled to the empty region** — `OBS-CONV3-5`, **open four cycles**; every empty-state capture so far has been cropped above the empty state,
   - a collection or tag mutation control,
   - `/research-management` redirect landing,
   - an interaction trace or explicit statement that **hit-testing was verified in a real browser** — jsdom cannot hit-test; that is how the item-3 `pointer-events` defect passed acceptance.
8. A delivery report. Item 6 shipped patches and transcripts with no report; disposition reasoning had to be reconstructed from source.
9. Exact wording: *deleted* / *relocated* / *copied* / *extended*.

---

## 9. ACCEPTANCE

1. All eleven capability groups present and reachable.
2. All ten endpoint consumers carried over.
3. **M1** three write guards verbatim, wired, error strings intact.
4. **M2** backend guard re-pointed non-vacuously.
5. **M3** six suites + registry re-pointed and green.
6. **M4** research stage renders, proven by named test; `?view=chart` and default layout unregressed.
7. **M5** independent degradation across ten fetches; no fabricated fallbacks.
8. `/research-management` resolves.
9. `data-testid` across all regions.
10. Suite green ≥ 1,185; nothing deleted to force green.
11. `tsc -b` clean; `vite build` succeeds.
12. RBAC not widened.
13. `ResearchManagementPage.tsx` + test deleted once superseded.
14. Captures **attached**, incl. correctly scrolled empty state and interactivity evidence.

---

## 10. ON PHASE CLOSURE

Item 4 is the **final item of UI-CONV-P03** and the last phase of the **CONV programme**. On approval I will issue the phase determination for UI-CONV-P03 and assess whether CONV as a whole can close.

**That determination will not be automatic.** `OBS-CONV3-8` stands: origin remains `34f4c62` and six items of verified work exist only as patches. A phase cannot be certified complete on artifacts that are not in the repository. I will state plainly what is approved-in-substance versus what is landed-at-origin.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This directive authorizes **item 4 only**. It is not authorization for SURF, DATA, CHART or POLISH.

**We don't guess. We prove.**
