# DELIVERY REPORT — UI-004-P05

## Research Artifacts, Collections & Saved-View Preferences

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Phase | **UI-004-P05** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-004-P05.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-004-P04.md` and `docs/build-orders/ITRGA_DETERMINATION_UI-004-P04_APPROVED_WITH_OBSERVATIONS.md` |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 41f/175t |
| DA status | Implemented; evidence package prepared; not self-approved |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Build identity

This delivery report is for:

```text
UI-004-P05 — Research Artifacts, Collections & Saved-View Preferences
```

It is governed by:

```text
docs/build-orders/BUILD_ORDER_UI-004-P05.md
docs/build-orders/ITRGA_REVIEW_UI-004-P04.md
docs/build-orders/ITRGA_DETERMINATION_UI-004-P04_APPROVED_WITH_OBSERVATIONS.md
docs/plans/UI-004_ENGINEERING_DESIGN_PLAN.md
```

DA does not self-approve UI-004-P05.

---

## 2. P04 observations carried into P05

| Observation | P05 handling |
|---|---|
| OBS-P04-1 timeout-fragile route-loop tests | Added explicit `30000` ms timeout to the two identified tests. |
| OBS-P04-2 served P04 panel screenshot owed | P05 operator evidence requires a served screenshot of the P04 Validation & Economic-Usefulness Integrity panel. |
| OBS-P04-3 local CI sentinel typo | P05 evidence command uses `$localCiExitCode = $LASTEXITCODE` and prints `LOCAL_CI_EXIT_CODE:` correctly. |

---

## 3. Implementation summary

UI-004-P05 adds a read-only research artifact context surface inside the existing `/intelligence` Research & Intelligence workspace.

Implemented:

1. `ResearchArtifactContextPanel` inside `InstitutionalIntelligencePage.tsx`;
2. existing `fetchResearchManagementBundle(50)` and `fetchJournalEntries(25)` read integrations;
3. read-only collections context;
4. read-only collection member references;
5. read-only research tags;
6. read-only journal references;
7. artifact id inventory across report/source ids, signal ids, and analytics source ids;
8. explicit saved-view absence card stating saved-view persistence is not implemented in UI-004-P05;
9. six UI-004-P05 named tests.

Saved-view persistence was **not implemented** in this phase. Therefore the R-2 raw psql persistence-capture control is not claimed and not required for this P05 submission.

---

## 4. Files added

```text
docs/build-orders/BUILD_ORDER_UI-004-P05.md
docs/build-orders/BUILD_ORDER_INTAKE_UI-004-P05.md
frontend/src/workstation/research/ResearchArtifactsContext.test.tsx
docs/evidence/UI-004-P05_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_UI-004-P05.md
```

---

## 5. Files modified

```text
frontend/src/pages/InstitutionalIntelligencePage.tsx
frontend/src/styles/global.css
frontend/src/workstation/components/InstitutionalWorkspaceShell.test.tsx
frontend/src/workstation/navigation/WorkflowNavigationCompletion.test.tsx
PROJECT_STATE.md
CHANGELOG.md
docs/governance/GOVERNANCE_AMENDMENTS.md
```

No backend source, API contract, schema, migration, package manifest, saved-view persistence, or workspace registry change was made.

---

## 6. Research artifact context posture

The P05 surface displays existing values only:

```text
research_collections.collection_id
research_collections.name
research_collections.description
research_collections.research_status
research_collection_members.collection_id
research_collection_members.artifact_type
research_collection_members.artifact_id
research_tags.tag
research_tags.artifact_type
research_tags.artifact_id
manual journal ids / linked_signal_ids / linked_report_ids
report ids / report hashes / source_artifact_ids
advisory signal ids
analytics source_artifact_ids when supplied
```

Collections and tags are read-only in UI-004-P05. No create/update/delete controls are rendered in the P05 panel.

---

## 7. Saved-view persistence decision

DA explicitly did **not** implement saved-view persistence in UI-004-P05.

Therefore:

```text
No operator_workspace_preferences write path was added.
No research-intelligence-workspace-v1 preference key was introduced.
No report body, analytics payload, artifact content, order/account/broker field, secret, or saved view payload is persisted.
No raw psql persistence-capture proof is claimed for P05.
```

Named test coverage uses the absence variant required by the Build Order:

```text
test_ui004_no_saved_view_persistence_is_implemented_this_phase
```

---

## 8. Explicit P05 boundaries

UI-004-P05 did not add:

- saved-view persistence;
- new table/migration/column/backend schema change;
- collection/tag mutation;
- source/report/artifact content copy into preferences;
- UI-004-P06 completion checkpoint;
- recompute/re-derivation/stronger relabeling;
- client-side analytics engine;
- external AI/LLM;
- live/real data;
- broker/account/order/execution/Gate path;
- new dependency;
- new endpoint;
- workspace registry or route change;
- production certification.

---

## 9. No-recompute / no-inference proof

Production source grep against `InstitutionalIntelligencePage.tsx` showed no matches for:

```text
inferSignal
runInference
authoritativeRecompute
emitSignal
generateSignal
recompute
recalculat
deriveConfidence
reclassif
summariz.*(ai|llm|gpt)
new .*Engine
/api/v1/orders
```

Result:

```text
NO_RECOMPUTE_GREP_CLEAN
```

---

## 10. No actuation proof

Production source grep against `InstitutionalIntelligencePage.tsx` showed no matches for:

```text
buy
sell
place_order
execute
go-live
connect-broker
account_id
order_ticket
open_gate
allow_execution
```

Result:

```text
NO_ACTUATION_GREP_CLEAN
```

---

## 11. No-drift substitute

DA local no-drift facts:

```text
No backend source change
No API/schema/migration change
No package manifest change
No workspace registry change
No saved-view persistence implemented
No new endpoint/provider/table markers
Alembic temp smoke: 20260717_0037 (head)
```

Registry remains:

```text
research.intelligence
/intelligence
```

No `/research-intelligence` route was added.

---

## 12. Named UI-004-P05 tests

Added:

```text
frontend/src/workstation/research/ResearchArtifactsContext.test.tsx
```

Required named tests:

```text
test_ui004_research_artifacts_render_existing_collections_tags_and_ids_read_only
test_ui004_collections_and_tags_expose_no_create_update_or_delete_mutation
test_ui004_no_saved_view_persistence_is_implemented_this_phase
test_ui004_research_artifact_surface_contains_no_recompute_inference_or_signal_generation
test_ui004_research_artifact_surface_contains_no_execution_order_broker_account_or_gate_path
test_ui004_research_artifacts_accessibility_and_brand_markers_hold
```

DA local result:

```text
1 file passed / 6 tests passed
```

---

## 13. Local DA validation

### 13.1 Frontend

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
npm audit --audit-level=high: exit 0
npm audit disclosed 2 moderate react-router/react-router-dom advisories; no high/critical audit failure and no dependency change authorized in P05
Frontend full suite: 42 files / 181 tests passed
TypeScript: clean
Production build: successful
```

Build output:

```text
CSS: 45.92 kB
JS: 529.02 kB
```

Baseline comparison from UI-004-P04:

```text
Frontend tests: 41 files / 175 tests → 42 files / 181 tests
Bundle: CSS 45.08 kB / JS 524.24 kB → CSS 45.92 kB / JS 529.02 kB
Delta: +1 test file / +6 tests; +0.84 kB CSS / +4.78 kB JS
```

### 13.2 Backend

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

### 13.3 Alembic

Temp SQLite Alembic smoke:

```text
alembic current: 20260717_0037 (head)
```

Operator target must still provide target `alembic current` evidence.

---

## 14. Doc 16 brand self-check

| Doc 16 check | DA self-check |
|---|---|
| B-1 Logo / monogram | Existing UI-001 shell AX monogram and AXIOM identity unchanged. |
| B-2 Constitutional palette | New styling uses existing CSS tokens only. No hardcoded colors in UI-004 production TSX. |
| B-3 Typography + monospace numerics | Collection ids, tag artifact ids, journal ids, report ids, signal ids, and source ids use textual/monospace presentation. |
| B-4 Unified iconography | No new icon set introduced. |
| B-5 Institutional-not-retail | Copy emphasizes existing governed artifacts, read-only collection/tag context, no mutation, and no saved-view persistence. |
| B-6 Accessibility | Semantic sections, ARIA labels, no mutation controls, readable cards, responsive layout. |
| B-7 Documentation branding | Delivery/evidence/build-order records use AXIOM governance format. |

Browser proof remains mandatory for operator evidence and ITRGA review.

---

## 15. Operator evidence package

Prepared:

```text
docs/evidence/UI-004-P05_OPERATOR_EVIDENCE_COMMANDS.md
```

The command pack covers:

- build identity;
- six named tests displayed passing;
- read-only artifact context proof;
- no mutation controls;
- saved-view absence proof;
- no-recompute/no-inference grep;
- no-actuation grep;
- no-drift substitute and no registry change;
- P04 observation closure evidence;
- Doc 16 brand/accessibility proof;
- frontend/backend regression;
- browser served-session evidence;
- fixed local CI sentinel.

---

## 16. DA disposition

DA submits UI-004-P05 for operator evidence collection and ITRGA review.

DA does not self-approve UI-004-P05.

UI-004-P06 is not authorized until ITRGA approves or approves-with-observations P05 and explicitly authorizes the next Build Order.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of DELIVERY_REPORT_UI-004-P05.md**
