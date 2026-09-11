# BUILD ORDER — TD-UI-POSTCSS-HIGH DEPENDENCY REMEDIATION

**Dedicated dependency-remediation Build Order — the ONLY authorized dependency change in the UI programme to date**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Track | Cross-cutting security residual remediation (feeds Production Readiness Certification, Doc 11) |
| Residual | **TD-UI-POSTCSS-HIGH** — `postcss <=8.5.17` (GHSA-r28c-9q8g-f849), high severity |
| Provenance | Disclosed UI-004-P06; Path-B re-accepted UI-005/UI-006 completions; hardened to **non-waivable pre-certification blocker** at UI-006-P06; scheduling condition R-5 (UI-007 design-plan review) = **before UI-007-P02** |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **55f/246t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Remediate the standing high-severity transitive advisory **`postcss <=8.5.17` (GHSA-r28c-9q8g-f849)** so it no longer blocks Production Readiness Certification. This is a **narrowly-scoped, authorized dependency change** — the first sanctioned manifest change of the UI programme. **This Build Order MUST precede UI-007-P02** (which renders certification status; it is incoherent to display a "non-waivable pre-cert blocker" while it remains unaddressed).

**IN scope:**
1. Bump `postcss` (and any transitive parents that pin it) to a fixed version `> 8.5.17` that clears GHSA-r28c-9q8g-f849 — via `npm audit fix` (non-forced) or a targeted dependency bump / `overrides`, whichever is minimal.
2. `package.json` / `package-lock.json` manifest update (the authorized change), plus the moderate `react-router`/`react-router-dom` advisories **only if** the fix is non-breaking and in the same minor line (otherwise disclose and leave as tracked moderates — they are not the blocker).

**OUT of scope (do NOT build):**
- Any application feature / UI change / new capability — this is a dependency bump only.
- Any backend / schema / migration change; alembic stays `20260717_0037`.
- Any forced major upgrade that breaks the build/tests (if `postcss` clears only via a breaking change, STOP and return to ITRGA with the constraint — do not force it).
- `strict-ssl false` or any audit-suppression trick (constitutionally prohibited).
- Relabeling audit output green without a real fix.

---

## 2. Mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL creds as standard.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF the TD-UI-POSTCSS-HIGH remediation.
- (b) **Manifest diff** — the exact `package.json` / `package-lock.json` change (before → after `postcss` version; any `overrides` added), displayed inline. This is the authorized change; nothing else in the manifests should move beyond what the fix requires.
- (c) **🔴 Networked `npm audit --audit-level=high` → exit 0** with the report body showing **postcss no longer listed as high** (`0 high/critical`; any residual moderates disclosed). This is the core proof — it MUST be a networked run that reached the registry (not an ENOTFOUND/ECONNRESET flake).
- (d) **Targeted before/after** — `npm ls postcss` (or lockfile grep) showing the resolved version moved from `<=8.5.17` to the fixed version.
- (e) **No functional regression** — frontend Vitest **≥55f/246t** all passing (no test lost); TypeScript clean; **production build successful** (postcss underlies the CSS/build pipeline, so the build passing is essential); bundle delta noted.
- (f) **Backend unaffected** — `pytest -q` **≥414 passed** (backend does not consume postcss, but confirm no incidental breakage).
- (g) **No-drift (non-dependency)** — `alembic current` = `20260717_0037`; no backend/schema/migration change; no registry/route change; no new endpoint. (The dependency manifest IS expected to change here — that is the authorized delta; everything else stays put.)
- (h) **Constitutional unchanged** — no actuation/Gate/execution/AI introduced by the bump (no-actuation grep clean); Gate CLOSED.
- (i) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel — this remediation is precisely what makes a green CI audit gate achievable; a networked exit-0 CI is the expected happy path. If the machine is genuinely offline (ENOTFOUND/ECONNRESET) the audit cannot be verified — in that case this Build Order is **incomplete** and must be re-run networked (the whole point is the networked audit-high exit 0).

---

## 3. Determination rule

**Approved** requires: (b) manifest diff shown; (c) **networked `npm audit --audit-level=high` exit 0 with postcss no longer high**; (d) resolved-version before/after; (e) frontend ≥55f/246t + tsc clean + build successful; (f) backend ≥414; (g) no non-dependency drift (alembic head, no schema/route/endpoint change); (h) constitutional unchanged. On Approved, ITRGA **closes TD-UI-POSTCSS-HIGH** and removes it from the residual register (Production Readiness Certification is no longer blocked by it).

A forced/breaking upgrade that red-gates the suite, an offline/flaked audit that cannot prove exit 0, any `strict-ssl false`/suppression, or relabeling without a real fix ⇒ Corrective / Rejected. If `postcss` cannot be cleared without a breaking change, STOP and return to ITRGA with the dependency constraint for a scoped decision.

**Sequencing:** This Build Order MUST be delivered and Approved **before `BUILD_ORDER_UI-007-P02`** (R-5). UI-007-P01 (read-only frame) may proceed in parallel since it introduces no dependency change.

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED (until the full Doc 11 track runs; this BO only clears one pre-cert blocker).**

**We don't guess. We prove.**

*— AXIOM ITRGA*
