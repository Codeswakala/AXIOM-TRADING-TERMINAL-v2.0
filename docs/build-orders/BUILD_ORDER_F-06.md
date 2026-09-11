# AXIOM — BUILD ORDER F-06
## Accessibility, Performance & Navigation Legibility (final frontend unit)

| Item | Value |
|------|-------|
| Build Order ID | `BO-F-06` |
| Programme | Frontend Operationalization (Visual Blueprint approved) |
| Authorizing authority | **Operator** (directive 2026-08-22: "authorized") |
| Predecessors | F-05 CLOSED · Blueprint §8 Addendum (navigation legibility — Operator requirement) |
| Governing documents | `VISUAL_BLUEPRINT.md` (incl. §8 Addendum) · `08_UI_UX_SPEC.md` §Accessibility · Reconciliation §33 (performance evidence) · Doc 16 (brand) |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and framing

This is the **final frontend unit**. It closes three named gaps:

1. **Navigation legibility (Operator requirement, Blueprint §8 Addendum).** Verified in code: the collapsed `UnifiedModuleRail` renders **only** a cryptic Unicode glyph (`● ◌ ⌁ ◇ ▦ ◆ ◎ ⇄ ✎ ▣ ▤ ☷ ▧ ◈ ⚙`) per workspace, with the label hidden behind `title`/`aria-label`. An operator cannot tell what each item does without hovering. The prototype ideology requires **self-explanatory navigation**.

2. **Accessibility** — the infrastructure exists (`SkipLink`, `RouteAnnouncer`, `focusTrap`, `useKeyboardShortcuts`, `highContrast`, `responsiveReflow`, an `accessibilityAudit.test`); this unit completes the audit and fixes any remaining gaps.

3. **Performance** — the §33 "performance is NOT PROVEN" finding from the very first capability audit remains: there are no **measured** latency numbers. This unit establishes and measures them.

---

## 1. Objective

1. Make navigation self-explanatory (meaningful icons + visible labels).
2. Complete the accessibility audit and fix remaining gaps.
3. Establish and hit measurable performance thresholds.

---

## 2. Scope

### F-06.1 — Navigation legibility (binding, Operator)
- Replace the cryptic Unicode glyphs (`● ◌ ⌁ …`) with **meaningful, self-explanatory icons** (a small, curated inline-SVG set — no new dependency, per Doc 09 §12; consistent with the F-00 design language and all six themes).
- The **collapsed rail** must no longer be icon-only-with-hidden-label: either (a) show a **visible text label** alongside/under each icon, or (b) ensure the meaningful icon is sufficient on its own **and** the label is shown on hover/expanded. The choice is stated and must result in at-a-glance navigability.
- Every nav item retains its `aria-label`/`title` (screen-reader correctness is not enough — **visible** legibility is the requirement).
- This is both usability and accessibility: the glyphs are not self-describing.

### F-06.2 — Accessibility completion
- Run/extend the `accessibilityAudit` across the six themes: contrast, focus visibility, keyboard navigation, reduced-motion, screen-reader semantics, landmark structure.
- Fix any remaining WCAG AA violations (AAA in High-Contrast). State what was found and fixed.

### F-06.3 — Performance measurement
- Establish **measured** interaction-latency numbers for the thresholds named in the Frontend Roadmap v2 §F-06: command-palette response, workspace switching, instrument selection, chart first render, live-update propagation.
- Report measured values against the stated targets (≤100ms / ≤300ms / ≤200ms / ≤1s / ≤500ms respectively, or the DA's proposed-and-justified values).
- If a target is missed, report it honestly as a named gap, not silently passed.

### F-06.4 — Honesty + non-actuation
- No fabricated measurements; no weakening of any prior invariant (non-actuation, themes, accessibility).
- No new runtime dependency for icons (inline SVG or existing assets only).

---

## 3. Exclusions (out of scope — do NOT do)

- **No** backend change (frontend-only).
- **No** new runtime dependency (icons are inline SVG / existing assets).
- **No** redesign of the shell structure (icons/labels only; no re-architecture).
- **No** weakening of themes, accessibility, or non-actuation.
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. Meaningful icon set + visible-label navigation (both dock and rail).
2. Completed accessibility audit + fixes (per theme).
3. Measured performance numbers vs. stated thresholds.
4. Tests (new/churn): icon-meaningfulness, visible-label presence, accessibility audit, performance measurement harness.
5. Delivery Report (§9) with relay-accurate manifest + register-in-patch rows.

---

## 5. Dependencies

- **Upstream:** F-00 → F-05 (all prior frontend) · the existing accessibility infrastructure · the Blueprint §8 Addendum.
- **Downstream:** X-01 Terminal Tier (the end-to-end verification).

---

## 6. Allowed files / components

- `frontend/src/workstation/registry/workspaceRegistry.tsx` (icon values).
- `frontend/src/workstation/navigation/NavigationDock.tsx`, `UnifiedModuleRail.tsx` (+ `.css`).
- A new icon module (e.g. `frontend/src/workstation/navigation/icons.tsx`) if an inline-SVG set is introduced.
- `frontend/src/workstation/accessibility/**` (audit + fixes).
- `frontend/src/test/**` + relevant `*.test.tsx` (new/churn).
- `docs/governance/TECHNICAL_DEBT_REGISTER.md` (register-in-patch — **required**).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- No new runtime dependency; no fabricated measurements; no weakened invariants.
- Icons must be consistent with the six-theme system (token-driven, not hardcoded colors).
- Accessibility and non-actuation preserved.

---

## 8. Acceptance criteria

- [ ] Nav icons are meaningful (not cryptic glyphs), and every nav item has a visible label (or an explicitly-justified hover/expanded label) — test-pinned.
- [ ] Collapsed rail is navigable at a glance (test-pinned: no icon-only-with-hidden-label).
- [ ] Accessibility audit passes across the six themes; remaining WCAG AA gaps fixed (test-pinned).
- [ ] Measured performance numbers reported vs. stated thresholds; any miss named as a gap.
- [ ] No new dependency; themes/accessibility/non-actuation intact (test-pinned).
- [ ] Register rows ship in the patch (register-in-patch).
- [ ] Full frontend suite green (`npm test`) + typecheck green (`tsc -b`); executed output supplied.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1 + register-in-patch)

**Binding:** CA-TRANSMIT-1 (relay-accurate manifest) + register-in-patch.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed frontend test output + typecheck | Level II | run transcript |
| Screenshot captures (navigation with meaningful icons + labels; per-theme accessibility) | Level I | images |
| Performance measurement report (measured numbers vs. targets) | Level II | report + raw numbers |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Navigation-legibility description (icon set + label strategy)
4. Accessibility audit results + fixes (per theme)
5. Performance measurement (measured vs. target, per interaction)
6. Screenshot evidence
7. Test evidence (executed)
8. Deviations register
9. Register rows in patch (confirmed) + transmission manifest (relay-accurate)

---

## 11. Rollback / containment

- Frontend-only; revert = revert patch. No backend change, no schema change, no new dependency.

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified, the Delivery Report submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of F-06, the **frontend roadmap is complete**, and the **X-01 Terminal Tier** (full UI end-to-end verification) may be issued — the milestone the Operator set as the gate for resuming predictive trials.

---

**End of Build Order F-06**
