# ITRGA Request — V2 BE-1 Correction Source Delta and Evidence

| Field | Value |
|---|---|
| Request ID | ITRGA-REQ-V2-BE-1-DELTA-001 |
| Date | 2026-08-24 |
| Purpose | Direct verification of corrections claimed by BE-1 Delivery Report DR-002 |
| Status | Active request — no new implementation scope |

---

## 1. Reason

DR-002 claims corrections for critical operator isolation, V2 exception-handler registration, response-envelope consistency, and 30 new integration tests. The current delivery submission contains the Delivery Report only; it does not contain current source or test evidence for those corrections.

The earlier source transcript predates these claimed fixes. A Delivery Report statement is not direct source evidence.

## 2. Required plain-text delta transcript

Submit one Markdown file named:

```text
V2_BE-1_SOURCE_REVIEW_DELTA.md
```

For each file use:

````markdown
## File: `relative/path`
**SHA-256:** `...`
```python
<literal current content>
```
````

Include literal current contents for:

```text
backend/app/v2/lineage/repository.py
backend/app/v2/api/lineage.py
backend/app/v2/api/audit.py
backend/app/v2/api/capability.py
backend/app/v2/errors/handlers.py
backend/app/main.py
backend/app/v2/models/capability.py
backend/tests/test_v2_integration.py
backend/tests/test_v2_audit.py
backend/tests/test_v2_rbac.py
backend/tests/test_v2_errors.py
```

Include any other changed BE-1 file required to make those corrections function, plus a short old-hash → new-hash manifest.

## 3. Required non-Git command evidence

Include literal output and exit statuses for:

```text
pytest tests/ --tb=short -q
pytest tests/test_v2_* tests/test_v2_integration.py --tb=short -q
```

The evidence must identify the 30 integration tests and show their actual execution.

## 4. Final review focus

ITRGA will verify:

- artifact-specific lineage lookup is operator-scoped;
- admin all-record exceptions are correctly permission-protected and audited;
- V2 exception handlers are registered and preserve safe error behavior;
- every V2 endpoint meets its response-envelope contract;
- cross-operator, trigger, sensitive-read, error-handler, and PostgreSQL-related tests exercise real code paths;
- no scope expands beyond BE-1.

No Git operation, new feature, provider/broker/account/execution/AI work, frontend work, or migration expansion is requested.
