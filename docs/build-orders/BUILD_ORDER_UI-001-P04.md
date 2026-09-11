# BUILD ORDER — UI-001-P04
## Workspace Persistence via `operator_workspace_preferences` (session restore · operator-scoped · no schema creep)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-001 · **Phase:** P04
**Predecessor:** `ITRGA_REVIEW_UI-001-P03.md` — **APPROVED WITH OBSERVATIONS** (authorizes this order)
**Governing spec:** `15_UI-001_IMPLEMENTATION_SPECIFICATION.md` **Part VII** (State/Session Coordination, §12 Session Persistence / §13 Deep Linking / §14 History); design-plan **R-4**; W7-U02 persistence contract.
**Baseline (must be unchanged):** platform v0.62.0 · Alembic head `20260717_0037` · backend 413 · frontend 24f/85t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Wire the P03 session-only layout seam to **durable, operator-scoped persistence** so the workstation **restores the previous session after login** (last workspace, layout, dock positions, panel visibility/sizes, expanded/collapsed, recent searches/artifacts, favorites). Persistence **reuses the existing `operator_workspace_preferences` table** (migration `20260717_0034`, W7-U02) — **NO new table, NO new migration, NO schema change (R-4 "no schema creep").**

## 2. Scope IN
1. **Persistence via the existing table** — store shell layout/preferences under the existing `operator_workspace_preferences` semantics (e.g. key `institutional-shell-v1`), using `layout_config` (and `visible_modules` only for allowlisted values, per R-4). Reuse W7-U02's existing repository/API path; **do not add a new endpoint unless strictly necessary** — if any new endpoint is required, it is read/write of preferences only, no execution surface.
2. **Session restore on login** (Part VII §12) — after auth, the shell restores the operator's last workspace + layout + dock/panel state. Deterministic; safe default when no row exists.
3. **Operator-scoping (W7-U02 contract, R-4)** — operator B cannot read/write operator A's shell prefs (valid-token two-operator proof — recall the **W7-U02 isolation-probe lesson**: each `/auth/login` must return **200 with a non-empty token** before trusting downstream 403/200; a blank-token 200 is an R7 non-result).
4. **Forbidden-field + secret-marker validation preserved** — the shell preference row passes W7-U02's existing validation; no secrets/credentials/forbidden fields persisted.
5. **Deep Linking (§13) + History (§14)** as presentation seams where they intersect restore — direct route access restores the appropriate workspace; history/recent must **not expose sensitive information** (§14).

## 3. Scope OUT (do NOT implement)
- Any **new table / migration / schema column** — reuse `operator_workspace_preferences` only (R-4). If the DA believes a new column is unavoidable, **STOP and request an ITRGA amendment** before building.
- Region-F three-layer overlay split — **P05** (OBS-P01-4). Full command-palette + notifications — **P05**. Legacy `TerminalLayout` retirement — **P06**.
- Any execution/actuation/broker/account surface; external AI; new business capability.

## 4. Constitutional & architectural guardrails (binding)
- **UG-1/UG-2/R-3** — no execution/actuation anywhere; persistence stores presentation state only (no order/broker/account data).
- **R-4 / no schema creep** — head `20260717_0037` **unchanged**; NO new Alembic revision; `operator_workspace_preferences` columns unchanged (prove via `information_schema` if a forbidden column is alleged).
- **W7-U02 contract not bypassed** — operator-scoped, forbidden-field validated, no-orphan audited.
- **UG-15** — no new dependency without a spike.
- **No regression** — every route + all P01/P02/P03 tests still green.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)

**(a) Build-identity** — `sed -n '1,15p'` of the P04 delivery report; confirm it is OF P04 (grep P04 markers, not a stale re-attach — this has recurred; I will check).

**(b) 🔴 PERSISTENCE-CAPTURE CONTROL (MANDATORY — an API read-back NEVER substitutes; W7-U02/W4-U02/W6-U04 precedent).** Since P04 **reuses** an existing table (no new table), the control applies to the **shell preference row** specifically:
  - **b1 — Committing path:** the code/script that writes the shell preference (repository/service call), shown in source.
  - **b2 — Raw `psql SELECT ≥1 row`** on **`operator_workspace_preferences`** showing the actual persisted **shell** row (e.g. `WHERE preference_key='institutional-shell-v1'`), INLINE, raw psql — not an API response.
  - **b3 — No-orphan audit JOIN** for the shell-preference write → `orphan_count 0` (raw psql).
  - **b4 — `operator_id → operators.id` no-orphan JOIN** → `orphan_count 0` (raw psql).
  - **b5 — No schema creep:** `alembic current` = `20260717_0037`; if any new column alleged, `information_schema.columns` proof that `operator_workspace_preferences` is unchanged.

**(c) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_shell_layout_persists_via_operator_workspace_preferences_no_new_table`
  - `test_shell_layout_restores_previous_session_after_login`
  - `test_shell_preferences_operator_scoped_B_cannot_read_A` (valid non-empty tokens — assert both logins 200 w/ token first)
  - `test_shell_persistence_no_execution_or_actuation_and_no_secret_fields`

**(d) Two-operator API isolation proof (operator-run, W7-U02 style)** — login A (200 + non-empty token), login B (200 + non-empty token), then: B_READ_A → 403; B_VISIBLE_A_COUNT → 0; B_WRITE_A → 403; A reads own → 200. Show the tokens are non-blank.

**(e) No-actuation source grep** (shell/persistence source, tests excluded) — `buy|sell|place_order|execute|go-live|order_ticket|connect-broker|account_id` → clean. *(Also closes OBS-P03-1 form.)*

**(f) Regression** — backend `pytest -q` **≥413 passed** (incl. `test_workspace_preferences.py` still green); frontend Vitest **>24f/85t** all passing; TS clean; build + bundle delta.

**(g) No backend/schema drift beyond reused persistence** — `git diff --name-only` shows NO new alembic revision, NO schema column change; head `20260717_0037`.

**(h) Browser (served session)** — shots: change layout (resize/dock/collapse) → **sign out → sign back in → layout restored**; safe default for a fresh operator; Gate CLOSED/research framing; logged-out block.

**(i) Local CI** — `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (or the TD-W6-CI-AUDIT env-flake surfaced AFTER substantive gates green — record, disposition via operator).

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; **(b) full persistence-capture control satisfied with INLINE raw psql** (committing path + SELECT ≥1 shell row + both no-orphan JOINs orphan_count 0 + no-schema-creep) — *a missing/API-only persistence proof ⇒ Corrective Actions Required*; (c) four named tests displayed passing; (d) two-operator isolation with non-blank tokens; (e) no-actuation grep clean; (f) regression green with actual totals; (g) head unchanged + no new migration/column; (h) browser restore demonstrated; CI exit 0 (or waived env-flake). **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-001-P05` (Overlay/Notifications/Command Palette + a11y hardening; folds OBS-P01-4 Region-F three-layer split).**

*We don't guess. We prove.*
