# ITRGA REVIEW — W7-U03

## Research Management Collections & Tags

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Unit:** W7-U03 (Wave 7) · **Reviewed pack:** `DELIVERY_REPORT_W7-U03.md` + `DELIVERY_REPORT_W7-U03_EVIDENCE_FIX.md` + `operator results.md` + 3 screenshots
**Build Order:** `BUILD_ORDER_W7-U03.md`
**Review date:** 2026-07-18
**Platform of record (pre-unit):** v0.56.0 · head `20260717_0034` · backend 366 / frontend 19f·61t
**Verdict:** 🟡 **CONDITIONAL APPROVAL** — every risk control proven; two named evidence items open (C-1 raw forbidden-column query; C-2 standalone alembic-current). **Version bump to v0.57.0 HELD.**
**Confidence:** HIGH. **Governance Gate:** CLOSED. **Motto:** *We don't guess. We prove.*

---

## 0. Build-identity check (done FIRST)

- `DELIVERY_REPORT_W7-U03.md`: Unit W7-U03, cites Build Order + W7-U02 FINAL; target v0.57.0, head `20260717_0037`. ✔
- `DELIVERY_REPORT_W7-U03_EVIDENCE_FIX.md`: DA self-reported **E-1** — the seed script `ModuleNotFoundError: No module named 'app'` made an initial run a non-result (zero rows); corrected by fixing the import path. **Honest self-flag — welcome.** ✔
- `operator results.md`: the corrected run (`W7_U03_RESEARCH_MANAGEMENT_SEED_COMPLETE`, real rows). ✔

---

## 1. What is PROVEN (Level-I)

| # | Requirement | Evidence | Result |
|---|---|---|---|
| b | Backend tests | `test_research_management.py` **11 passed** (named suite incl. all §4 tests) | ✅ |
| — | Full backend regression | **377 passed** (+11 over 366); broker suite green | ✅ |
| — | Frontend | **20 files / 64 tests passed** | ✅ |
| — | Migration applied | CI "Alembic upgrade head against PostgreSQL"; all three tables return `(3 rows)` on raw SELECT (schema at 0035/0036/0037 exists) | ✅ (see C-2 re: standalone `alembic current`) |
| **f** | **R7-5 NO-MUTATION (CENTRAL)** | `SOURCE_BEFORE_HASH == SOURCE_AFTER_HASH` (`920292ae…` identical) → `SOURCE_IDENTITY_UNCHANGED=True`; `SOURCE_AUDIT_BEFORE=1 == SOURCE_AUDIT_AFTER=1` → `SOURCE_AUDIT_UNCHANGED=True` | ✅ |
| d | Persistence-capture (3 tables) | raw SELECT ≥1 row each (3 rows each); **six no-orphan JOINs all 0** (audit ×3 + operator ×3) | ✅ |
| g | Two-operator isolation (valid tokens) | `LOGIN_A/B 200`; `B_READ_A_COLLECTION 403` + `B_VISIBLE_A_COLLECTION_COUNT 0`; `B_READ_A_TAG 403` + `B_VISIBLE_A_TAG_COUNT 0` | ✅ |
| h | **Authorize-before-validate (OBS-W7U02 folded in)** | `B_MUTATE_A_COLLECTION_EMPTY_BODY_STATUS: 403` (403 not 422) + `B_DELETE_A_TAG 403` | ✅ |
| i | No secrets/PII | `stored_secret_marker_count 0` across names/descriptions/tags + JSON grep clean | ✅ |
| — | Browser (GR7-10) | served `localhost:8000/research-management`: "Reference-only research organization… AXIOM does not act", "Per-operator scoping is enforced", collections/tags over existing artifacts (RESEARCH_ONLY), member references by (type,id); **no actuation controls**; logged-out `localhost:8000/login` | ✅ |
| k | No barred dependency | grep clean | ✅ |
| l | CI (GR7-11) | `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** | ✅ |
| m | Gate CLOSED | `test_gate_remains_closed_for_wave7` (in suite) + broker suite green | ✅ |

**The red line — organizing must never mutate the organized — is proven** (identical source hash + unchanged source audit), isolation holds with valid tokens (0 visible), cross-operator mutation is 403 before body validation, and all three tables are audited/no-orphan.

---

## 2. CONDITIONS

### 🟡 C-1 — The §5(e) raw `information_schema` forbidden/source-content column query was NOT operator-run.
Build Order §5(e) named: an `information_schema.columns` query over all three tables proving the §2 forbidden columns (+ no `source_artifact_content`/materialized-copy column) are **absent** → 0 rows. The operator transcript contains **`information_schema` 0 times.** The property is covered by the passing in-process test `test_research_management_tables_have_no_forbidden_or_source_content_columns` (one of the 11), but — as at W6-U04 C-1 — a passing test does not substitute for the **named raw schema query**, and "no source-content column" is a core R7-5/data-model guarantee that a milestone-grade unit must show directly.
**To close C-1:** run, on target, `SELECT column_name FROM information_schema.columns WHERE table_name IN ('research_collections','research_collection_members','research_tags') AND column_name IN (<§2 forbidden list + 'source_artifact_content'>)` → **0 rows**.

### 🟡 C-2 — Standalone `alembic current = 20260717_0037` not shown (LOW, corroborated).
The operator transcript shows CI "Alembic upgrade head against PostgreSQL" and all three tables live with data, so the schema is demonstrably at `0037` — but the standalone `alembic current` line + three revision-file `Test-Path` (§5(c)) are absent. Minor form gap.
**To close C-2:** submit `alembic current` = `20260717_0037 (head)` on PostgreSQL + confirm the three revision files exist.

---

## 3. Classification

- **C-1** — MEDIUM (named raw forbidden/source-content column proof missing; proven only by in-process test; the no-source-content guarantee must be shown directly).
- **C-2** — LOW (head corroborated via CI-migrate + live tables; owes the one-line standalone proof).
- No CRITICAL, no HIGH. R7-5 no-mutation, isolation, authorize-before-validate, no-orphan ×6, no secret/PII, Gate CLOSED — all proven Level-I. Per proportionality (R13): every *risk* item proven, two *named* items open ⇒ **CONDITIONAL**, not WITHHELD. **v0.57.0 HELD** (platform stays v0.56.0).

---

## 4. Not a finding / commended

- **E-1 (DA self-flagged, resolved):** the seed `ModuleNotFoundError` made an initial run a non-result; the DA disclosed it in `..._EVIDENCE_FIX.md` and re-ran with rows created — exactly the right posture (a blank/errored step is a non-result, not a pass). No penalty; commended for honesty.
- Browser logged-out is `localhost:8000/login` with URL bar; acceptable (auth test passes); the workspace/research route protection is consistent with the passing auth test.

---

## 5. Path to FINAL

On C-1 (raw `information_schema` → 0 rows) and C-2 (standalone `alembic current 0037`), I will write `ITRGA_VERDICT_W7-U03_FINAL.md` superseding this CONDITIONAL, bump to **v0.57.0** (head `20260717_0037`), update onboarding, and W7-U04 (API Ecosystem Catalogue & Versioned Research API Hardening) becomes authorizable.

---

## 6. Posture note

A strong unit: the R7-5 red line is proven with matching source hashes and unchanged source audit, isolation is clean with valid tokens, and the W7-U02 authorize-before-validate hardening landed (cross-operator mutation now 403, not 422). The two open items are evidence-form — a raw forbidden-column query and a one-line alembic-current — both closable in minutes. Organize the research without altering it: proven. Close the named schema proofs and this unit is FINAL.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
