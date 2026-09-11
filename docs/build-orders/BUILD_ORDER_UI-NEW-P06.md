# BUILD ORDER — UI-NEW-P06
## Whole-Terminal Integration, Visual Audit & Handover

| Field | Value |
|---|---|
| Instrument type | ITRGA Build Order (Directive §§29–31) — **terminal phase of the UI-NEW programme** |
| Issued by | Independent Technical Review & Governance Authority |
| Issued to | AXIOM Development Authority (DA) |
| Date | 2026-08-13 |
| Authorization | Operator, 2026-08-13 ("authorized") |
| Governing plan | `docs/plans/UI-NEW_ENGINEERING_DESIGN_PLAN.md` §V-P06, §N, §W — sha256 `8834aa91…` |
| Preceding determination | `ITRGA_REVIEW_UI-NEW-P05.md` — APPROVED WITH OBSERVATIONS |
| Baseline of record | commit `a44b6a29…` · tag `UI-NEW-P05_DELIVERY` `0a337cc6…` · 158 suites / 686 frontend / 415 backend / **1,101 total** · `index-CVVoXKT4.js` 712.99 kB · Alembic `20260717_0037` |
| Governance Gate | CLOSED · Production NOT CERTIFIED |

---

## 1. Certification preconditions — these are no longer carried conditions

P06 is the handover phase. It is the gateway to `11_PRODUCTION_READINESS_CERTIFICATION.md`, and the standard changes here. Conditions the Operator elected to carry through implementation phases **cannot be carried across the certification boundary.**

**1.1 CA-P03-1 (GA-167) — precondition on P06 delivery approval.**

Origin: `grep -c "GA-167"` = **0**, register head **GA-166**, and no delivery commit from P01–P05 is present. The constitutional record for the Tier-5 displacement of `08_UI_UX_SPEC.md` does not exist in the register after six phases and twelve review cycles.

> **P06 will not be approved, and handover will not be certified, while CA-P03-1 stands.**

This is not a change of position — I stated it in the P05 determination §6. Closure requires the Operator to confirm authorship of GA-167 (or re-make it under Operator hand) and record it. The DA is **not** to create, edit, or transcribe it.

**1.2 The evidence corpus must be readable at origin.**

P05 §10.1 disclosed that **push rights are held by the Operator**. That answer discharged the DA's obligation and I accepted it. It does not discharge the requirement.

A handover package that no third party can inspect is not a handover. Before P06 delivery review: all delivery commits and annotated tags `UI-NEW-P01_DELIVERY` … `UI-NEW-P06_DELIVERY`, the governance register including GA-167…GA-173, and `docs/evidence/uinew/` **must be present at origin**. This is an **Operator action**. If it cannot be performed, the DA states so plainly in §10 and P06 will be determined on that basis.

**1.3 Scope discipline.** P06 is verification and closure. It is **not** a remediation phase. Defects found by the audit are to be *recorded*, not silently fixed — see §5.

---

## 2. Purpose & scope

**IN scope**
1. `terminalWholeSurface.test.tsx` — whole-surface integration harness across P01–P05 panes.
2. Whole-frontend design-token audit (§4).
3. Whole-frontend actuation, LLM, secrets and depth-ladder audit at programme scope (§5).
4. Full route-inventory verification — **17 registered routes** (§6).
5. Final `PROJECT_STATE.md` / `CHANGELOG.md` synchronisation and the `UI-NEW COMPLETE` declaration package.
6. Handover dossier to Production Readiness Certification (§7).

**OUT of scope**
- Any new feature, pane, tab, or surface. P06 adds no capability.
- Any backend endpoint, schema, migration, or dependency. Alembic head stays `20260717_0037`.
- Remediation of defects the audit discovers, unless they are P06 regressions (§5).
- Production certification itself — P06 hands over *to* that process; it does not perform it.
- Retiring `/charts`; re-opening any closed P01–P05 determination.

---

## 3. 🔴 B-P06-1 — Whole-surface integration must exercise the real composition

`terminalWholeSurface.test.tsx` must verify the terminal as an assembled system, not five components in isolation:

- All five zones mount together without DOM collision: ticker header (P01), watchlist dock (P02), chart stage (P03), right dock (P04), bottom dock (P05).
- Symbol selection in the watchlist propagates to chart, telemetry, signal stream and risk panel through `TerminalContext`.
- Timeframe change propagates without unmounting sibling panes.
- Right-dock tab switching (`SIGNALS` / `TELEMETRY` / `INTELLIGENCE`) and bottom-dock tab switching (four tabs) do not disturb one another or the chart.
- Governance chips — `GATE CLOSED`, `RESEARCH-ONLY`, `NON-ACTUATING` — are present in the assembled surface, not only in unit scope.

## 4. 🔴 B-P06-2 — The token audit has a known answer; report it honestly

Plan §V-P06 requires *"0 ad-hoc hex outside `tokens.css`."* I ran that audit against the P05 baseline. **Two files carry ad-hoc hex:**

```
frontend/src/styles/global.css          15 occurrences
frontend/src/components/chart/PriceChart.tsx   7 occurrences
```

I am giving the DA this result deliberately, so the audit is a reconciliation rather than a discovery.

**`global.css` is the substantive finding.** It defines a **parallel token system** — `--bg-root: #0b0e11`, `--bg-panel`, `--bg-hover`, `--border`, `--border-strong` — separate from `workstation/design/tokens.css` and its `--ix-*` namespace. Two coexisting token vocabularies is the same class of issue as the two chart surfaces in P03, and it bears directly on `TD-005` *"Handcrafted CSS / no design tokens."*

**Required:**
- Run the audit at whole-frontend scope and publish the **raw transcript**, including these two files. An audit reporting `0 matches` at programme scope will be treated as incorrectly scoped (the CA-P03-4 precedent).
- State plainly whether `global.css` is (a) legacy to be retired, (b) the base layer that `--ix-*` builds on, or (c) unresolved duplication.
- **Do not remediate either file in P06.** Record the disposition and, if unresolved, raise a technical-debt entry. `PriceChart.tsx` was reported cured in P04 §7 — if hex persists there, that is a **reconciliation discrepancy** and must be reported as such, not quietly fixed.

## 5. 🔴 B-P06-3 — Programme-scope safety audit; record, do not repair

Re-run at **whole-frontend scope**, not `components/terminal/` alone:

| Audit | Scope | Expected |
|---|---|---|
| T-1 actuation (`buy`, `sell`, `place_order`, `execute`, `broker`, `account_id`, `position`, `balance`, `margin`) | all of `frontend/src` | 0 functional |
| T-4 / T-5 external LLM | all of `frontend/src` + `package.json` | 0 |
| C-1 order book / depth ladder | all of `frontend/src` | 0 |
| T-7 / S-5 secrets | all of `frontend/src` | 0 |
| S-3 `dangerouslySetInnerHTML` / `eval` / `new Function` | all of `frontend/src` | 0 |
| B-P06-2 ad-hoc hex | all of `frontend/src` except `tokens.css` | **2 files, per §4** |

Publish raw transcripts. Where a hit is a false positive (e.g. `position` in a CSS property), show the line and say so — do not filter silently.

**If the audit finds a genuine defect in P01–P05 code, record it as a finding for a remediation Build Order.** The DA must not repair it inside P06. Correcting a P05 defect during a P06 audit destroys the independence of both.

## 6. 🔴 B-P06-4 — Route inventory: verify the real count

P04/P05 reports tabulate **16 routes**. The registry contains **17 `route:` entries**. That discrepancy may be benign — an alias, a redirect, an index — but it has been carried unexamined for two phases.

Enumerate every registered route from `workspaceRegistry.tsx`, confirm each mounts and is auth-guarded, and **reconcile the count explicitly**. If the true number is 17, correct the table and say what the seventeenth is.

## 7. 🔴 B-P06-5 — The handover dossier must be self-contained and honest

The dossier hands the programme to Production Readiness Certification. It must state:

- **Every open technical debt item** carried into certification, verbatim with correct line numbers — including `TD-005`, `TD-021`, `TD-028`, `TD-029`, `TD-UI-REACTROUTER-MODERATE`, and `TD-AXIOM-DEV-CREDENTIAL-LITERALS` (the Doc 11 §2 pre-certification blocker).
- **Every observation carried from P01–P05 determinations** that remains open, including OBS-P06-1/-2/-3 and any `global.css` disposition from §4.
- The **complete determination chain** P01→P06 with ITRGA document hashes.
- An explicit statement that the Governance Gate is **CLOSED**, production is **NOT CERTIFIED**, and no phase determination constituted certification.
- The **CA-P03-1 status** as of handover, stated plainly whatever it is.

The dossier must not claim certification readiness. It declares `UI-NEW COMPLETE` and hands over; the certification judgement belongs to Doc 11.

## 8. Conditions carried

| ID | Condition | Status in P06 |
|---|---|---|
| CA-P03-1 | GA-167 unrecorded | **Certification precondition** (§1.1) — Operator |
| OBS-P06-1 | Corpus not at origin | **Precondition for delivery review** (§1.2) — Operator |
| OBS-P06-2 | `DISCHARGED / ESCALATED` vocabulary | Use `DA-DISCHARGED / OPERATOR-OPEN` |
| OBS-P06-3 | Surface `updated_at`, not only `[EDITED]` | Recommended, not required |
| OBS-5 | Cumulative bundle +62.97 kB across P01–P05 | Include a bundle review in the audit |
| C-1 / T-1 / T-3 / T-4 / T-5 | Permanent exclusions | Absolute |

## 9. Mandatory named tests

Six tests, displayed **passing by name** under the Vitest verbose reporter, in `terminalWholeSurface.test.tsx`:

1. `test_uinew_p06_all_five_terminal_zones_mount_together_without_dom_collision`
2. `test_uinew_p06_symbol_selection_propagates_to_chart_telemetry_signals_and_risk`
3. `test_uinew_p06_dock_tab_switching_does_not_unmount_or_disturb_sibling_panes`
4. `test_uinew_p06_governance_chips_render_in_assembled_surface_not_only_in_units`
5. `test_uinew_p06_whole_frontend_contains_zero_actuation_llm_orderbook_or_secret_affordance`
6. `test_uinew_p06_every_rendered_statistical_value_carries_uncertainty_or_explicit_unavailable`

Test 6 is the programme-level generalisation of CA-P04-5 and B-P05-2: it must span P04 signal cards **and** P05 risk metrics **and** scenario figures.

Plus `uinew_p06_security_invariants.test.ts` at programme scope.

## 10. Mandatory evidence

(a) Delivery commit + annotated tag `UI-NEW-P06_DELIVERY`, `git rev-parse` output, **present at origin** (§1.2).
(b) SHA-256 for every created and modified file. No placeholders.
(c) Full suite counts against the delivered commit, fresh transcript. Bundle hash must differ from `index-CVVoXKT4.js` / 712.99 kB if any frontend source changed. Named tests claimed must appear in the transcript.
(d) **Raw** audit transcripts per §5, whole-frontend scope, including the two expected hex files.
(e) Field-provenance table consolidated across P01–P06.
(f) **Level-I captures at 1920×1080, attached as image files**: (i) whole assembled terminal, all five zones populated; (ii) symbol switched to a second instrument, showing propagation; (iii) bottom dock on a tab other than the default with the chart intact; (iv) logged-out redirect; (v) any surface showing a governance chip set at full-bleed width.
(g) Deviation register — if zero, state zero and mean it.
(h) Technical debt reconciliation, verbatim, correct line numbers.
(i) The §7 handover dossier.

## 11. Acceptance criteria

P06 is approvable when: B-P06-1…B-P06-5 are satisfied; the six named tests display passing; the 1,101-test baseline is maintained or grown with zero regression; `tsc -b` and `vite build` exit 0 against the delivered commit; Alembic head unchanged; evidence (a)–(i) complete; the corpus is readable at origin; **and CA-P03-1 is closed.**

Plan §V-P06 sets the programme bar: *"100% regression test pass, 0 ad-hoc hex literals, 0 actuation, and successful handover."* Note the DA cannot report zero ad-hoc hex honestly today — §4 governs. **An honest non-zero finding with a recorded disposition satisfies this Build Order; a zero achieved by narrow scoping does not.**

## 12. Authorization

The DA is authorized to implement UI-NEW-P06 as scoped above, effective immediately.

This Build Order is not an approval of any future delivery, and approval of P06 is **not** production certification — it is handover to the certification process under `11_PRODUCTION_READINESS_CERTIFICATION.md`. Correction is not approval. The DA may not self-approve. The Governance Gate remains **CLOSED**.

**We don't guess. We prove.**

*— AXIOM ITRGA*
