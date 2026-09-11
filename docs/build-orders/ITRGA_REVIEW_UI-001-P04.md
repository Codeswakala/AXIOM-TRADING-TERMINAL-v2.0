# ITRGA REVIEW — UI-001-P04
## Workspace Persistence via `operator_workspace_preferences` (session restore · operator-scoped · no schema creep)

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-001 · **Phase:** P04
**Build Order under review:** `BUILD_ORDER_UI-001-P04.md`
**Evidence pack:** `DELIVERY_REPORT_UI-001-P04.md`, `operator results.md` (correct P04 target transcript, 1683 lines), 2 served-session screenshots (login → restored Operations).
**Determination:** ✅ **APPROVED WITH OBSERVATIONS**
**Authorizes:** `BUILD_ORDER_UI-001-P05` (Overlay/Notifications/Command Palette + a11y hardening; folds OBS-P01-4 Region-F three-layer split).
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity verification (done FIRST) — PASS
Pack is OF P04: **48** `UI-001-P04` refs, only **1** `UI-001-P03` ref (predecessor path check), **25** hits on the four P04 named tests. Not stale/concatenated. DA: "Not self-approved." Operator disclosed the network dropped mid-final-command — assessed below (§2, CI).

---

## 1. Verification matrix (Level-I, line-by-line)

| # | Requirement | Evidence (transcript line) | Verdict |
|---|---|---|---|
| **(b) 🔴 PERSISTENCE-CAPTURE CONTROL — inline raw psql (reuse-existing-table variant)** | committing path + SELECT ≥1 shell row + 2 no-orphan JOINs + no schema creep | see breakdown below | **PASS (FULL)** |
| — b1 committing path | source | `persistence/shellPreferences.ts` (`SHELL_WORKSPACE_KEY="institutional-shell-v1"`, `layout_config`) + committing script `scripts/ui_001_p04_seed_shell_preference.py` (repo `create_preference`) (L65–98) | **PASS** |
| — b2 raw psql SELECT ≥1 row | `operator_workspace_preferences` | `psql … WHERE workspace_key='institutional-shell-v1'` → **1 real row**: preference_id 73e5a6f8…, operator_id a24c3315…, `layout_config` (active_workspace `monitor.operations`, last_route `/signals`, panel_layout placements), research_status **research_only**, audit_correlation_id eef49c24… (L118–121) | **PASS** |
| — b3 audit no-orphan JOIN | orphan_count 0 | `shell_preference_orphan_audit_count` = **0** (L125–129) | **PASS** |
| — b4 operator_id → operators.id JOIN | orphan_count 0 | `shell_preference_orphan_operator_count` = **0** (L132–135) | **PASS** |
| — b5 no schema creep | head + information_schema | `alembic current` = **`20260717_0037 (head)`** (L150); `information_schema.columns` forbidden-column probe (order/broker/account/pnl/gate/secret/api_key/token) → **(0 rows)** (L145, L156) | **PASS** |
| **(c) Four named tests displayed passing** | R-2-class | frontend: `…persists_via_operator_workspace_preferences_no_new_table` (L215), `…restores_previous_session_after_login` (L216), `…no_execution_or_actuation_and_no_secret_fields` (L217); backend: `tests/test_ui_shell_preferences.py::test_shell_preferences_operator_scoped_B_cannot_read_A PASSED` (L342) | **PASS (all 4)** |
| **(d) Two-operator API isolation (W7-U02 style, non-blank tokens FIRST)** | 403/0/403 | `LOGIN_A 200` / `TOKEN_A_PRESENT True`; `LOGIN_B 200` / `TOKEN_B_PRESENT True`; `A_READ_A 200`; **`B_READ_A 403`**; **`B_VISIBLE_A_COUNT 0`**; **`B_WRITE_A 403`** (L1036–1043) — isolation-probe lesson honored | **PASS** |
| **(e) No-actuation + no-secret source grep** | clean | persistence source scan `buy|sell|place_order|execute|…|access_token|jwt|password|secret|api_key|private_key` → **no output** (L1047–1049). Also closes OBS-P03-1 form | **PASS → OBS-P03-1 CLOSED** |
| **(f) Regression + growth** | backend ≥413, frontend grown | Backend **414 passed** (L966, up from 413 — +1 persistence test); frontend full **25 files / 89 tests passed** (L314–315, up from 24f/85t); ruff `All checks passed!` (L967) | **PASS** |
| **(g) No backend/schema drift beyond reused persistence** | head unchanged, no new migration/column | head `20260717_0037`; information_schema 0 rows (b5); no new Alembic revision | **PASS** |
| **(h) Browser (served) — restore after login** | sign-out → sign-in → restored | Screenshots: `/login` → restored Operations with persisted layout (Context Panel widened, panels docked, nav expanded) matching persisted `layout_config`; Gate CLOSED/research framing; logged-out block | **PASS** |
| **Constitutional line** | Gate CLOSED, no execution, no secrets persisted | persistence stores presentation state only; research_only marker; grep clean; audit no-orphan | **PASS** |
| **(i) Local CI** | exit 0 or waived | `LOCAL_CI_EXIT_CODE: 1` — offline `npm audit` (`getaddrinfo ENOTFOUND registry.npmjs.org`) AFTER **414 backend + ruff green**; network dropped mid-command per operator = **TD-W6-CI-AUDIT** env-flake | **WAIVED by operator** |

---

## 2. CI disposition (network-drop-induced env-flake)
The wrapper ran substantive gates green — backend **414 passed** + `All checks passed!` (ruff) — then died at the offline npm-audit step with `getaddrinfo ENOTFOUND registry.npmjs.org`, yielding `LOCAL_CI_EXIT_CODE: 1` and no `==> Local CI equivalent complete` sentinel (consistent: the run ended at audit). The operator disclosed the network disconnected during this command. This is the recurring **TD-W6-CI-AUDIT** class (offline/proxy audit endpoint), which surfaced *after* all substantive gates passed. **Operator waived** (consistent with all prior instances). Fix remains: networked rerun / graceful-audit; **never `strict-ssl false`**.

## 3. Observations (non-blocking)
- **OBS-P04-1 (CI form):** resubmit a networked `scripts/local_ci.sh` run showing `LOCAL_CI_EXIT_CODE: 0` + the `==> Local CI equivalent complete` sentinel at P05 intake (trivial; prior P03 run already demonstrated this passes when networked).
- **Carried closures resolved this phase:** OBS-P03-1 (exact no-actuation source grep) ✅.
- **Still carried:** F-2 (OBS-P01-4) Region-F three-layer overlay split → **P05 (now due)**; F-3 (OBS-P01-5) full token architecture → P05.

## 4. Determination & rationale
**APPROVED WITH OBSERVATIONS.** P04 is a substantively clean pass. The decisive gate — the **persistence-capture control** — is satisfied to the letter with **inline raw psql**: a committing path, a real persisted shell row on `operator_workspace_preferences`, both no-orphan JOINs at `0`, and a proven **no schema creep** (head `20260717_0037`, information_schema forbidden-column probe empty, no new table/migration) — honoring R-4 and the W7-U02 contract without any API-read-back substitution. Operator-scoping is proven by a textbook two-operator isolation (non-blank tokens verified first, then 403/0/403) plus a backend test. All four named tests are displayed passing, the no-actuation/no-secret grep is clean, regression grew cleanly (backend 414, frontend 25f/89t), and the browser demonstrates session restore after login. The sole non-green item is the offline-audit CI exit-1 — a network-drop-induced TD-W6-CI-AUDIT env-flake occurring after all substantive gates green — **waived by operator**.

Per the UI-Transformation vocabulary, **Approved with Observations authorizes progression.** → **`BUILD_ORDER_UI-001-P05` is authorized.** P05 must fold the now-due **OBS-P01-4 (Region-F three-layer overlay split)** and continue **OBS-P01-5 (token architecture)**; close OBS-P04-1 (networked CI) at P05 intake.

Baseline unchanged (no schema change): v0.62.0 / head `20260717_0037` / backend **414** / frontend **25f·89t**. Residuals unchanged & non-blocking: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT.

*We don't guess. We prove.*
