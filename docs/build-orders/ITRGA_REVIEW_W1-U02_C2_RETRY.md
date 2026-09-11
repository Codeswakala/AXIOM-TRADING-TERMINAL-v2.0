# AXIOM ITRGA — C-2 RE-VERIFICATION (W1-U02 redaction log sample)

**Authority:** ITRGA · **Item under review:** C-2 (the single blocking item — redaction LOG SAMPLE)
**Input:** operator results console (redaction-evidence attempt). **Date:** 2026-07-13 · **Std:** R1/R7.

---

## VERDICT: **C-2 STILL NOT SATISFIED. Approval remains WITHHELD (one item).**

The attempt was made, but **it did not produce the evidence** — the verification could not read any server
log, so there is **zero proof** that the token was redacted (or leaked). Under R1/R7, a blank result from a
grep that errored is **not evidence**. This is an *evidence-collection* failure, not a code defect, and it
is close — but I will not approve a logging unit's defining security control on a check that never ran.

---

## 1. WHAT THE ATTEMPT SHOWS

**Partial (good):** an authenticated request was genuinely made — 255-char Bearer token, correlation ID
`redaction-log-proof-001`, `AUTHENTICATED_REQUEST_STATUS: 200`. The request half is real.

**The verification FAILED:** the script pointed at a server-log file that does not exist:
```
$ServerLog = "..\docs\evidence\W1-U02_FINAL_REDACTION_SERVER_LOG_20260713_154327.jsonl"
Select-String -Path $ServerLog ...
→ "Cannot find path '...W1-U02_FINAL_REDACTION_SERVER_LOG_...jsonl' because it does not exist"  (×5)

RAW_TOKEN_IN_SERVER_LOG:      (blank)
DB_PASSWORD_IN_SERVER_LOG:    (blank)
REDACTION_CID_IN_SERVER_LOG:  (blank)
STRUCTURED LOG LINES FOR REDACTION CID:   (none — path not found)
```

## 2. WHY THIS IS NOT CLOSURE (critical)

The three blank results are **NOT** "token absent from logs." They are **"the grep errored because the log
file wasn't there."** A failed `Select-String` returns nothing — that is the *absence of a test*, not a
*passing test*. In fact, `REDACTION_CID_IN_SERVER_LOG:` is also blank, which means the script couldn't
even confirm the request was logged **at all** — so we have neither a positive (cid present) nor the
security negative (token absent). This proves the operator **could not locate/read the structured logs**,
which is the opposite of what C-2 requires.

## 3. ROOT CAUSE (evidence-collection, not code)

Most likely one or more of:
- **Wrong path / cwd mismatch:** the transcript starts in `...\AXIOM\axiom`, but `$ServerLog` uses
  `..\docs\evidence\...` which resolves to `...\AXIOM\docs\evidence` (one level **above** the project),
  while the server (if it wrote a file at all) would be under `...\AXIOM\axiom\...`.
- **Server not writing logs to a file:** if uvicorn was started normally, structured logs go to **stdout/
  console**, not to that `.jsonl` — so no file exists to grep. The evidence run assumed a file that was
  never created.
- The `$ServerLog` timestamp (`154327`) predates the transcript (`154435`), suggesting the file was
  expected from an earlier step that didn't produce it.

## 4. REQUIRED CORRECTION (single, to close C-2 → APPROVED)

Capture the server's **actual** log output for one authenticated request and inspect it. Two clean ways:

**Option A — capture console logs to a file, then grep that exact file:**
```powershell
# From the backend dir, start uvicorn writing logs to a known file:
cd C:\Users\Swakala\.vscode\AXIOM\axiom\backend
python -m uvicorn app.main:app --port 8000 *>&1 | Tee-Object -FilePath .\server_redaction.log
# (in a second shell) make ONE authenticated request carrying a Bearer token + a unique correlation id:
$login = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v1/auth/login -ContentType application/json -Body '{"username":"admin","password":"admin123"}'
$token = $login.tokens.access_token
Invoke-WebRequest -Uri http://localhost:8000/api/v1/metrics -Headers @{ Authorization = "Bearer $token"; "X-Correlation-ID"="redaction-proof-002" } -UseBasicParsing | Out-Null
# then, against the REAL file that now exists:
Select-String -Path .\server_redaction.log -Pattern "redaction-proof-002"    # expect: request WAS logged
Select-String -Path .\server_redaction.log -Pattern ([regex]::Escape($token)) # expect: NO matches (token absent)
Select-String -Path .\server_redaction.log -Pattern "axiom_dev_password"      # expect: NO matches
Select-String -Path .\server_redaction.log -Pattern "REDACT|\*\*\*|Bearer \*" # expect: the masked form, if any
```

**Option B — if the app already writes a structured log file**, first *find* it
(`Get-ChildItem -Recurse -Filter *.jsonl`, or check the logging config for the path), confirm it exists
(`Test-Path`), then run the same three greps against the confirmed path.

**Success criteria (all three):**
1. the correlation id **is present** (proving the request was logged),
2. the raw access token string is **absent** (0 matches),
3. the DB password (`axiom_dev_password`) is **absent** (0 matches) —
plus, ideally, one log line showing the Authorization value rendered in its **masked** form.

## 5. TRACKED (unchanged, non-blocking)
- OBS-2 / C-5 green CI run (all gates already proven green manually on target).
- TD-012 npm-audit critical/high (schedule + risk-assess).

## 6. DISPOSITION
**W1-U02: CONDITIONAL — still one item from APPROVED.** C-1/C-3/C-4/C-6 remain satisfied from the prior
round; **C-2 is still open** because its verification never actually read a log. Re-run with a confirmed
log-file path (Option A is simplest), show the cid present + token/password absent, and I will approve
immediately. **No next Build Order until then.**

**Note to the DA/operator:** this is purely an evidence-capture fix — point the grep at a log file that
exists. A `Select-String` that errors with "path does not exist" is not a passing security check; it is a
non-result. First `Test-Path` the log, then grep it.

---

## EVIDENCE CONFIDENCE STATEMENT
- **Evidence Reviewed:** operator console — authenticated request 200 with a real Bearer token + cid; five
  `Select-String` calls that **failed with "path does not exist"**; blank redaction results.
- **Confidence Level:** **HIGH** that C-2 is **not** demonstrated (the log was never read). No change to
  C-1/C-3/C-4/C-6 (still met). No approval on a check that did not run.
- **Remaining Unknowns:** whether the structured logs actually redact the token at runtime (the whole
  point) — still unproven.
- **Additional Evidence Required:** C-2 redaction log sample against a **confirmed-existing** log file
  (cid present; raw token + DB password absent).

---

*"An authenticated request fired — but every log grep hit 'path does not exist,' so nothing was inspected.
A blank from a broken search is not proof the token was redacted; it is proof the check didn't run. Point
it at a log file that exists, show the token isn't there, and this approves. We don't guess. We prove."*
— AXIOM ITRGA
