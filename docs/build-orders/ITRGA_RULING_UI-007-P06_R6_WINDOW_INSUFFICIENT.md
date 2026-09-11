# ITRGA RULING — UI-007-P06 R-6 Visibility Diagnostic

**Authorized remedy proven INSUFFICIENT · DA diagnosis CORRECTED · R-6 re-scoped**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Unit | UI-007-P06 — Completion Checkpoint |
| In response to | `UI-007-P06_R6_VISIBILITY_DIAGNOSTIC.md` + 2 raw API artifacts |
| **DISPOSITION** | ⚠️ **Remedy 1 WITHDRAWN as insufficient** · **DA diagnosis corrected** · **R-6 second limb RE-SCOPED** |
| Determination status | UI-007-P06 remains **Corrective Actions Required** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Ruling in brief

1. **The remedy I authorized does not work.** `category=SECURITY&limit=200` cannot reach the target row. That is my error to correct, not the DA's.
2. **The DA's diagnosis is wrong** — this is **not** a server/database misconfiguration. No misconfiguration is evidenced. **Do not act on `CHECK_SERVER_DATABASE_CONFIGURATION`.**
3. **No integrity fault exists.** The audit trail is intact and the API is behaving correctly.
4. **R-6's second limb is re-scoped** to a form that is provable today (§5).

---

## 2. Independent analysis of the raw artifacts (I parsed the JSON myself)

The DA supplied the raw API responses. I analysed them rather than relying on the runner's summary — and the runner's own counter is misleading.

| Measurement | Value |
|---|---|
| Rows actually returned by `?category=SECURITY&limit=200` | **200** (the runner reported `SECURITY_ROW_COUNT: 1` — see OBS-P06-3) |
| Category purity of those rows | **200/200 `SECURITY`** — filter works correctly |
| Newest returned | `2026-07-29T05:53:09Z` |
| **Oldest returned** | **`2026-07-18T21:36:20Z`** |
| **Target row (`055e3295…`)** | **`2026-07-18T19:59:07Z`** (= `22:59:07+03`) |
| Target inside `[oldest, newest]`? | **NO** — it is **~1 h 37 m OLDER than the oldest row returned** |
| Total audit rows (stats API) | **640** |
| DB backend (stats API) | `postgresql` / `postgresql+asyncpg` |

**This is decisive.** The 200-row newest-first cap truncates *before* reaching the target. The row is not missing from the API's data — it is beyond the reach of **any** newest-first read with `limit ≤ 200`, because `SECURITY` rows alone now exceed 200.

**The endpoint is working exactly as specified.** `category` filters correctly; `limit` caps at its documented maximum of 200. Nothing is broken.

---

## 3. 🔴 The DA's diagnosis is CORRECTED — no database misconfiguration

The diagnostic emitted:

```
PSQL_ROW_PRESENT_BUT_API_SECURITY_WINDOW_MISSING__CHECK_SERVER_DATABASE_CONFIGURATION
```

**That inference is not supported by the evidence, and I am striking it.** The reasoning behind it — psql sees the row, the API doesn't, therefore they may be different databases — is a reasonable hypothesis, but the artifacts refute it:

- The stats API reports `backend: postgresql`, `database_url_scheme: postgresql+asyncpg` — the **same PostgreSQL** the psql query hit.
- The stats API reports **`audit_count: 640`** — the server sees a full audit corpus, not a truncated or empty one.
- The API returned 200 `SECURITY` rows spanning **2026-07-18 → 2026-07-29**, i.e. it reaches back to the *same day* as the target.
- The exclusion boundary is explainable **entirely** by row count, to the minute.

**Had this diagnosis stood unchallenged, it would have sent the DA to investigate a phantom database fault — or, worse, seeded doubt about audit-trail integrity at the exact moment this workstream is being certified.** There is no integrity fault. The audit trail is sound. **`TD-AXIOM-GIT-PROVENANCE` remains the only genuine infrastructure finding open.**

This is why R-6 requires the psql row *and* the served row: the two together localise the problem precisely. They did their job here.

**Commendation stands:** the DA hit a wall, produced raw artifacts rather than prose, offered a hypothesis explicitly flagged as needing a check, and did **not** proceed on it. Its hypothesis was wrong; its conduct was right. Supplying the raw JSON is what let me refute the hypothesis in minutes.

---

## 4. Remedy 1 is WITHDRAWN — my authorization was insufficient

I authorized `category=SECURITY&limit=200` on the reasoning that category scoping is deterministic where a general limit is not. **That reasoning assumed the SECURITY partition was under 200 rows. It is not** — it is at least 200 and truncates ~1h37m short of the target.

I did not verify the partition size before authorizing. **That is an ITRGA error, recorded under R19 as the second such correction in this workstream** (the first being the C-2 baseline-ref demand at P04). The DA implemented and tested exactly what I authorized; the shortfall is mine.

**Remedy 1 is withdrawn.** Do not pursue it further.

---

## 5. R-6 second limb — RE-SCOPED (this is now the closing requirement)

The control's purpose is to prove the served UI renders a stored `*_REFUSED` code **verbatim, as a refusal, not reinterpreted as an authorization path.** That property does **not** depend on which refusal row demonstrates it.

**Authorized substitute — prove the property on a reachable refusal row:**

1. **Identify a `*_REFUSED` row inside the served window.** Run raw psql against `audit_events` for rows whose `details->>'reason_code'` ends in `_REFUSED`, ordered newest-first, and select one that falls within the explorer's loaded set.
2. **Show it in psql** — full row: `id · category · action · actor · resource_type · resource_id · reason_code · created_at`.
3. **Show the same row in the served Audit Explorer detail pane**, matching field-for-field.
4. **Existing rows only.** No audit event may be created, no timestamp altered, no chronology touched. *(Unchanged and non-negotiable.)*

**If no `*_REFUSED` row exists within the served window**, then say so with evidence — a psql query showing the newest `*_REFUSED` row and its position relative to the window — and R-6's second limb is **discharged as environmentally unprovable at P06**. In that case it converts to a **tracked residual** under OBS-P06-2, and I will close CA-P06-1 on the strength of the psql limb plus the passing named test `test_ui007_completion_verbatim_no_cherry_picking_and_residual_disclosure_hold`.

**No product source change is authorized.** The merge remedy is off the table; the Audit Explorer fetch seam stays as it is.

---

## 6. Findings

| ID | Severity | Status |
|---|---|---|
| **CA-P06-1** | HIGH | ❌ **OPEN — re-scoped per §5** |
| **ITRGA-ERR-2** | RECORDED (R19) | Remedy 1 authorized without verifying the SECURITY partition size. Withdrawn. **ITRGA error, not DA** |
| **DA-DIAG-1** | CORRECTED | `CHECK_SERVER_DATABASE_CONFIGURATION` is **struck** — no misconfiguration evidenced; same PG, 640 rows, boundary explained by row count |
| **OBS-P06-3** | OBSERVATION (new) | Runner reported `SECURITY_ROW_COUNT: 1` while the artifact contains **200** rows — the counter mis-measures (likely `.Count` on a non-enumerated object). A wrong count in an evidence harness is an R7 hazard: fix before it understates a real result |
| **OBS-P06-2** | MEDIUM (upgraded) | **Now quantified:** with 640 audit rows and >200 in `SECURITY` alone, refusal records older than the 200-row ceiling are **permanently unreachable from the UI**. This is a genuine institutional governance-visibility limitation, not an evidence inconvenience. **To close:** a future authorized enhancement — server-side reason-code filtering, pagination, or date-range selection — under its own Build Order. Disclose on the governance surface |
| — | **COMMENDATION** | The DA produced raw artifacts, halted on an unproven hypothesis, and requested disposition rather than acting. That is precisely why this resolved correctly and quickly |

---

## 7. Disposition

**UI-007-P06 remains Corrective Actions Required, with the closing requirement re-scoped to §5.**

The situation is now fully understood: the audit trail is intact, the API is correct, the endpoint's 200-row ceiling simply cannot reach a refusal from 18 July, and my authorized remedy was insufficient because I did not check the partition size first. No database fault exists and none should be investigated.

Everything else in the P06 pack stands proven — five completion tests, all whole-surface boundary greps, the R-6 psql limb, 61f/276t, backend 414, alembic head, CI exit 0, Doc-16, UI-001/UI-002 integration, nine residuals dispositioned, and the logged-out block.

**One artifact remains**: a refusal row shown in psql *and* in the served UI — any reachable one — or evidence that none is reachable, in which case the limb converts to a tracked residual and I close it.

Verification is limited to supplied evidence, which in this instance was sufficient: the raw JSON permitted direct measurement rather than inference.

**Baseline does NOT advance — v0.62.0 · backend 414 · frontend 60f/271t of record** (61f/276t proven, pending). **UI-007 completion NOT DECLARED.** Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**.

---

## 8. Evidence Confidence Statement

- **Evidence reviewed:** `UI-007-P06_R6_VISIBILITY_DIAGNOSTIC.md` (28 lines); `UI-007-P06_R6_VISIBILITY_SECURITY_API.json` (200 records, parsed and measured directly); `UI-007-P06_R6_VISIBILITY_STATS_API.json`.
- **Confidence:** **HIGH** that the exclusion is a 200-row cap, not a fault — the target predates the oldest returned row by ~1h37m, and all 200 rows are correctly category-filtered. **HIGH** that no database misconfiguration exists — same backend, 640 rows, same-day coverage. **HIGH** that the runner's row counter is defective.
- **Remaining unknowns:** whether any `*_REFUSED` row falls inside the served window — determinable by the §5 query.
- **Additional evidence required:** §5.

---

*The psql row and the served row exist as a pair precisely so a gap between them can be located. It was — and it pointed at my authorization, not at the database.*

**We don't guess. We prove.**

*— AXIOM ITRGA*
