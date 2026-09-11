# DELIVERY REPORT — W7-U03 EVIDENCE FIX

## Research Management Collections & Tags

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Unit | W7-U03 — Research Management Collections & Tags |
| Trigger | Operator evidence transcript `operator results.md` |
| Platform candidate | v0.57.0 |
| Alembic head | `20260717_0037` |
| DA status | Evidence-command defects corrected |
| Approval status | Not self-approved; W7-U03 still pending valid operator evidence and ITRGA review |

---

## 1. Issues observed

### E-1 — Seed script import path failed from repository root

Operator evidence showed:

```text
python scripts\w7_u03_seed_research_management.py
ModuleNotFoundError: No module named 'app'
```

Root cause: the script was documented to run from repository root, but it imported backend package `app` without adding `backend/` to `sys.path`.

Impact: the seed step was a non-result; downstream raw SELECTs returned zero rows because no evidence rows had been created.

### E-2 — PowerShell login prompt blocked two-operator proof

Operator evidence stopped at:

```text
Security Warning: Script Execution Risk
Invoke-WebRequest parses the content of the web page...
```

Root cause: Windows PowerShell legacy `Invoke-WebRequest` parsing warning. The login commands lacked `-UseBasicParsing`.

Impact: the two-operator API proof was interrupted before token validation.

---

## 2. Corrections applied

### Script robustness

Updated:

```text
scripts/w7_u03_seed_research_management.py
```

The script now inserts the backend package root before importing `app`:

```text
BACKEND_ROOT = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))
```

### Evidence pack hardening

Updated:

```text
docs/evidence/W7-U03_OPERATOR_EVIDENCE_COMMANDS.md
```

Changes:

- seed command now captures stderr and throws on non-zero `$LASTEXITCODE`;
- two-operator seed command now captures stderr and throws on non-zero `$LASTEXITCODE`;
- seed output / JSON existence checks added;
- login commands now use `Invoke-WebRequest -UseBasicParsing` to avoid the interactive script-execution warning.

### Focused rerun pack

Created:

```text
docs/evidence/W7-U03_EVIDENCE_FIX_COMMANDS.md
```

This pack lets the operator rerun only the failed/non-result portions:

1. fixed seed script;
2. raw persistence capture;
3. non-interactive login/token validation;
4. continuation of the two-operator API isolation proof.

---

## 3. Local validation of fix

DA validated the fixed seed script from repository root against a migrated SQLite smoke database.

Result:

```text
W7_U03_RESEARCH_MANAGEMENT_SEED_COMPLETE
OPERATOR_ID=<id>
SCENARIO_REPORT_ID=<id>
COLLECTION_ID=<id>
MEMBER_ID=<id>
TAG_ID=<id>
SOURCE_IDENTITY_UNCHANGED=True
SOURCE_AUDIT_BEFORE=1
SOURCE_AUDIT_AFTER=1
SOURCE_AUDIT_UNCHANGED=True
```

The prior backend/frontend tests in the operator transcript already showed:

```text
W7-U03 named backend tests: 11 passed
W7-U03 + W7 security + broker targeted suite: 34 passed
Backend full suite: 377 passed
Ruff: All checks passed
Frontend: 20 files / 64 tests passed
Build: successful
```

---

## 4. Governance disposition

These were evidence-command defects, not approval, not a new capability, and not W7-U04 authorization.

W7-U03 remains pending valid operator evidence and ITRGA review. DA does not self-approve W7-U03 or authorize any next unit.

---

**End of DELIVERY_REPORT_W7-U03_EVIDENCE_FIX.md**
