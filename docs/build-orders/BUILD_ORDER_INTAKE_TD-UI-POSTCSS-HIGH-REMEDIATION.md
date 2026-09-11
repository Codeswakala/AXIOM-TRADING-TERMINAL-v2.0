# BUILD ORDER INTAKE — TD-UI-POSTCSS-HIGH REMEDIATION

**Dedicated dependency-remediation Build Order**

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Track | Cross-cutting security residual remediation |
| Residual | **TD-UI-POSTCSS-HIGH** — `postcss <=8.5.17` / GHSA-r28c-9q8g-f849 |
| Build Order | `docs/build-orders/BUILD_ORDER_TD-UI-POSTCSS-HIGH-REMEDIATION.md` |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 55 files / 246 tests |
| Intake status | Accepted by DA under ITRGA Build Order; dependency change confined to the authorized PostCSS remediation |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

ITRGA issued a dedicated dependency-remediation Build Order for `TD-UI-POSTCSS-HIGH`. This is the only dependency change authorized in the current UI programme and must be handled separately from UI-007 feature work.

Recorded governance file:

```text
docs/build-orders/BUILD_ORDER_TD-UI-POSTCSS-HIGH-REMEDIATION.md
```

---

## 2. Accepted scope

DA accepts a narrow dependency remediation only:

```text
clear postcss <=8.5.17 high advisory
manifest/lockfile change only as required by the fix
networked npm audit --audit-level=high exit 0 evidence
full frontend/backend regression
no backend/schema/route/feature/Gate change
```

---

## 3. Explicit non-authorizations

This Build Order does not authorize:

- UI/application feature changes;
- backend/API endpoint changes;
- schema migration or table changes;
- forced/breaking major upgrade if tests/build red-gate;
- audit suppression or `strict-ssl false`;
- relabeling audit output green without a real fix;
- Governance Gate change;
- production certification.

---

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
