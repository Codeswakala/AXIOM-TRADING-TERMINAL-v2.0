# Wave 7 Engineering Design and Implementation Plan

## Institutional Platform — Research Terminal, Gate Closed

| Field | Value |
|---|---|
| Wave | **7 — Institutional Platform** |
| Prepared by | AXIOM Development Authority |
| Prepared for | ITRGA review under `docs/build-orders/ITRGA_REQUEST_WAVE7_DESIGN_PLAN.md` |
| Date | 2026-07-18 |
| Platform of record | **v0.54.0** |
| Alembic head | **20260717_0033** |
| Status | **Submitted design plan — no Wave-7 construction authorized** |
| Milestone predecessor | Execution Research Environment Complete — declared by ITRGA |
| Constitutional posture | Governance Gate **CLOSED**; no live execution/broker/account path authorized |

---

## 0. DA Non-Authorization Statement

This document is a **design plan only**. It does not authorize implementation of W7-U01 or any Wave-7 unit.

The Development Authority will not build any Wave-7 unit until:

1. ITRGA reviews and accepts this design plan;
2. ITRGA issues a specific Wave-7 Build Order; and
3. the operator authorizes that Build Order.

Wave 7 is the final roadmap wave. It turns AXIOM into an institutional research terminal, but not into a live execution, broker, account, or real-money platform. The Constitutional Governance Gate remains **CLOSED**.

---

## 1. Scope and Non-Scope

### 1.1 In-scope Wave-7 interpretation

Wave 7 may build institutional platform capabilities that organize, secure, expose, and scale existing governed research artifacts:

- workspace customization and saved operator preferences;
- research portfolio dashboards over existing advisory/simulated artifacts;
- research management, tagging, search, and collections;
- strategy laboratory over pre-registered simulation/research artifacts;
- plugin contracts with sandboxed, least-privilege extension points;
- authenticated, versioned API ecosystem for research artifacts;
- advanced reporting/export over existing research artifacts;
- enterprise scalability, observability, and performance hardening;
- multi-user readiness with default-deny RBAC and per-operator scoping.

### 1.2 Explicit non-scope

Wave 7 does **not** authorize:

- live broker adapter;
- broker SDK or exchange SDK;
- broker credentials;
- real orders, order routing, or go-live switch;
- real account, real position, real balance, margin, capital, or real P&L;
- opening the Governance Gate;
- plugin access to broker/order/account/live seams;
- unauthenticated data APIs;
- cross-operator leakage;
- external LLM/API inside a feature or plugin unit;
- production SSO/MFA unless a separate Build Order explicitly names it;
- Wave-8 work, because there is no Wave 8 in the current roadmap.

---

## 2. Roadmap Component Fence Map

| Component | Permitted interpretation | Construction fence | Prohibition proof |
|---|---|---|---|
| Workspace customization | Per-operator presentation preferences over existing research surfaces. | Stored preferences are UI/layout only, scoped to operator. | Schema excludes action/order/account fields; browser no-actuation test. |
| Portfolio dashboard | Research aggregation over advisory/simulated artifacts. | Uses simulated/research labels and no real account source. | Forbidden account/balance/margin/P&L columns; no live portfolio API. |
| Research management | Tag/search/collections over governed artifacts. | Metadata only; original artifact content/audit immutable. | No mutation of source artifacts; audit on tags/collections. |
| Strategy laboratory | Pre-registered simulation/research experiments reusing Wave-6 machinery. | Server-side governed experiment plans only; no live bridge. | No-look-ahead, no cherry-picking, Gate CLOSED, no broker path. |
| Plugin architecture | Extensions only through published sandboxed contracts. | Contract allowlist; no arbitrary imports; no broker/account/Gate APIs. | Hostile-plugin refusal tests and containment grep. |
| API ecosystem | Authenticated, versioned read/research APIs. | Bearer auth, RBAC, per-operator scoping, rate/abuse guard. | 401/403 tests, no execution endpoints, no secret payloads. |
| Advanced reporting | Export/report existing artifacts with uncertainty/disclaimers. | Report/export renderer reads governed artifacts only. | No real-P&L/guarantee tests; no orphan audit for exported report records if persisted. |
| Enterprise scalability | Performance/observability/scaling of research platform. | Does not weaken auth, audit, or Gate controls. | Regression, metrics, redaction, auth tests. |
| Multi-user readiness | Coarse roles/RBAC readiness and per-operator scoping. | Default-deny permissions; existing `operators` identity. | Two-operator isolation tests; no Gate-opening role. |

---

## 3. Binding Wave-7 Guardrail Design Responses

| Guardrail | Design response |
|---|---|
| GR7-1 Gate stays CLOSED | Every Wave-7 unit carries Gate CLOSED proof and broker suite where applicable. No plugin/API/role can open or reach the Gate. |
| GR7-2 Research/advisory only | All surfaces remain research/presentation/metadata/reporting only; no real execution, account, position, balance, margin, capital, or real P&L. |
| GR7-3 Broker/plugin containment | Broker logic remains only in External Integration. Plugins operate only through published contracts; no import of broker/order/account modules. |
| GR7-4 Uncertainty/stat≠economic | Analytics/reporting/portfolio/strategy lab outputs carry uncertainty, sample count, limitations, and separate economic usefulness. |
| GR7-5 API ecosystem auth/abuse guard | New APIs are authenticated, versioned, scoped, and documented; unauth 401, forbidden 403, no execution endpoints, no secret payloads. |
| GR7-6 Plugin sandbox/least privilege | Plugins cannot import broker/live/execution modules, cannot open sockets to venues, cannot read secrets, and cannot mutate governed artifacts outside contracts. |
| GR7-7 Multi-user readiness | Roles default-deny; per-operator scoping is tested with two operators; no role can open Gate or reach execution. |
| GR7-8 No secrets/PII leaks | Extend secret-marker checks to API/export/plugin/reporting surfaces; structured logs remain redacted. |
| GR7-9 Persistence capture | Every new table requires Alembic, committing script, raw SELECT, and no-orphan audit JOIN. `operator_id -> operators.id`. |
| GR7-10 UI browser proof | UI units require served-browser screenshots, research framing, no action controls, and logged-out block. |
| GR7-11 Git-Bash CI | Every unit includes Git-Bash CI transcript with `LOCAL_CI_EXIT_CODE: 0`, or a formally accepted TD only if operator/ITRGA authorizes. |
| GR7-12 No unspiked dependency | No new plugin runtime/API framework/RBAC/compiled/LLM dependency without spike and ITRGA review; broker SDK barred. |
| GR7-13 External LLM future-gated | No external LLM/API in Wave-7 feature/plugin units without separate hard-gated Build Order. |

---

## 4. Proposed Bounded Contexts / Packages

### 4.1 Institutional Platform bounded context

Proposed backend package, when authorized:

```text
backend/app/institutional_platform/
```

Responsibilities:

- workspace preferences;
- research collections/tags;
- RBAC policy contracts;
- API catalogue/version metadata;
- reporting/export metadata;
- plugin contract registry metadata.

Non-responsibilities:

- broker connectivity;
- order routing;
- account/position state;
- model training;
- live execution;
- Gate state.

### 4.2 Plugin subsystem boundary

If authorized, plugin contracts should live under:

```text
backend/app/institutional_platform/plugins/
```

with:

- explicit contract interfaces;
- allowlisted capabilities;
- no dynamic code execution in early Wave 7;
- built-in reference plugins only unless separately authorized;
- sandbox refusal tests.

### 4.3 API ecosystem boundary

API ecosystem work should extend existing FastAPI router patterns, with:

- versioned route contracts;
- auth dependencies;
- role/permission checks;
- OpenAPI/tag organization;
- endpoint inventory and tests;
- rate/abuse guard if proposed.

---

## 5. Data Model Plan

No data model is authorized until a Build Order.

Candidate tables, subject to refinement:

### 5.1 Operator workspace preferences

```text
operator_workspace_preferences
```

Candidate fields:

```text
preference_id
created_at
updated_at
operator_id -> operators.id
workspace_key
layout_config
visible_modules
theme_config
research_status
metadata
 audit_correlation_id
```

Forbidden:

```text
order_payload
broker_account_id
account_id
position_id
execution_status
real_pnl
Gate/open flags
```

### 5.2 Research collections / tags

```text
research_collections
research_collection_members
research_tags
```

Purpose: organize existing governed artifacts without mutating original artifact content.

Each member references artifact type/id and stores operator attribution. No source artifact mutation.

### 5.3 RBAC readiness tables

Potential tables only if authorized:

```text
operator_roles
operator_permissions
operator_role_assignments
```

Design preference: start with policy constants/tests before schema if possible. If persisted, default-deny and no Gate/execution permission exists.

### 5.4 API catalogue

```text
api_contract_catalog
api_access_audit_summary
```

Optional if needed for documentation and enterprise API inventory.

### 5.5 Plugin contracts

```text
plugin_contracts
plugin_contract_capabilities
plugin_execution_audit_events
```

Only if plugin unit is authorized. No arbitrary code/plugin execution by default.

### 5.6 Advanced reports

```text
advanced_research_reports
report_exports
```

Report/export artifacts over existing governed research, with disclaimer, uncertainty, limitations, source artifact ids, and no real-P&L/guarantee framing.

---

## 6. Security and Containment Test Plan

Mandatory Wave-7 test families:

```text
test_gate_remains_closed_for_wave7
test_no_execution_or_broker_endpoint_in_wave7_api
test_api_requires_auth_for_all_institutional_routes
test_rbac_default_denies_unprivileged_operator
test_two_operator_isolation_no_cross_operator_leakage
test_plugin_contract_disallows_broker_order_account_imports
test_hostile_plugin_request_refused_and_audited
test_workspace_customization_has_no_action_fields
test_reports_exports_have_no_secret_or_pii_markers
test_wave7_bright_line_grep_no_execution_path
```

Every unit pack must include:

- exact named tests;
- auth status table;
- grep output;
- no secret marker checks;
- persistence-capture for new tables;
- browser screenshots for UI units;
- Git-Bash CI.

---

## 7. UI Plan

Wave-7 UI surfaces should be institutional research terminal surfaces:

- dashboard/workspace preference management;
- research collection/tag explorer;
- API documentation/catalogue surface if authorized;
- plugin contract catalogue if authorized;
- portfolio research dashboard over simulated/advisory artifacts if authorized;
- advanced report builder/export preview if authorized.

UI rules:

- research/advisory framing visible;
- no execution/order/broker/account controls;
- no go-live/execute/connect-broker affordances;
- logged-out blocks;
- per-operator scoping visible where relevant;
- uncertainty/disclaimers visible for analytics/reports.

---

## 8. Analytics and Reporting Method Plan

Any Wave-7 reporting/analytics must:

- read existing governed artifacts;
- preserve source artifact ids;
- preserve uncertainty and limitations;
- report sample count and method;
- separate statistical metrics from economic usefulness;
- avoid real-P&L claims;
- avoid guaranteed return language;
- include deterministic report hash if persisted;
- audit creation/update;
- include no-orphan proof.

---

## 9. Dependency Declaration

Wave 7 starts with existing stack only:

```text
Python / FastAPI / SQLAlchemy / Alembic / Pydantic
React / TypeScript / Vite / Vitest
```

Explicit non-dependencies:

- no broker SDK;
- no exchange SDK;
- no external LLM/API;
- no plugin runtime package by default;
- no new compiled dependency by default;
- no SSO/MFA provider package unless separately authorized.

Any proposed dependency requires:

- compatibility spike;
- security review;
- no-secret/no-PII review;
- ITRGA approval in the relevant Build Order.

---

## 10. Standing Security Debt Disposition

| Item | Design posture |
|---|---|
| `admin/admin123` local default | Remains local/dev evidence profile only with insecure-dev flag; Wave 7 should harden documentation and avoid production framing. |
| Full RBAC/MFA | RBAC readiness may be designed; production MFA/SSO requires separate Build Order if proposed. |
| WS JWT-in-query TD-022 | Already mitigated with WS tickets; Wave 7 API review should ensure no regression. |
| Refresh rotation | Existing refresh rotation present; Wave 7 may add tests/inventory if auth hardening unit is authorized. |
| TD-W6-CI-AUDIT | Resolved at W6 closeout per final verdict; keep CI audit network assumptions documented. |

---

## 11. Proposed Unit Decomposition

### W7-U01 — Institutional Platform Security & API Foundation

Purpose: prove the Wave-7 safety envelope before new institutional features.

Scope:

- API/RBAC policy skeleton;
- endpoint inventory for institutional routes;
- default-deny permission model;
- two-operator isolation tests;
- Gate CLOSED proof;
- no execution endpoint grep;
- no new table unless explicitly authorized.

### W7-U02 — Operator Workspace Customization

- per-operator preferences;
- layout configuration;
- no action fields;
- persistence-capture;
- browser proof.

### W7-U03 — Research Management Collections & Tags

- organize existing artifacts;
- no mutation of source artifacts;
- operator scoping;
- audit and no-orphan.

### W7-U04 — API Ecosystem Catalogue & Versioned Research API Hardening

- API catalogue and docs;
- auth/role tests;
- abuse/rate guard if authorized;
- no execution endpoints.

### W7-U05 — Plugin Contract Safety Foundation

- published extension contracts;
- no arbitrary plugin execution initially;
- hostile-plugin refusal tests;
- no broker/order/account imports.

### W7-U06 — Portfolio Research Dashboard / Advanced Reporting

- research dashboard over advisory/simulated artifacts;
- uncertainty/disclaimers;
- no real account/P&L.

### W7-U07 — Enterprise Scalability & Multi-User Readiness Hardening

- performance/observability/auth hardening;
- two-operator isolation proof;
- route inventory and regression.

### W7-U08 — Wave-7 Closeout & Platform Completion

- full-wave no-execution/API/plugin/security proof;
- artifact audit completeness;
- browser E2E;
- docs/register reconciliation;
- milestone candidate: Institutional Platform Complete.

---

## 12. Recommended W7-U01 Scope

Recommended first Build Order:

> **W7-U01 — Institutional Platform Security & API Foundation**

Acceptance criteria should include:

- no new user feature unless minimal evidence endpoint/inventory is authorized;
- Gate CLOSED proof;
- no execution/order/broker/account endpoint;
- API auth inventory;
- RBAC policy skeleton, default-deny;
- two-operator isolation tests;
- no secret/PII checks;
- no new dependency unless explicitly authorized;
- full regression and Git-Bash CI.

---

## 13. Bright-Line Self-Check

| Capability | Gate closed | No execution | Auth/RBAC | Operator isolation | No secrets | Browser proof if UI | Persistence capture if table |
|---|---:|---:|---:|---:|---:|---:|---:|
| Security/API foundation | Yes | Yes | Yes | Yes | Yes | If UI | If table |
| Workspace preferences | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Research management | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| API ecosystem | Yes | Yes | Yes | Yes | Yes | If UI | If table |
| Plugin contracts | Yes | Yes | Yes | Yes | Yes | If UI | If table |
| Portfolio/reporting | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Scalability/readiness | Yes | Yes | Yes | Yes | Yes | If UI | If table |
| Closeout | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

---

## 14. ITRGA Review Request

The Development Authority submits this Wave-7 Engineering Design and Implementation Plan for ITRGA review.

No Wave-7 implementation is authorized by this plan. DA awaits ITRGA review, binding refinements, a future W7-U01 Build Order, and operator authorization before beginning Wave-7 construction.

The Constitutional Governance Gate remains **CLOSED**.

---

**End of Wave 7 Engineering Design and Implementation Plan**
