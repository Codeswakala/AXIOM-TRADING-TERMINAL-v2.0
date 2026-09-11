# DELIVERY REPORT — UI-001-P04

## Workspace Persistence via `operator_workspace_preferences`

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | Institutional UI Transformation |
| Workstream | UI-001 — Institutional Workspace Shell |
| Phase | P04 |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-001-P04.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-001-P03.md` — APPROVED WITH OBSERVATIONS |
| Baseline platform | v0.62.0 |
| Alembic head | `20260717_0037` unchanged |
| DA status | Implemented and locally validated |
| Approval status | Not self-approved; pending operator evidence / browser evidence / ITRGA review |

---

## 1. Executive summary

UI-001-P04 has been implemented as durable shell layout persistence using the existing W7-U02 `operator_workspace_preferences` table and API path.

The institutional shell now has a persistence seam for:

```text
active workspace id
last route
navigation collapsed state
panel layout descriptor
```

Shell preferences are stored under:

```text
workspace_key = institutional-shell-v1
```

The implementation reuses the existing W7-U02 operator-scoped preference API and repository semantics. No new table, migration, schema column, or backend endpoint was added.

The shell restores the saved preference after login and falls back safely to default layout when no preference exists.

The Governance Gate remains **CLOSED**.

---

## 2. Scope delivered

### A. Shell preference persistence service

Created:

```text
frontend/src/workstation/persistence/shellPreferences.ts
frontend/src/workstation/persistence/shellPreferences.test.ts
```

Key implementation:

```text
SHELL_WORKSPACE_KEY = institutional-shell-v1
ShellLayoutPreference
findShellWorkspacePreference
toShellPreferenceWrite
shellPreferenceFromRecord
loadShellLayoutPreference
persistShellLayoutPreference
```

The service uses existing frontend API client functions:

```text
fetchWorkspacePreferences
createWorkspacePreference
updateWorkspacePreference
```

No new endpoint was added.

### B. Shell integration

Modified:

```text
frontend/src/workstation/components/InstitutionalWorkspaceShell.tsx
```

The shell now:

- loads shell preferences after authenticated shell mount;
- restores navigation collapsed state;
- restores compatible panel layout;
- restores last route from default `/` entry when a saved route exists;
- persists active workspace, last route, navigation collapsed state, and panel layout after shell changes;
- continues to use P03 session layout seam as local runtime store.

### C. Evidence seed script

Created:

```text
scripts/ui_001_p04_seed_shell_preference.py
```

The script commits a shell preference through the existing backend `WorkspacePreferenceRepository` and prints ids for raw PostgreSQL evidence.

### D. Operator isolation test

Created:

```text
backend/tests/test_ui_shell_preferences.py
```

This test proves, with valid tokens, that operator B cannot read/list/write operator A's shell preference row.

---

## 3. Persistence design

Shell preference payload shape:

```text
workspace_key: institutional-shell-v1
layout_config:
  active_workspace
  last_route
  navigation.collapsed
  panel_layout
  persistence_scope
visible_modules:
  operations
  research_journal
  institutional_intelligence
theme_config:
  mode
  density
metadata:
  ui_workstream
  version
```

The payload is constrained by the existing W7-U02 validation, including:

- forbidden field rejection;
- secret marker rejection;
- allowed visible module validation;
- current-operator scoping;
- create/update audit events.

No schema change is required.

---

## 4. Guardrail compliance

| Requirement | Result |
|---|---|
| R-4 no schema creep | Preserved. No table/migration/schema column added; Alembic remains `20260717_0037`. |
| Existing W7-U02 persistence reused | Implemented. Uses `operator_workspace_preferences` through existing API/repository. |
| Operator scoping | Implemented/tested. Valid-token B cannot read/list/write A's shell preference. |
| No actuation | Preserved/tested. Persistence payload contains no execution/order/broker/account/Gate control. |
| No secrets/PII | Preserved/tested. Payload and source marker tests are clean. |
| Restore after login | Implemented/tested at service level; browser evidence pack requires served-session sign-out/sign-in proof. |
| No dependency | Preserved. No package added. |
| No backend schema/API expansion | Preserved. No new endpoint/table/migration. |
| No regression | Preserved locally. Backend 414 passed; frontend 25 files / 89 tests passed. |

---

## 5. Files changed or added for UI-001-P04

### Frontend created

```text
frontend/src/workstation/persistence/shellPreferences.ts
frontend/src/workstation/persistence/shellPreferences.test.ts
```

### Frontend modified

```text
frontend/src/workstation/components/InstitutionalWorkspaceShell.tsx
```

### Backend tests / scripts created

```text
backend/tests/test_ui_shell_preferences.py
scripts/ui_001_p04_seed_shell_preference.py
```

### Docs created/updated

```text
docs/build-orders/ITRGA_REVIEW_UI-001-P03.md
docs/build-orders/BUILD_ORDER_UI-001-P04.md
docs/build-orders/BUILD_ORDER_INTAKE_UI-001-P04.md
docs/evidence/UI-001-P04_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_UI-001-P04.md
README.md
PROJECT_STATE.md
CHANGELOG.md
```

No backend application source, API route, Alembic/schema, ML, or governance behavior implementation files were changed for UI-001-P04.

---

## 6. Mandatory tests implemented

Frontend tests in:

```text
frontend/src/workstation/persistence/shellPreferences.test.ts
```

Implemented named tests:

```text
test_shell_layout_persists_via_operator_workspace_preferences_no_new_table
test_shell_layout_restores_previous_session_after_login
test_shell_persistence_no_execution_or_actuation_and_no_secret_fields
```

Backend tests in:

```text
backend/tests/test_ui_shell_preferences.py
```

Implemented named test:

```text
test_shell_preferences_operator_scoped_B_cannot_read_A
```

Existing P01/P02/P03 shell tests continue to pass.

---

## 7. Local validation performed by DA

### P04/P03/P02/P01 shell tests

```bash
cd /home/user/axiom/frontend
npm test -- shellPreferences.test.ts InstitutionalWorkspaceShell.test.tsx PanelInfrastructure.test.tsx NavigationDock.test.tsx
```

Result:

```text
4 files / 22 tests passed
```

### Frontend full suite

```bash
cd /home/user/axiom/frontend
npm audit --audit-level=high
npm test
npm run lint
npm run build
```

Results:

```text
npm audit: found 0 vulnerabilities
Vitest: 25 files / 89 tests passed
TypeScript: clean
Build: successful
```

Build output after P04:

```text
dist/assets/index-CBBuyKq-.css   29.93 kB │ gzip: 5.79 kB
dist/assets/index-Ck9IZiIc.js   452.19 kB │ gzip: 132.24 kB
```

P03 build reference:

```text
CSS 29.93 kB
JS  450.54 kB
```

Approximate raw delta:

```text
CSS +0.00 kB
JS  +1.65 kB
```

### Backend regression

```bash
cd /home/user/axiom/backend
ruff check .
pytest tests/test_ui_shell_preferences.py tests/test_broker_integration.py tests/test_wave7_closeout.py -q
pytest -q
```

Results:

```text
Ruff: All checks passed
Targeted: 13 passed, 1 warning
Backend full suite: 414 passed, 1 warning
```

### Seed smoke

```bash
python scripts/ui_001_p04_seed_shell_preference.py
```

Result:

```text
UI_001_P04_SHELL_PREFERENCE_SEED_COMPLETE
SHELL_PREFERENCE_ACTION=created
SHELL_WORKSPACE_KEY=institutional-shell-v1
SHELL_PREFERENCE_ID=<id>
SHELL_AUDIT_CORRELATION_ID=<id>
```

---

## 8. Operator evidence pack

Operator evidence command pack is ready at:

```text
docs/evidence/UI-001-P04_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell/PostgreSQL/browser commands for:

1. build identity;
2. source committing path proof;
3. shell preference seed through existing repository;
4. raw psql SELECT of shell row;
5. no-orphan audit join;
6. operator FK no-orphan join;
7. no schema creep / forbidden column proof;
8. named frontend/backend tests;
9. valid-token two-operator isolation proof;
10. no-actuation/no-secret source grep;
11. browser restore after sign-out/sign-in;
12. local CI.

---

## 9. Deferred / explicitly not implemented

Deferred to later UI-001 phases:

- P05 Region-F three-layer overlay family completion;
- P05 full command palette behavior;
- P06 legacy `TerminalLayout` cleanup;
- advanced layout persistence semantics beyond shell key;
- full token architecture completion.

Explicitly not implemented:

- new table or migration;
- new backend endpoint;
- backend business logic change;
- API/schema/governance/ML change;
- new dependency;
- new trading/research capability;
- execution/order/broker/account/Gate controls;
- external AI/LLM;
- production certification.

---

## 10. DA disposition

UI-001-P04 is implemented and locally validated by the Development Authority.

This is **not** an approval. DA does not self-approve UI-001-P04, does not self-authorize UI-001-P05, does not certify production readiness, does not expand platform capability, and does not modify the Governance Gate.

Next required step: operator runs `docs/evidence/UI-001-P04_OPERATOR_EVIDENCE_COMMANDS.md` on the target Windows/PostgreSQL/browser environment and submits transcript + screenshots to ITRGA for review.

---

**End of DELIVERY_REPORT_UI-001-P04.md**
