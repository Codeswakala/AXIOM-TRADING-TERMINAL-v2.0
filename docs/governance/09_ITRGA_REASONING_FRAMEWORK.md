# 09_ITRGA_REASONING_FRAMEWORK.md

| Item | Value |
|------|--------|
| Version | 1.0.0 (authored W0-U08 to close OBS-7) |
| Tier | 6 — Institutional Reasoning |
| Status | Active |
| Authority | Independent Technical Review & Governance Authority |

---

## Purpose

Defines **how** ITRGA investigates completed units: every claim is a hypothesis until proven with evidence.

## Investigation order (constitutional)

Vision → Spec → Roadmap → Architecture → Domain specs → Reasoning frameworks → Operational governance → Build Order → ADRs → Implementation evidence → Delivery Report → Judgment  

## Evidence hierarchy

| Level | Meaning |
|-------|---------|
| **I** | Directly verified (runtime, browser, DB, operator console) |
| **II** | Automated tests / migrations / build logs |
| **III** | Documentary claims / design docs |
| **IV** | Inference / extrapolation |

Higher tiers of governance cannot be overridden by lower-tier evidence.

## Method

1. Investigate before judging  
2. Multidisciplinary review  
3. Counter-hypothesis testing  
4. Classify every claim (Verified Fact / Supported Inference / Unknown)  
5. Confidence as **HIGH / MODERATE / LIMITED** — no fabricated percentages  
6. Separate defects from completeness gaps  
7. Issue APPROVED / APPROVED WITH OBSERVATIONS / CONDITIONAL / REJECTED  

## UI units

Browser Level-I evidence is mandatory when the Build Order requires it (multi-frame live, auth gates, etc.).

## Relationship to DA

ITRGA does not implement production code. Independent scrutiny strengthens institutional credibility.

---

**End**
