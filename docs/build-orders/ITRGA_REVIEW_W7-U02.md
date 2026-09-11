# ITRGA REVIEW — W7-U02

## Operator Workspace Customization

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Unit:** W7-U02 (Wave 7) · **Reviewed pack:** `DELIVERY_REPORT_W7-U02.md` + `operator results.md` + 3 screenshots
**Build Order:** `BUILD_ORDER_W7-U02.md`
**Review date:** 2026-07-18
**Platform of record (pre-unit):** v0.55.0 · head `20260717_0033` · backend 359 / frontend 18f·58t
**Verdict:** 🟡 **CONDITIONAL APPROVAL** — feature proven; the mandatory **two-operator isolation API proof is a non-result** (broken probe) and must be re-run (C-1). **Version bump to v0.56.0 HELD.**
**Confidence:** HIGH on what was proven; C-1 is an invalid-evidence gap (not a proven leak, but NOT a proven isolation either).
**Governance Gate:** CLOSED (verified). **Motto:** *We don't guess. We prove.*

---

## 0. Build-identity check (done FIRST)

- `DELIVERY_REPORT_W7-U02.md`: Unit W7-U02, cites Build Order + W7-U01 FINAL; target v0.56.0, head `20260717_0034`. ✔
- `operator results.md`: fresh pack (ADR-065, `operator_workspace_preference.py`, migration `0034`, `WorkspaceCustomizationPage`). ✔

---

## 1. What is PROVEN (Level-I)

| # | Requirement | Evidence | Result |
|---|---|---|---|
| b | Named backend tests | `test_workspace_preferences.py` **6/6 named PASSED** (+1) | ✅ |
| — | Full backend regression | **366 passed** (+7 over 359); broker suite green | ✅ |
| — | Frontend | **19 files / 61 tests passed** (+1 file, +3 tests) | ✅ |
| c | Migration/head | `0033 → 0034`; `alembic current = 20260717_0034` | ✅ |
| d | Persistence-capture | raw `SELECT` from `operator_workspace_preferences`; **no-orphan audit JOIN = 0**; **operator-vs-operators JOIN = 0** | ✅ |
| e | Forbidden columns | `information_schema` for order/account/position/pnl/balance/margin/capital/gate → **(0 rows)** | ✅ |
| g | No secrets/PII | `stored_secret_marker_count = 0` across layout/theme/visible/metadata; grep clean | ✅ |
| — | Presentation-only | `research_status` present; UI banner "Presentation preferences only… AXIOM does not act."; `test_workspace_customization_has_no_action_or_account_or_execution_fields` PASS | ✅ |
| — | Auth required | `test_workspace_preferences_require_auth` PASS | ✅ |
| h(browser) | Browser evidence | served `localhost:8000/workspace`: Workspace Customization, per-operator scoping copy, "Presentation preferences only" disclaimer, preference editor/saved/detail, **no execution/actuation controls**; Ops Dashboard v0.56.0 W7-U02; login page for logged-out | ✅ (see C-1 re: logged-out) |
| j | No barred dependency | grep clean | ✅ |
| k | CI (GR7-11) | `npm audit → 0 vulnerabilities`, `==> Local CI equivalent complete`, **`LOCAL_CI_EXIT_CODE: 0`** | ✅ |
| gate | Gate CLOSED | `test_gate_remains_closed_for_wave7` PASS; broker suite green | ✅ |

The feature itself — per-operator, presentation-only, audited, no-orphan, no forbidden columns, no secrets, Gate CLOSED, CI green — is proven.

---

## 2. CONDITION

### 🟡 C-1 — The two-operator isolation API proof is a NON-RESULT (broken probe) — R7-3 not validly demonstrated at the API level.
Build Order §5(f) + R7-3 require an operator-run two-operator API isolation: operator B, **authenticated with B's own token**, cannot read/list/mutate operator A's preference (403/empty) + 0 leakage. The transcript instead shows:

```
Invoke-RestMethod : {"detail":[{"loc":["body","username"],"msg":"Input should be a valid string","input":null},
                              {"loc":["body","password"],... "input":null}]}   ← BOTH logins (A and B) FAILED
A_READ_A_PREF_STATUS:200
B_READ_A_PREF_STATUS:200        ← looks like a leak, but was made with NO valid token
B_LIST_STATUS:401               ← confirms the token was invalid/blank
B_VISIBLE_A_PREF_COUNT: 1       ← computed by parsing a 401 error body as JSON — garbage
B_WRITE_A_PREF_STATUS:405
```

**Root cause:** the login bodies used PowerShell variables (`$OperatorAUsername`/`$OperatorBUsername`/`$EvidencePassword`) that were **never assigned** — the seed printed `OPERATOR_A_USERNAME`/`PASSWORD` as *text* but did not set the shell vars. So **both `/auth/login` calls returned 422 (null username/password)**, `$TokenA`/`$TokenB` are empty, and the subsequent 200s were served to an **unauthenticated/lingering-session** request, not to operator B. The `B_LIST_STATUS: 401` corroborates that the token was invalid; `B_VISIBLE_A_PREF_COUNT: 1` is a parse of the 401 error body.

**This is an R7 non-result, and it is disqualifying on its own terms:** the isolation property that this entire wave's security foundation exists to guarantee is **not proven at the API level**. It is **NOT** evidence of an actual leak (the 200s carried no valid B identity; the in-process `test_workspace_preferences_are_operator_scoped_two_operator_isolation` PASSES), but per the standing rule a blank/errored variable is a non-result (R7), and a 200 that *looks* like cross-operator read cannot stand unexplained in the record.

**To close C-1:** re-run the two-operator isolation with **valid, distinct A and B access tokens** (set `$OperatorAUsername`/`$OperatorBUsername`/`$EvidencePassword` from the seed, confirm each `/auth/login` returns 200 with a token), then show:
- `B_READ_A_PREF_STATUS: 403` (B cannot read A's preference),
- `B_LIST_STATUS: 200` with **`B_VISIBLE_A_PREF_COUNT: 0`** (B's list contains none of A's rows),
- `B_WRITE_A_PREF_STATUS: 403/405`,
- and (optional but welcome) a raw `psql` cross-operator scoping check → 0.
Credentials/IDs may be masked; the two operators must be provably distinct.

---

## 3. Classification

- **C-1** — MEDIUM (mandatory named evidence is a non-result; the property is asserted by a passing in-process test but NOT validly proven at the operator-run API level as required; transcript contains misleading 200s that must be corrected).
- No CRITICAL, no HIGH — there is **no proof of an actual leak**; the 200s are unauthenticated-session artifacts of a broken probe. But there is also **no valid proof of isolation**, so approval is held. Per proportionality (R13): feature risk items proven, one *named* mandatory proof invalid ⇒ **CONDITIONAL**, not WITHHELD. **v0.56.0 HELD** (platform stays v0.55.0).

---

## 4. Not a finding / disclosed

- The `200`/`count 1` values are **not** accepted as a leak nor waved away — they are diagnosed as a broken (null-token) probe and must be re-run correctly (C-1). I will not relabel a confusing 200 as either "green" or "breach" without valid evidence.
- Browser logged-out shot is the `/login` page; acceptable given the passing auth test, but the corrected C-1 rerun should confirm the workspace route rejects an unauthenticated request (401/redirect) so the logged-out item is unambiguous.

---

## 5. Path to FINAL

On a valid C-1 rerun (B authenticated with B's token → 403 read / 0 visible / write blocked), I will write `ITRGA_VERDICT_W7-U02_FINAL.md` superseding this CONDITIONAL, bump to **v0.56.0** (head `20260717_0034`), update onboarding, and W7-U03 (Research Management Collections & Tags) becomes authorizable.

---

## 6. Posture note

The feature is clean — presentation-only, audited, no-orphan, no forbidden columns, no secrets, Gate CLOSED, CI green. The single blocker is the **isolation proof itself**, which was invalidated by unset login variables: both `/auth/login` calls 422'd, so the "B read A → 200" is a token-less artifact, not a demonstration. On the highest-attack-surface wave, per-operator isolation must be **proven**, not implied by a green in-process test. Re-run it with real B credentials and this unit is FINAL.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
