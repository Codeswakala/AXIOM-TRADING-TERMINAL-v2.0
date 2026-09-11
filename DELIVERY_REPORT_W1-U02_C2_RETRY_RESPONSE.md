# Delivery Report — W1-U02 C-2 Retry Response

| Field | Value |
|-------|-------|
| Parent unit | **W1-U02** Observability Service & CI Gate Consolidation |
| Trigger | `docs/build-orders/ITRGA_REVIEW_W1-U02_C2_RETRY.md` |
| Date | 2026-07-13 |
| Author | Development Authority |
| Status | **Evidence-capture correction supplied; operator final log capture pending** |
| Approval | **Not self-approved** |

---

## 1. Verdict acknowledgement

The Development Authority accepts ITRGA's C-2 retry verdict.

The authenticated request was real, but the evidence failed because the script grepped a server-log path that did not exist. ITRGA correctly ruled that blank `Select-String` results caused by `path does not exist` are not proof of redaction.

This is an evidence-capture failure, not a demonstrated code defect.

---

## 2. Correction supplied

Created a simpler final command pack:

`docs/evidence/W1-U02_C2_FINAL_LOG_CAPTURE_COMMANDS.md`

The new command pack eliminates the path ambiguity by writing server logs to a known file inside the backend directory:

```text
backend\server_redaction.log
```

It requires `Test-Path` before and after the request:

```powershell
SERVER_LOG_EXISTS_BEFORE_REQUEST: True
SERVER_LOG_EXISTS_AFTER_STOP: True
```

It then checks the confirmed log file for:

```text
RAW_TOKEN_IN_SERVER_LOG: False
DB_PASSWORD_IN_SERVER_LOG: False
REDACTION_CID_IN_SERVER_LOG: True
```

---

## 3. Why this satisfies ITRGA's requested proof

The final command pack produces all three ITRGA-required facts:

1. **Correlation ID present** — proves the authenticated request was actually logged.
2. **Raw access token absent** — proves the Bearer token did not leak into emitted logs.
3. **DB password absent** — proves the configured PostgreSQL credential did not leak into emitted logs.

AXIOM intentionally does not log request headers, so a masked Authorization field may not appear. This is safer than logging headers and masking them. The security claim is therefore demonstrated by correlation-present plus raw-token-absent against a confirmed log file.

---

## 4. Operator action required

The Operator should run:

`docs/evidence/W1-U02_C2_FINAL_LOG_CAPTURE_COMMANDS.md`

and submit:

1. the terminal transcript/output;
2. the confirmed server log file:

```text
backend\server_redaction.log
```

---

## 5. Current disposition

> W1-U02 remains conditional on final C-2 log evidence.  
> C-1/C-3/C-4/C-6 remain satisfied from prior operator evidence.  
> C-5 remains a tracked non-blocking observation.  
> DA does **not** self-approve.

---

**End of W1-U02 C-2 Retry Response**
