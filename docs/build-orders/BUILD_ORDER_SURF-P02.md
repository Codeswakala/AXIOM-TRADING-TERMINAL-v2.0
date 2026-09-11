# BUILD ORDER — SURF-P02

**Issuing authority:** Independent Technical Review & Governance Authority
**Authorized by:** Operator, 2026-08-17
**Programme:** SURF — Surface the unsurfaced · Phase 2 of 3
**Base:** `34f4c62` + item3 (`b7b4c4f7…`) + item5 (`4c03910c…`) + item6 (`f65da5c3…`) + item4 Rev B (`a516c2c1…`) + SURF-P01 (`62c4d021…`) + OBS-SURF1-2 (`69964afe…`)
**Predecessor:** SURF-P01 — APPROVED WITH OBSERVATIONS, no open findings
**Closes:** `TD-061`

---

## 1. OBJECTIVE

Blueprint §5, verbatim:

> **SURF-P02** **Alerts** — closes `TD-061`. Left-rail badge with unread count, dock tab, acknowledge action, severity styling.

Technical debt register, line 69:

> `TD-061` | Alert UI indicator absent | Low-Med | **Reduced** W3-U08 adds read-only alert panel to Operations dashboard for closeout visibility; richer alert UI still deferred | Future UI unit

**This Build Order is the "future UI unit" that register entry defers to.** On approval, `TD-061` moves from *Reduced* to *Closed*.

---

## 2. VERIFIED STARTING STATE

Established by ITRGA against the base chain. The DA must not restate these as claims.

### 2.1 Backend — three endpoints

`backend/app/api/routes/monitoring_alerts.py`, prefix `/alerts`:

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/alerts` | List, filterable by `alert_type`, `severity`, `subject_type`, `subject_id`, `acknowledged`; `limit` 1–200, default 50 |
| `GET` | `/alerts/{alert_id}` | Single alert; 404 if absent |
| `POST` | `/alerts/{alert_id}/ack` | *"Acknowledge an alert read-state only (operator-authenticated)"* |

Severity is `Literal["info", "warning", "critical"]` (`monitoring/service.py:29`).

### 2.2 The acknowledge write — verified, not assumed

I read the service rather than trusting the docstring. `monitoring/service.py:237-259`:

```python
alert.acknowledged = True
alert.acknowledged_at = utc_now()
alert.acknowledged_by = actor
await self._session.flush()
await self._audit.append(category="GOVERNANCE", action="monitoring_alert.acknowledged", ...)
```

**Three read-state fields plus an audit entry. Nothing else is mutated.** The subject model is untouched — `test_monitoring_alert_ack_does_not_mutate_subject_model` already guards this at `test_monitoring_alerts.py:207`.

**This write is materially different from SURF-P01's five excluded POSTs.** Those would have *created research artifacts* in the execution-adjacent domain. This one records that a human read a notice. It is named in Blueprint §5 as in-scope, it is audit-logged, and it cannot alter any analytical or execution state.

**It is therefore IN SCOPE** — with the guards in §4.

### 2.3 Frontend — almost nothing reaches it

```
api/client.ts:989   fetchMonitoringAlerts(limit = 5)   ← the only client function
acknowledgeAlert / acknowledgeMonitoringAlert          ← 0 matches
GET /alerts/{alert_id}                                 ← no client function
```

**`components/alerts/MonitoringAlertsPanel.tsx` — 41 lines, 0 `data-testid`, and mounted nowhere.** Its only importer is its own test file. It is an orphan: built, tested, unreachable by any operator.

It currently renders: title, a read-only disclaimer, error/loading/empty states, and per-alert `alert_type`, `summary`, `subject_type/subject_id`, `Ack: yes|no`, and a severity badge via `severityClass()` mapping `critical → danger`, `warning → degraded`, else `stub`.

**The default `limit = 5` is a silent truncation** of an endpoint that accepts up to 200 — the same class as SURF-P01's `slice(0, 5)` fills defect.

### 2.4 No frontend T-1 guard

`backend/tests/test_monitoring_alerts.py` has five tests including `test_drift_alert_triggers_no_retrain_model_change_order_or_auto_action` and `test_alert_record_is_inert_and_alert_code_has_no_execution_path`. **None pins a frontend path** — the same gap SURF-P01's M1 closed for execution research.

---

## 3. SCOPE

### IN SCOPE

**S1 — Surface the alerts UI in the terminal.** Left-rail badge with unread count, plus a dock tab or panel. The DA selects the home and states reasoning. Blueprint §5 names the left-rail badge explicitly; a right-dock tab is plausible here given alerts are short list items — unlike the wide surfaces of CONV.

**S2 — Unread count.** Derived from `acknowledged=false`. **Must be a genuine count from the API, never a placeholder.** If the count cannot be determined, render absence — not `0`.

**S3 — Acknowledge action.** Add the client function for `POST /alerts/{alert_id}/ack` and wire it to a control. Subject to §4.

**S4 — Severity styling.** Preserve the existing `critical → danger`, `warning → degraded`, `info → stub` mapping. All three `Literal` values must be handled.

**S5 — Surface `GET /alerts/{alert_id}`.** Currently unreachable. Selecting an alert should retrieve its record.

**S6 — Remove or disclose the `limit = 5` default.** Either raise it with a stated value, or disclose the truncation in the UI. A limit the operator cannot see is a quiet inaccuracy (`OBS-CONV2-1` family).

**S7 — `data-testid` across all regions.** Baseline 0. Prior deliveries: 8, 10, 20, 17, 23, 20, 27.

### OUT OF SCOPE

SURF-P03 · DATA · CHART · POLISH · `TD-062` (external notification providers — *"explicitly out of W3-U06; future gated provider work"*) · the 697 kB bundle (POLISH-P01) · `F-BRAND-1` · **any backend endpoint, schema, model or service change**. The three endpoints exist and are sufficient.

**No alert creation, dismissal, deletion, or bulk mutation.** Only `ack` exists; only `ack` may be surfaced.

---

## 4. 🔴 MANDATORY — THE ACKNOWLEDGE CONTROL

**M1 — Acknowledge is read-state only, and must read that way.** Label it `Acknowledge` or `Mark as read`. **Never** `Resolve`, `Dismiss`, `Clear`, `Fix`, `Action`, or `Handle`. An operator must not be able to infer that acknowledging changed anything about the underlying condition. The alert's subject is untouched; the UI must not imply otherwise.

**M2 — No optimistic update.** The acknowledged state renders only after the API confirms. On failure, surface the error explicitly and leave the alert unacknowledged. This is the M2 discipline from CONV item 3, and it matters more here because the control writes an audit record.

**M3 — Acknowledging must not hide the alert by default.** It is a read-state marker, not a delete. The acknowledged alert remains visible with its state shown. A filter to hide acknowledged alerts is acceptable **if it is operator-selected and not the default**.

**M4 — Frontend T-1 guard.** Extend `test_monitoring_alerts.py` with a source-inspection test over the new alerts UI module, following the SURF-P01 M1 pattern:
- **non-vacuity anchors** — positive assertions that the file contains the surface,
- absence of `place_order`, `submit order`, `go live`, `connect broker`, `broker_account`, `retrain`, `remediate`, `auto_action`, `resolve_alert`, `execute`.

The `retrain` / `remediate` / `auto_action` terms mirror the existing backend guard at `:79`. The alerts domain's specific T-1 risk is an alert appearing to *trigger* a corrective action.

---

## 5. STANDING REQUIREMENTS

**R1 — Preserve every capability** in §2.3, including the disclaimer *"Read-only alerts inform the operator; they do not retrain, remediate, or act."* That sentence is a constitutional honesty surface — keep it, verbatim, wherever the alerts render.

**R2 — No fabricated values.** Unread count, severity, timestamps, subject ids render verbatim or as explicit absence. Never a plausible-looking number.

**R3 — Independent degradation.** If alerts fail to load, the badge and panel say so; nothing else in the shell is affected.

**R4 — Layout.** The `OBS-SURF1-2` fix (`flex-shrink: 0` on stage-scroll children) is in the base. If the alerts surface introduces a new scroll container, verify at 1920×1080 that no panel collapses. **Do not rely on tests alone for this** — it was found by looking at the image.

**R5 — RBAC not widened.** 16/16 `protectedWorkspace()` wrappers, `ALL_AUTHENTICATED_ROLES = ["admin","operator"]`. All three endpoints are `CurrentOperatorDep`-authenticated; the UI must not weaken that.

**R6 — Suite green.** Current: **785 frontend / 416 backend = 1,201**. New surface requires new tests. Never delete a failing test to reach green.

**R7 — `npm ci` before `tsc -b`.**

**R8 — Deletion discipline.** If `MonitoringAlertsPanel.tsx` is superseded rather than extended, delete it and re-point its test in the same cycle. **Do not leave a second orphan.** If it is extended in place, say so — *extended*, not *relocated*.

**R9 — Update `TD-061`** in `docs/governance/TECHNICAL_DEBT_REGISTER.md` line 69 from *Reduced* to *Closed*, citing SURF-P02. This is a governance record the Build Order explicitly closes.

---

## 6. DELIVERY REQUIREMENTS

**Transport — six consecutive hash-reconciled deliveries; repeat exactly.** Neither authority commits to the repository; the verified patch is the artifact of record.

```bash
git diff <base> > surf_p02.patch
git apply --check surf_p02.patch ; echo "exit=$?"
sha256sum surf_p02.patch
```

Inline in the message body · **LF endings, terminating newline** · **state the full base chain explicitly**.

**Report must contain:**

1. Chosen home + reasoning.
2. Capability disposition table — every §2.3 element mapped.
3. Endpoint coverage — all three, marked `surfaced` / `already surfaced`.
4. **M1–M4 confirmations**, including the acknowledge control's exact label text and the T-1 guard's non-vacuity anchors.
5. S6 disposition — limit raised, or disclosure text used.
6. R8 disposition — panel extended or superseded, stated precisely.
7. R9 — the `TD-061` register line, before and after.
8. Raw console transcripts — vitest, tsc -b, vite build, pytest.
9. **Level-I captures attached** — raw PNGs are acceptable and preferred over the HTML gallery, which has failed to upload twice. Required:
   - left-rail badge showing a genuine unread count,
   - the alerts surface populated, all three severities visible if fixtures allow,
   - **an acknowledge interaction** — before and after, with the audit-visible state change,
   - **an empty-state capture scrolled to the empty region**,
   - a load-failure capture showing independent degradation.
10. **Interaction trace** for the acknowledge control — Playwright `elementFromPoint` before click, per the item-4 method. This control writes; hit-testing it is not optional.
11. Exact wording: *deleted* / *relocated* / *copied* / *extended* / *surfaced*.

---

## 7. ACCEPTANCE

1. Alerts reachable in the terminal; left-rail badge with genuine unread count.
2. All three endpoints surfaced, including `GET /alerts/{alert_id}`.
3. **M1** acknowledge labelled as read-state only; no resolve/dismiss/clear semantics.
4. **M2** no optimistic update; failure surfaced explicitly.
5. **M3** acknowledged alerts remain visible by default.
6. **M4** frontend T-1 guard present, non-vacuous, passing.
7. **S4** all three severity values styled.
8. **S6** `limit = 5` truncation removed or disclosed.
9. R1 disclaimer sentence preserved verbatim.
10. R2 no fabricated values; absence renders as absence.
11. `data-testid` across all regions.
12. Suite green ≥ 1,201; nothing deleted to force green.
13. `tsc -b` clean; `vite build` succeeds.
14. RBAC not widened.
15. R8 no orphaned panel left behind.
16. **R9 `TD-061` marked Closed** in the register.
17. Captures attached incl. acknowledge before/after and scrolled empty state; interaction trace supplied.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This Build Order authorizes **SURF-P02 only**. It is not authorization for SURF-P03, DATA, CHART or POLISH.
**Only the `ack` write may be surfaced. No alert creation, dismissal or deletion.**

**We don't guess. We prove.**
