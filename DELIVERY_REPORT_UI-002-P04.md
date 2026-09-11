# DELIVERY REPORT — UI-002-P04

## Global Search Framework · Read-Only Source Adapters · Search Overlay

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-002 — Workflow Navigation Framework |
| Phase | **UI-002-P04** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-002-P04.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-002-P03.md` — APPROVED WITH OBSERVATIONS |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 29f/115t |
| DA status | Implemented; evidence package prepared; not self-approved |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Build identity

This delivery report is for:

```text
UI-002-P04 — Global Search Framework · Read-Only Source Adapters · Search Overlay
```

It is not a UI-002-P03 report.

This implementation is governed by:

```text
docs/build-orders/BUILD_ORDER_UI-002-P04.md
docs/build-orders/ITRGA_REVIEW_UI-002-P03.md
```

Binding controls applied:

- **OBS-P03(UI002)-1 hard intake gate:** operator evidence commands begin with scoped-diff sentinel + `alembic current` proof.
- **R-2:** search first slice limited to workspace + signals + journal + research-collections.
- **R-5:** search results are read-only navigation targets only.
- **R-6:** Level-I evidence pack prepared for operator target run.

---

## 2. Implementation summary

UI-002-P04 adds global search as a Region-F overlay using the existing UI-001 overlay family.

Implemented:

1. `GlobalSearchResult` model with:

   ```ts
   resultAction: "navigate"
   readonly: true
   ```

2. first-party deterministic matching/ranking utility with client-side cache TTL and AbortController cancellation;
3. read-only search source adapters for exactly the R-2 first-slice sources:

   ```text
   workspace
   signals
   journal
   research-collections
   ```

4. existing-read-API adapters using:

   ```text
   fetchAdvisorySignals
   fetchJournalEntries
   fetchResearchManagementBundle
   ```

5. `GlobalSearchOverlay` rendered inside the existing Region-F `OverlayLayer`;
6. keyboard and accessibility behavior: focus on open, `aria-live` result count, listbox/option results, ArrowUp/ArrowDown, Enter selection, Escape close;
7. no query text or artifact payload persistence.

No backend search index, endpoint, table, migration, dependency, or actuation path was introduced.

---

## 3. Files added

```text
frontend/src/workstation/search/globalSearchTypes.ts
frontend/src/workstation/search/globalSearchIndex.ts
frontend/src/workstation/search/globalSearchSources.ts
frontend/src/workstation/search/GlobalSearchOverlay.tsx
frontend/src/workstation/search/GlobalSearch.test.tsx
docs/build-orders/ITRGA_REVIEW_UI-002-P03.md
docs/build-orders/BUILD_ORDER_UI-002-P04.md
docs/build-orders/BUILD_ORDER_INTAKE_UI-002-P04.md
docs/evidence/UI-002-P04_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_UI-002-P04.md
```

---

## 4. Files modified

```text
frontend/src/workstation/components/InstitutionalWorkspaceShell.tsx
frontend/src/workstation/components/InstitutionalWorkspaceShell.css
frontend/src/workstation/commands/commandTypes.ts
frontend/src/workstation/commands/commandRegistry.ts
frontend/src/workstation/commands/quickActionCatalogue.ts
frontend/src/workstation/overlays/OverlayProvider.tsx
frontend/src/workstation/overlays/OverlayLayer.tsx
PROJECT_STATE.md
CHANGELOG.md
docs/governance/GOVERNANCE_AMENDMENTS.md
```

Command-catalogue modification enables the previously vetted `qa.open.global-search` UI-toggle quick action. The `qa.clear.search-query` item remains disabled/deferred because P04 does not add a global persistent search-query state.

---

## 5. R-2 first-slice scope

P04 implements only:

| Source id | Origin | Route target |
|---|---|---|
| `workspace` | UI-001 `WORKSPACE_REGISTRY` | registered workspace routes |
| `signals` | existing `fetchAdvisorySignals` read API | `/signals` |
| `journal` | existing `fetchJournalEntries` read API | `/journal` |
| `research-collections` | existing `fetchResearchManagementBundle` read API, collections only | `/research-management` |

Explicitly not implemented in P04:

```text
intelligence
scenario
portfolio
chart-annotations
trade-plans
execution-research
```

Those remain P04b or later scope if ITRGA authorizes them.

---

## 6. R-5 read-only result model

Search results are data records, not executable commands.

They contain:

```text
route
resultAction: "navigate"
readonly: true
```

They do not contain an `onSelect` callback or mutation action.

The overlay selection logic performs only:

```text
onNavigate(result.route)
```

The result guard is implemented as:

```text
assertReadOnlyNavigationResult(...)
```

Unsafe result models are rejected by the named test:

```text
test_ui002_global_search_never_registers_mutation_or_actuation_results
```

---

## 7. No persistence / no backend expansion

P04 does not persist:

- query text;
- artifact payloads;
- business payloads;
- search results;
- source caches outside memory.

The search cache is an in-memory `Map` with TTL inside the browser runtime.

P04 does not add:

- backend search endpoint;
- search index table;
- Alembic migration;
- dependency or fuzzy-search library;
- package manifest change.

---

## 8. Explicitly not added

UI-002-P04 did not add:

- backend search index;
- new API endpoint;
- table, migration, column, or Alembic head change;
- fuzzy-search package or any dependency;
- search adapters beyond R-2 first slice;
- mutation/action search results;
- second overlay/search shell;
- external AI/LLM;
- dynamic plugin path;
- execution/order/broker/account/Gate path;
- production certification.

---

## 9. Local DA validation

### 9.1 Named UI-002-P04 tests

Command:

```bash
cd frontend
npm test -- --reporter=verbose GlobalSearch.test.tsx
```

Result:

```text
1 file passed / 6 tests passed
```

Named tests displayed passing:

```text
test_ui002_global_search_returns_read_only_navigation_results
test_ui002_global_search_uses_workspace_registry_and_existing_read_sources
test_ui002_global_search_never_registers_mutation_or_actuation_results
test_ui002_global_search_does_not_persist_query_text_or_artifact_payloads
test_ui002_global_search_accessibility_keyboard_and_result_announcement
test_ui002_global_search_adds_no_backend_schema_or_dependency_change
```

### 9.2 Frontend regression

Commands:

```bash
cd frontend
npm audit --audit-level=high
npm test -- --reporter=verbose
npx tsc -b --pretty false
npm run build
```

Results:

```text
npm audit: 0 vulnerabilities
Frontend full suite: 30 files / 121 tests passed
TypeScript: clean
Production build: successful
```

Build output:

```text
CSS: 37.19 kB
JS: 483.89 kB
```

Baseline comparison from UI-002-P03:

```text
Frontend tests: 29 files / 115 tests → 30 files / 121 tests
Bundle: CSS 35.93 kB / JS 477.30 kB → CSS 37.19 kB / JS 483.89 kB
Delta: +1 test file / +6 tests; +1.26 kB CSS / +6.59 kB JS
```

### 9.3 Backend regression

Commands:

```bash
cd backend
ruff check .
pytest -q
```

Results:

```text
Ruff: All checks passed!
Backend full suite: 414 passed, 1 warning
```

### 9.4 Alembic head

Temp SQLite Alembic smoke:

```text
alembic current: 20260717_0037 (head)
```

Operator target must still provide the PostgreSQL-target `alembic current` evidence as the first evidence lines under the hard P04 intake gate.

### 9.5 No-actuation / no-persistence grep

DA local grep over search source, tests excluded, for:

```text
buy|sell|place_order|execute|go-live|connect-broker|account_id|order_ticket|open_gate|allow_execution
localStorage|sessionStorage|search_query|artifact_payload|business_payload
```

Result:

```text
clean — no matches
```

---

## 10. OBS-P03(UI002)-1 hard intake gate

Prepared operator command pack begins with the hard intake gate:

```text
SCOPED_DIFF_NO_MATCHING_FILENAMES
20260717_0037 (head)
```

File:

```text
docs/evidence/UI-002-P04_OPERATOR_EVIDENCE_COMMANDS.md §0
```

The hard gate is intentionally first and uses simple commands to avoid the prior PowerShell `NativeCommandError` / interleaving issue.

---

## 11. Operator evidence package

Prepared:

```text
docs/evidence/UI-002-P04_OPERATOR_EVIDENCE_COMMANDS.md
```

The command pack covers:

- hard intake gate first;
- build identity;
- read-only result model proof;
- R-2 first-slice source proof;
- no backend expansion / no dependency proof;
- no-actuation and no-persistence grep;
- six named tests displayed passing;
- frontend regression, TypeScript, audit, build;
- backend regression and Ruff;
- served browser screenshots for first-slice global search, read-only jump-to result selection, keyboard operation, Gate CLOSED/research framing, and logged-out block;
- networked Git-Bash CI with exit-code sentinel.

---

## 12. Constitutional attestation

UI-002-P04 is presentation/navigation integration only.

The implementation:

- extends UI-001 rather than modifying its architectural responsibilities;
- reuses the existing Region-F overlay family;
- introduces global search as read-only jump-to navigation only;
- limits source adapters to the R-2 first slice;
- uses existing read APIs only;
- persists no search queries or artifact payloads;
- introduces no backend/API/schema/dependency change;
- introduces no external AI/LLM or dynamic plugin execution;
- introduces no business/trading/action search result type;
- introduces no execution/order/broker/account/Gate path;
- keeps the Governance Gate CLOSED;
- does not certify production deployment.

---

## 13. DA disposition

DA submits UI-002-P04 for operator evidence collection and ITRGA review.

DA does not self-approve UI-002-P04.

UI-002-P05 and P04b are not authorized until ITRGA approves UI-002-P04 and explicitly authorizes the next Build Order.

---

**End of DELIVERY_REPORT_UI-002-P04.md**
