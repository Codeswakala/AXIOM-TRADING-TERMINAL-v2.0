# AXIOM BUILD ORDER — W5-U02

## Human-AI Collaboration: Audited Assistant Research Responses (persisted, grounded, non-actuating, read-only — still no external LLM)

**Build Order ID:** W5-U02
**Wave:** 5 — Human-AI Collaboration · **Unit:** 02
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **W5-U01 APPROVED — CLEAN** (Platform v0.39.0; assistant non-actuating/grounded/injection-refusing, audited) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07/08_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-5 guardrails **GR-1…GR-11**; this unit carries
**R5-2, R5-3, R5-5, R5-6, R5-7** + standing **R5-1/R5-8** (`ITRGA_REVIEW_WAVE5_DESIGN_PLAN.md`).
**Governing plan:** `WAVE5_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §4.3 (response record), §6.1
(assistant panel), §7 (`assistant_research_responses`), §10 (W5-U02).
**Builds on:** W5-U01 (`collaboration` context, `AssistantPort`, non-actuating registry, grounding/refusal +
audit).
**Baseline to meet/exceed:** backend **244** / frontend **12 files · 29 tests**; Platform **v0.39.0**; head
**20260716_0023**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

W5-U02 **persists** the assistant's grounded research responses and refusals (the W5-U01 foundation currently
audits behavior via `audit_events` but stores no response record) into a dedicated
`assistant_research_responses` table, and exposes them **read-only**. Every stored response carries **grounding
source ids + provenance + disclaimer**; every refusal is recorded with its reason; **the assistant remains
non-actuating and grounded-or-refuses, and there is still NO external LLM.** An optional presentation-only
assistant panel may be added — if so, **browser evidence is mandatory** (R5-6).

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No un-audited persisted record (R5-7 — KEYSTONE, INLINE).** The new `assistant_research_responses` table
  triggers the persistence-capture control: Alembic head advance + committing script + **raw `psql SELECT ≥1
  row` on `assistant_research_responses`** + **no-orphan audit JOIN** (each response row ↔ its
  `assistant.response_draft_created`/`assistant.refused` audit event; `orphan_count 0`) — inline in the first
  submission. `research_status` mandatory.
- ❌ **Assistant still non-actuating (R5-1 standing) + grounding-or-refuse (R5-5).** Persisting a response
  mutates/triggers nothing beyond its own audited record; a stored response either has grounding source ids or
  is a recorded refusal (no ungrounded claim persisted). Re-run the tool-registry non-actuation test + the
  grounding-or-refuse test.
- ❌ **Injection/secret refusal re-run + AUDITED (R5-3).** The six W5-U01 named refusal tests re-run and PASS;
  refusals persist with reason codes; sampled stored-output secret-marker check clean (GR-11). **No raw request
  text stored** — store `request_text_hash` only (privacy; §4.3).
- ❌ **No external LLM / no new compiled or LLM dependency (R5-2).** Deterministic local assistant only. Any
  LLM is a future hard-gated unit. Unspiked/LLM import ⇒ FAIL.
- ❌ **Disclaimer on every stored + displayed response (R5-6).** The §4.5 disclaimer is on every response
  record and (if a panel is added) on screen — proven by test + **browser screenshot**. Grounding sources +
  refusal reasons shown; **no secret/raw-internal display.**
- ❌ **Read-only API.** `GET` list + detail, authenticated: unauth **401** / auth **200**; POST/mutation →
  **405/404**. No endpoint lets a caller make the assistant act.
- ❌ **No execution / order / broker / account / Gate path** (GR-1/GR-3). **R5-8 wave-wide grep** (command +
  output, extended verbs) — residuals limited to forbidden-key lists/refusal codes/benign seams, disclosed.
- ❌ **No D-W2-001 breach; no client-side authoritative recompute (GR-8) if UI.**
- ❌ **No regression** (Wave-0…W5-U01). Full suite green + **CI via documented Git-Bash path →
  `LOCAL_CI_EXIT_CODE: 0`** + parity smoke (transcript W5-U02).
- ✅ **Preserve:** advisory/research-first, presentation-only UX, tz-UTC, market-agnostic, all prior hardening,
  npm-audit 0, ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.** R5-7 (audited persistence, inline) + R5-3 (audited refusal re-run) are
the keystones; R5-6 browser proof is mandatory **if** any panel is added.

---

## 3. Scope (Components A–D)

### A. Response persistence (backend, `collaboration`)
- `assistant_research_responses` table + Alembic migration + committing repository/script.
- Store per §4.3: `assistant_response_id, created_at(UTC), operator_id/actor, request_text_hash,
  assistant_policy_version, provider_name/version, model_or_engine_version, source_artifact_ids,
  grounding_summary, response_text, limitations, disclaimer, research_status, audit_correlation_id`.
  **No raw request text; no secret/raw-internal; no order/sizing/account field.**
- On create: immutable audit event (`assistant.response_draft_created` for grounded; `assistant.refused` +
  reason for refusals). No orphan by construction.

### B. Read-only API
- `GET /api/v1/collaboration/assistant-responses` (list) + `GET …/{response_id}` (detail) — authenticated,
  read-only. Unauth **401**; POST **405/404**. No emit/act endpoint.

### C. (Optional) presentation-only assistant panel
- If added: shows grounded response + **grounding sources** + **refusal reasons** + **disclaimer**; **no
  execution controls; no secret display; no client recompute**; **browser screenshots** from a reachable served
  session (R5-6). If no UI, state so — API + tests suffice.

### D. Tests + registers
- Named: R5-7 persistence/no-orphan; R5-3 six refusals re-run + audited; R5-5 grounding-or-refuse; R5-1
  registry non-actuation; disclaimer present; no-raw-text/secret; read-only API 401/200/405. Update RISK,
  CHANGELOG → **v0.40.0**, PROJECT_STATE, ADR, GOVERNANCE_AMENDMENTS (Option A/Gate CLOSED).

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL)

Report `DELIVERY_REPORT_W5-U02.md` + raw `operator results.md` (+ browser shots if panel). **Build identity
first.**

1. **Build identity** — new files/ADR; v0.40.0; `git log -1 --oneline`.
2. **R5-7 persistence (inline)** — Alembic head advance + `alembic current`; committing script; **raw
   `psql SELECT ≥1 row` on `assistant_research_responses`**; **no-orphan audit JOIN** (`orphan_count 0`;
   response↔audit event).
3. **R5-3 re-run + audited** — six refusal tests PASS by name; `SELECT … FROM audit_events WHERE
   resource_type='assistant_response'` shows refusals w/ reason codes; sampled stored-output secret check clean;
   confirm **no raw request text** stored (only `request_text_hash`).
4. **R5-5 grounding-or-refuse** — named test PASSED; a persisted grounded response shows `source_artifact_ids`.
5. **R5-1 non-actuation** — tool-registry test re-run.
6. **R5-6 disclaimer** — test asserts disclaimer on every response; if panel, **browser screenshot** (grounded
   response + sources + refusal reason + disclaimer + no-exec + logged-out block).
7. **API** — unauth **401**; **list 200** + **detail 200** (non-blank echoes); POST → **405/404**.
8. **R5-2** — no LLM/dep grep; existing stack only.
9. **R5-8 wave-wide grep** — command + output; residuals disclosed + benign; Gate CLOSED.
10. **Full regression** — backend `pytest` **≥ (244 + new)**, 0 failed; frontend green; ruff/tsc/build clean;
    npm audit 0.
11. **CI** — Git-Bash → `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** (transcript W5-U02).
    **Parity smoke.**

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.40.0.
- [ ] **R5-7 (keystone):** `assistant_research_responses` Alembic head advanced; committing script + **raw
      SELECT ≥1 row** + no-orphan audit JOIN (`orphan_count 0`) — inline.
- [ ] **R5-3:** six refusal tests re-run PASS; refusals persisted/audited w/ reason codes; sampled secret check
      clean; **no raw request text** stored (hash only).
- [ ] **R5-5** grounding-or-refuse (test + persisted source ids); **R5-1** registry non-actuation re-run.
- [ ] **R5-6:** disclaimer on every response (test); if panel → browser shots (response+sources+refusal+
      disclaimer+no-exec+logged-out).
- [ ] Read-only API 401 / list-200 / detail-200 / POST-405.
- [ ] **R5-2** no LLM/dep; **R5-8** grep empty/benign (command+output); Gate CLOSED; no D-W2-001 breach.
- [ ] No regression; full suite green; **CI via Git-Bash → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke; browser
      evidence if UI.
- [ ] DA does not self-approve, self-advance, build W5-U03+, ship an LLM, add an actuating tool/execution/
      order/account linkage, or open the Gate.

**A single CRITICAL, unmet mandatory evidence, or a red gate ⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA
approves W5-U02, advances to **v0.40.0**, and (on operator authorization) issues `BUILD_ORDER_W5-U03.md`
(Chart Research Annotations & Drawing Tools) carrying R5-4/R5-6/R5-7/R5-8 + presentation-only.

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Annotations/drawings/workspaces/journal/scenario/closeout (W5-U03…U08, each own Build Order).
- Any external LLM/API or new compiled/LLM dependency (future gated unit).
- Any actuating assistant tool; any execution/order/sizing/broker/account/position path; opening the Gate.
- Storing raw request text or any secret/raw-internal; any ungrounded persisted claim.
- Any Wave-6 work.

---

## 7. Notes to the Development Authority

This unit gives the assistant a **memory that is fully accountable**: every stored response is grounded +
disclaimed + audited, every refusal is persisted with its reason, and **no raw request text or secret is
stored** (hash + redaction). Deliver the **raw SELECT + no-orphan audit inline** (R5-7). Keep it **LLM-free**
(R5-2). If you add a panel, it is presentation-only and **must be shown in the browser** (R5-6, W3-U05/W0-U06).
Re-run the injection/refusal + non-actuation tests. Run CI via the **documented Git-Bash path** for a clean
exit 0. Prove build identity first; disclose grep residuals with output.

DA does not self-approve, self-advance the version, build W5-U03+, ship an external LLM, add an actuating tool
or any execution/order/account linkage, or open the Gate. The next unit follows ITRGA's verdict + a new Build
Order + operator authorization.

> **We don't guess. We prove.** — ITRGA
