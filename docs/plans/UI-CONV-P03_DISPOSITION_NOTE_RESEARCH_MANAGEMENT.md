# UI-CONV-P03 §4 — DISPOSITION NOTE: `ResearchManagementPage`

| Field | Value |
|---|---|
| Document type | DA disposition note (BUILD_ORDER_UI-CONV-P03 §4 — mandatory gate before item-4 implementation) |
| Issued by | AXIOM Development Authority (DA) |
| Issued to | AXIOM ITRGA |
| Date | 2026-08-15 |
| Surface | `frontend/src/pages/ResearchManagementPage.tsx` — 1,391 lines, 10 endpoint consumers, 0 `data-testid` |
| Base | `75c71c5` (verified) |

---

## 1. Chosen target home

**A dedicated full-height `RESEARCH` view of the unified terminal workstation**, swapped into the terminal's primary stage (the same mechanism the Chart Stage occupies), reached by:

- `/?view=research` — deep-link target (legacy `/research-management` redirects here via the P02 `<Navigate replace />` pattern);
- the **left module rail** (Research launcher) — one click from anywhere in the terminal;
- the **command palette** (`Open Research Management` → post-absorption destination `/?view=research`).

**Rejected homes, with reasons:**

| Candidate | Rejection reason |
|---|---|
| Right dock tab | 320 px wide. The hub renders a catalog grid, filter panel, mutation forms, and detail cards. Cramming it into the right dock would make every capability harder to reach — a direct violation of the turn-56 reframe. |
| Bottom dock tab | Height-limited drawer already hosting four research tabs. A 1,391-line cross-cutting hub consuming ten endpoints cannot be honestly presented in a drawer without severe compression. |
| Route left as a standalone page | Keeps a second full-page surface outside the terminal — fails the CONV objective of one shell. |

The primary stage already hosts exactly one such full-height capability view (the Chart Stage), so the architecture has a proven precedent for stage-level views. Implementing `view` consumption is a **small, bounded presentation change** (no backend, no schema, no endpoint change — BO §6 respected).

## 2. Capability preservation map (all eleven §3 groups → Research Hub view)

| §3 capability group | Component (relocates unchanged) | Reachable in Research Hub |
|---|---|---|
| Unified Research Artifact Explorer | `ArtifactExplorerFrame` | Yes — stage view |
| Governed Data-Source Inventory | `ArtifactSourceInventory` | Yes |
| Unified Artifact Catalog | `ArtifactCatalog` | Yes |
| Collection Organization Controls (create collection, add artifact reference, member references) | `CollectionMembershipOrganizationPanel` | Yes |
| Source ids · Stored lineage · Scope/samples/uncertainty/limitations · Stored relationships · Stored detail fields | catalog entry rendering (`buildCatalogEntries` / detail cards) | Yes — unchanged rendering |
| Tag Organization Controls (create tag) | `TagOrganizationPanel` | Yes |
| Existing Research Organization Records | organization record lists | Yes |
| Report Builder / Export Preview cross-references (via advanced report fetch) | retained fetch surface | Yes |

**No capability is proposed for removal, re-scoping, or demotion.** All ten endpoint consumers carry over; the fetch orchestration moves from the page wrapper into the view module.

## 3. Relocation proposal (not deletion, not absorption-into-dock)

Per the CONV-P02 lesson (relocate and re-home; do not delete):

1. The page module **relocates** to `frontend/src/components/terminal/research/ResearchHubView.tsx` (all exports keep their names and contracts, mirroring `ChartWorkspaceSurface`).
2. `frontend/src/pages/ResearchManagementPage.tsx` is deleted; the legacy route `/research-management` becomes `ResearchManagementRedirect` → `<Navigate to="/?view=research" replace />`.
3. The eight dependent test files (incl. `pages/ResearchManagementPage.test.tsx` and the seven `workstation/artifacts/*` suites) are re-pointed to the new module path; the page test file moves alongside its subject.
4. `data-testid` hooks are added to every major region of the view (R4): frame, source inventory, catalog, filters, collection controls, tag controls, records lists.
5. The `view` param consumption is implemented in the terminal workspace (currently unparsed — honest disclosure): `?view=research` swaps the primary stage to the Research Hub; `?view=chart` keeps the Chart Stage; absent view renders the default multi-pane terminal.

## 4. Proposed deviations

**None.** Every §3 capability group is re-homed. No endpoint, schema, dependency, or RBAC change is involved (the registry entry keeps its role requirements; the view renders only for authorized operators inside the shell).

## 5. Sequencing note

Implementation of item 4 begins only after ITRGA responds to this note. Items 1, 2, 3, 5, 6 proceed in parallel per the Build Order.

---

**Awaiting ITRGA response before item-4 code.**

*— AXIOM Development Authority (DA)*
*2026-08-15*
