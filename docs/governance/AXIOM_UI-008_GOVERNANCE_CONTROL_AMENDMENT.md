# AXIOM — UI-008 GOVERNANCE CONTROL AMENDMENT
## P03 Forward-Execution & Evidence Integrity Rules

**Authority:** Operator  
**Applies To:** Development Authority (DA) and Independent Technical Review & Governance Authority (ITRGA)  
**Workstream:** UI-008 — Institutional AI Experience  
**Effective Boundary:** UI-008-P03 and all subsequent UI-008 phases  
**Historical Status:** P01, P01-M1, and P02 remain valid and are not reopened by this amendment.

---

## 1. Purpose

This amendment establishes stricter execution, evidence, traceability, and documentation rules for the continuation of UI-008.

The purpose is not to invalidate previous work.

The purpose is to prevent:

- undocumented deviation from the approved Design Plan;
- ambiguity between planned and implemented architecture;
- double-counting of tests;
- unsupported claims in Delivery Reports;
- ITRGA acceptance based solely on assertions;
- undocumented changes to project-state artifacts;
- phase boundaries becoming blurred;
- DA and ITRGA independently redefining the project;
- loss of continuity when either authority changes chat/session.

The governing development chain remains:

```text
Roadmap
    ↓
Design Plan
    ↓
ITRGA Review / Determination
    ↓
Build Order
    ↓
DA Implementation
    ↓
DA Testing & Evidence
    ↓
Delivery Report
    ↓
ITRGA Independent Review
    ↓
Correction, if required
    ↓
ITRGA Determination
    ↓
Next Build Order
```

No authority may silently bypass this chain.

---

# 2. Historical Baseline Preservation

The following milestones are immutable historical baselines unless a future formal determination explicitly states otherwise:

```text
UI-008-P01
Commit: 9b1bdf0
Tag: UI-008-P01_APPROVED
ITRGA: D-30
Status: APPROVED WITH OBSERVATIONS

UI-008-P01-M1
Commit: 30169a4
Tag: UI-008-P01-M1_INTEGRATED
ITRGA: D-45
Status: APPROVED WITH OBSERVATIONS

UI-008-P02
ITRGA: D-47
Status: APPROVED
```

P03 must begin from the **verified P02 repository state**.

The DA must not:

- restart P01;
- recreate P01-M1;
- rewrite approved P02 functionality;
- delete historical evidence;
- alter approved tags;
- rewrite previous Delivery Reports;
- retroactively change previous ITRGA determinations.

Any required correction to historical material must be handled as a separately documented amendment.

---

# 3. Single Active Phase Rule

Only one UI-008 implementation phase may be active at a time.

For P03:

```text
P03 = ACTIVE
P01 = HISTORICAL
P01-M1 = HISTORICAL
P02 = APPROVED / HISTORICAL
P04+ = NOT AUTHORIZED
```

The DA must not implement P04 or later functionality merely because it appears convenient while implementing P03.

If a later-phase dependency is discovered, the DA must document it rather than silently implementing it.

---

# 4. Build Order Is the Implementation Contract

The current Build Order is the authoritative implementation boundary.

The DA may implement:

- explicitly required items;
- technically necessary supporting changes;
- tests required to prove the required behavior;
- documentation required by the Build Order.

The DA may not expand the functional scope merely because:

- a feature appears useful;
- an architectural improvement appears desirable;
- a later phase depends upon it;
- implementation is easier if another feature is added;
- the DA believes the roadmap would benefit from it.

Any scope expansion must be identified explicitly.

---

# 5. Mandatory Deviation Register

Every Delivery Report must contain a section:

```text
## Deviations From Approved Build Order
```

It must contain one of:

```text
NO DEVIATIONS
```

or:

| ID | Build Order Requirement | Actual Implementation | Deviation | Reason | Authority/Determination |
|---|---|---|---|---|---|
| DEV-01 | [requirement] | [actual] | [difference] | [reason] | [reference] |

A deviation must never be hidden inside ordinary implementation prose.

---

# 6. Design-Plan Traceability Rule

Every major implementation component must be traceable through:

```text
Governing Requirement
        ↓
Design Plan Section
        ↓
Build Order Item
        ↓
Implementation
        ↓
Test / Evidence
        ↓
ITRGA Finding
```

If implementation differs from the Design Plan, the DA must explicitly state:

1. what the Design Plan says;
2. what was implemented;
3. why the implementation differs;
4. whether the difference changes scope;
5. whether a Build Order amendment is required.

The DA must not silently rewrite the Design Plan through implementation.

---

# 7. API / Architecture Change Rule

Changes to API routes, contracts, component boundaries, data sources, authentication mechanisms, or architectural seams require explicit traceability.

For every such change the Delivery Report must identify:

```text
Planned Architecture:
[original design]

Implemented Architecture:
[actual implementation]

Reason for Difference:
[technical reason]

Scope Impact:
NONE / MINOR / MATERIAL

Build Order Impact:
NONE / AMENDMENT REQUIRED

Evidence:
[tests / inspection / documentation]
```

For example, if the Design Plan specifies:

```text
/api/v1/assistant/responses
```

but implementation uses:

```text
/api/v1/collaboration/assistant-responses
```

the difference must be explicitly documented and reconciled.

The DA may not simply substitute one architecture for another without recording the change.

---

# 8. Test Accounting Rule

This rule is mandatory.

Every Delivery Report must distinguish:

### A. Previous baseline

Example:

```text
Frontend:
66 suites / 295 tests
```

### B. New tests physically added

Example:

```text
24 new tests
```

### C. Tests removed

Example:

```text
0 removed
```

### D. Tests modified

Example:

```text
5 existing tests modified
```

### E. Current total

Example:

```text
Frontend:
71 suites / 319 tests
```

The DA must never calculate "new tests" by adding overlapping test categories.

If a test belongs to several categories, it may be described under each category, but it must only be counted once in the numerical total.

The Delivery Report must explicitly state:

> **Category counts are descriptive and may overlap; baseline delta counts are authoritative.**

---

# 9. Test Inventory Rule

Each newly introduced test suite must identify:

- file path;
- number of tests;
- purpose;
- requirement tested;
- whether tests are new or modified;
- evidence status.

Example:

| Test Suite | New/Modified | Tests | Requirement | Result |
|---|---|---:|---|---|
| assistantClient.test.ts | NEW | 5 | P03-AC-01 | PASS |
| AssistantCommandSurface.test.tsx | MODIFIED | 7 | P03-AC-02 | PASS |

This prevents vague statements such as "comprehensive tests were added."

---

# 10. Regression Baseline Rule

Every phase must preserve the previous phase's baseline.

The Delivery Report must include:

```text
Previous Baseline
        ↓
Current Result
        ↓
Delta
        ↓
Regression Determination
```

At minimum:

- frontend suites;
- frontend tests;
- backend tests;
- build/type-check;
- relevant security proofs;
- relevant lint/static-analysis results.

Any regression must be explicitly declared.

A passing current suite does not automatically prove absence of regression unless the previous baseline is identified.

---

# 11. Evidence Hierarchy Rule

The ITRGA must distinguish between:

### Direct Evidence
Evidence directly demonstrating the claimed condition.

### Strong Indirect Evidence
Evidence supporting the claim but not directly demonstrating the entire condition.

### Assertion
A statement made by the DA without independently sufficient evidence.

Delivery Reports must not describe assertions as verification.

ITRGA determinations must identify evidence limitations where they exist.

---

# 12. ITRGA Independence Rule

The ITRGA must independently evaluate the DA submission.

The ITRGA must not automatically convert:

```text
DA says X
```

into:

```text
X verified
```

without identifying the evidence supporting X.

For each material acceptance criterion, the ITRGA should record:

```text
Criterion
    ↓
DA Claim
    ↓
Evidence
    ↓
Independent Assessment
    ↓
Finding
```

---

# 13. Delivery Report Completeness Rule

Every Delivery Report must contain, at minimum:

1. Phase identity;
2. Governing Build Order;
3. Design Plan reference;
4. Previous baseline;
5. Implementation summary;
6. Files created;
7. Files modified;
8. Files removed;
9. Scope compliance;
10. Deviations;
11. Test inventory;
12. Regression results;
13. Security evidence;
14. UI/UX evidence where applicable;
15. Documentation changes;
16. Technical debt changes;
17. Known limitations;
18. Evidence index;
19. Proposed next phase;
20. DA sign-off.

A Delivery Report is incomplete if it merely describes successful implementation.

---

# 14. Project-State Synchronization Rule

The following state artifacts must remain synchronized with every completed phase:

```text
PROJECT_STATE.md
CHANGELOG.md
RISK_REGISTER.md
TECHNICAL_DEBT_REGISTER.md
Relevant ADRs
Relevant roadmap/design documents
Delivery Report
ITRGA Determination
```

If an artifact is intentionally not changed, the Delivery Report must state:

```text
PROJECT_STATE.md — NO CHANGE REQUIRED
Reason: [reason]
```

The DA must not silently allow project-state documents to become stale.

---

# 15. Authority Separation

### Operator

The Operator:

- manages workspace continuity;
- authorizes authority initialization;
- provides governing documents;
- issues operational directives;
- manages chat/session transitions;
- does not perform independent technical certification.

### DA

The DA:

- interprets approved Build Orders;
- implements;
- tests;
- documents;
- produces Delivery Reports;
- does not certify its own implementation.

### ITRGA

The ITRGA:

- independently reviews;
- verifies evidence;
- identifies deviations;
- determines compliance;
- approves/rejects/corrects;
- does not implement the work it reviews.

No authority may assume another authority's role.

---

# 16. No Silent Governance Changes

Neither the DA nor the ITRGA may silently change:

- phase definitions;
- acceptance criteria;
- architecture;
- security boundaries;
- documentation requirements;
- evidence requirements;
- authority responsibilities;
- production status;
- governance gate status.

Any such change requires an explicit documented amendment or determination.

---

# 17. Production Certification Firewall

The following states must remain separate:

```text
IMPLEMENTATION COMPLETE
        ≠
PHASE APPROVED
        ≠
WORKSTREAM COMPLETE
        ≠
PRODUCTION CERTIFIED
```

For UI-008:

```text
P02 IMPLEMENTATION COMPLETE
        ↓
D-47 APPROVED
        ↓
P03 AUTHORIZED
```

This does **not** imply:

```text
UI-008 COMPLETE
```

and does **not** imply:

```text
AXIOM PRODUCTION CERTIFIED
```

Production certification remains governed independently by the applicable production-readiness authority.

---

# 18. Phase Boundary Rule

Every Build Order must explicitly contain:

### IN SCOPE

What the DA must implement.

### OUT OF SCOPE

What the DA must not implement.

### DEPENDENCIES

What must already exist.

### ACCEPTANCE CRITERIA

What must be proven.

### EVIDENCE REQUIRED

What evidence the DA must submit.

### EXIT CONDITION

What constitutes completion.

This prevents phase boundaries from becoming progressively broader.

---

# 19. Carry-Forward Rule

At the beginning of every phase, the DA must explicitly identify:

```text
Previous Approved Baseline:
[commit/tag]

Previous ITRGA Determination:
[determination]

Inherited Components:
[list]

Inherited Tests:
[list/count]

Inherited Technical Debt:
[list]

Inherited Observations:
[list]

New Phase Scope:
[list]
```

The DA must not reconstruct project history from memory.

---

# 20. Correction Rule

If the ITRGA identifies a defect:

```text
ITRGA Finding
      ↓
Correction Required
      ↓
DA Correction
      ↓
Correction Evidence
      ↓
ITRGA Re-review
```

The DA must not silently correct the issue and present the corrected state as though it had always existed.

---

# 21. No Premature Next-Phase Implementation

The DA may recommend the next phase.

The DA may prepare non-implementation planning material if explicitly authorized.

The DA may **not implement the next phase** until:

1. the current phase is reviewed;
2. the ITRGA issues its determination;
3. the next phase is formally authorized;
4. the corresponding Build Order is issued.

Therefore:

```text
P03 implementation
    ↓
P03 Delivery Report
    ↓
ITRGA P03 Review
    ↓
P03 Determination
    ↓
P04 Build Order
    ↓
P04 implementation
```

---

# 22. Chat / Session Continuity Rule

When either the DA or ITRGA changes chat/session, the new authority must be initialized from the authoritative project artifacts.

The Operator must provide:

1. current repository state;
2. current commit/tag;
3. latest PROJECT_STATE;
4. latest governing documents;
5. latest Design Plan;
6. latest Build Order;
7. latest Delivery Report;
8. latest ITRGA Determination;
9. current outstanding observations/corrections.

The new authority must not infer project state from conversation memory.

---

# 23. Continuity Confirmation

Before beginning implementation or review, the authority must explicitly confirm:

```text
BASELINE IDENTIFIED
GOVERNING DOCUMENTS IDENTIFIED
CURRENT PHASE IDENTIFIED
PREVIOUS DETERMINATION IDENTIFIED
ACTIVE BUILD ORDER IDENTIFIED
PROJECT STATE SYNCHRONIZED
SCOPE BOUNDARY UNDERSTOOD
AUTHORITY ROLE CONFIRMED
```

Only after this confirmation may phase work begin.

---

# 24. P03-Specific Mandatory Controls

Before issuing or executing `BUILD_ORDER_UI-008-P03`, the following must be established:

### 24.1 Contextual Assistant Boundary

P03 must explicitly define:

- supported surfaces;
- supported contexts;
- context data allowed into the assistant;
- context data prohibited;
- read-only boundaries;
- authentication requirements;
- refusal behavior.

### 24.2 Architecture

The P03 Build Order must reference the actual P02 architecture rather than assuming the original P02 architecture.

### 24.3 Test Baseline

P03 starts from:

```text
Frontend: 71 suites / 319 tests
Backend: 414 tests
Build: exit 0
D-47: APPROVED
```

unless the repository itself establishes a newer formally verified baseline.

### 24.4 Security

P03 must preserve:

```text
No actuation
No external LLM
Read-only assistant behavior
JWT authentication
401 handling
Refusal taxonomy
Auditability
```

### 24.5 No Retroactive Rework

P03 must not reopen P01/P01-M1/P02 unless a specific defect is discovered and formally documented.

---

# 25. Mandatory Delivery Report Declaration

Every future UI-008 Delivery Report must conclude with:

```text
## Governance Declaration

Historical approved work was preserved.

The implementation was performed only within the authorized phase boundary.

All deviations from the governing Build Order have been explicitly declared.

Test counts distinguish:
- previous baseline;
- tests added;
- tests removed;
- tests modified;
- current total.

Evidence claims are distinguished from assertions.

Project-state artifacts have been synchronized or explicitly marked as unchanged with justification.

No subsequent phase was implemented without authorization.

Production certification status remains unchanged unless separately determined by the appropriate authority.
```

---

# 26. Mandatory ITRGA Review Declaration

Every future UI-008 ITRGA determination must conclude with:

```text
## Independent Review Declaration

The ITRGA independently assessed the submitted evidence.

DA assertions were not treated as verification without supporting evidence.

Scope was compared against the governing Build Order.

Implementation was compared against the approved Design Plan.

Deviations were explicitly assessed.

Test-count deltas were reconciled against the previous verified baseline.

Security boundaries were independently assessed to the extent supported by available evidence.

Production certification was not inferred from phase approval.

The determination applies only to the reviewed phase and does not automatically certify subsequent phases.
```

---

# 27. Governing Principle

The governing principle for UI-008 continuation is:

> **Preserve what has been proven, change only what is authorized, document every deviation, prove every material claim, and never allow implementation to silently redefine governance.**

The objective is not bureaucracy for its own sake.

The objective is to ensure that when UI-008 reaches P06—or any later phase—we can reconstruct the entire engineering and governance chain without relying on memory, interpretation, or chat history.

---

## Status

**This amendment governs UI-008 from P03 forward.**

It does not invalidate:

- D-30;
- D-45;
- D-47;
- approved UI-008 implementation;
- existing commits;
- existing tags;
- historical Delivery Reports.

The next authorized step remains:

**UI-008-P03 Build Order preparation and issuance.**

---

**End of AXIOM — UI-008 Governance Control Amendment**