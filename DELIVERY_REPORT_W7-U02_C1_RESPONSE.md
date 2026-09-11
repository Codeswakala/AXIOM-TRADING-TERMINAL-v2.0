# DELIVERY REPORT — W7-U02 C-1 RESPONSE

## Operator Workspace Customization — Two-Operator Isolation Evidence Correction

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Unit | W7-U02 — Operator Workspace Customization |
| Trigger | `docs/build-orders/ITRGA_REVIEW_W7-U02.md` |
| ITRGA verdict | CONDITIONAL APPROVAL; C-1 open; version bump held |
| Platform of record | v0.55.0 until ITRGA final approval |
| Candidate implementation version | v0.56.0 |
| Alembic head under review | `20260717_0034` |
| DA status | C-1 correction prepared and locally validated |
| Approval status | Not self-approved; awaiting operator rerun and ITRGA final verdict |

---

## 1. ITRGA finding

ITRGA found that the W7-U02 two-operator isolation API proof was a non-result. The operator evidence attempted to authenticate two seeded operators, but the PowerShell variables used for `/auth/login` were not populated. Both logins therefore failed with 422, leaving blank/invalid tokens and invalidating the API-level proof required by R7-3.

ITRGA did **not** classify this as a proven cross-operator leak. The issue is an invalid evidence probe that must be rerun with two valid, distinct operator tokens.

---

## 2. DA corrective action

DA recorded the review and prepared a C-1 correction pack.

### Files added

```text
docs/build-orders/ITRGA_REVIEW_W7-U02.md
docs/evidence/W7-U02_C1_CORRECTION_COMMANDS.md
DELIVERY_REPORT_W7-U02_C1_RESPONSE.md
```

### Files modified

```text
backend/app/api/routes/institutional_platform.py
backend/app/institutional_platform/preferences.py
backend/tests/test_workspace_preferences.py
```

### Implementation adjustment

The workspace preference read/update API now distinguishes:

- missing preference ID → `404 Workspace preference not found`;
- existing preference owned by another operator → `403 Cross-operator workspace preference access denied`.

This aligns the operator-run C-1 proof with ITRGA's required closure signal:

```text
B_READ_A_PREF_STATUS:403
B_WRITE_A_PREF_STATUS:403
```

No schema change, migration change, dependency change, execution/order/broker/account route, Gate-opening path, plugin execution, external API/LLM, or W7-U03 functionality was added.

---

## 3. Corrected operator evidence command pack

The C-1 rerun command pack is:

```text
docs/evidence/W7-U02_C1_CORRECTION_COMMANDS.md
```

It avoids the prior unset-variable failure mode by:

1. seeding two real operators and one workspace preference for each operator;
2. writing seed values to JSON;
3. parsing PowerShell variables directly from that JSON;
4. validating both login HTTP statuses;
5. validating both access tokens are present;
6. proving A can read A's preference;
7. proving B can read B's own preference;
8. proving B receives `403` when reading A's preference;
9. proving B's list has `B_VISIBLE_A_PREF_COUNT: 0` and `B_VISIBLE_B_PREF_COUNT >= 1`;
10. proving B receives `403` when attempting to update A's preference;
11. proving unauthenticated API access receives `401`;
12. providing a raw PostgreSQL 0-leakage check.

---

## 4. Local DA validation

DA reran backend validation after the C-1 adjustment.

```bash
cd /home/user/axiom/backend
python3 -m venv /tmp/axiom-venv
. /tmp/axiom-venv/bin/activate
pip install -q -e '.[dev]'
ruff check .
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_DATABASE_URL='sqlite+aiosqlite:///:memory:' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
pytest tests/test_workspace_preferences.py tests/test_institutional_platform_security.py tests/test_broker_integration.py -q
```

Result:

```text
All checks passed!
23 passed, 1 warning
```

Full backend regression:

```bash
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_DATABASE_URL='sqlite+aiosqlite:///:memory:' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
pytest -q
```

Result:

```text
366 passed, 1 warning
```

Frontend was not changed by this correction.

---

## 5. Governance disposition

W7-U02 remains **not finally approved**. DA does not self-approve the conditional item, does not declare v0.56.0 as the platform of record, does not authorize W7-U03, and does not open the Governance Gate.

Next required step: operator runs `docs/evidence/W7-U02_C1_CORRECTION_COMMANDS.md` on the Windows/PostgreSQL/browser evidence environment and returns the transcript to ITRGA for `ITRGA_VERDICT_W7-U02_FINAL.md`.

---

**End of DELIVERY_REPORT_W7-U02_C1_RESPONSE.md**
