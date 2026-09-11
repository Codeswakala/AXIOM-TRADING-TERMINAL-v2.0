# DELIVERY REPORT — UI-001-P06 TERMINALLAYOUT RETIREMENT FIX

## Trigger

The operator reported that the P06 retirement error persists:

```text
test_terminal_layout_retired_shell_is_sole_frame
expect(sourceText).not.toContain("TerminalLayout")
```

## Diagnosis

This failure means the target operator environment still contains a production source reference to:

```text
TerminalLayout
```

In the P06 context, the expected cause is the stale legacy file:

```text
frontend\src\layouts\TerminalLayout.tsx
```

In the DA workspace, the file is absent and the only remaining string is in the test assertion itself. The target machine therefore needs the explicit retirement/removal step before rerunning evidence.

## Corrective action prepared

Updated:

```text
docs/evidence/UI-001-P06_CA_CORRECTION_COMMANDS.md
```

Created:

```text
docs/evidence/UI-001-P06_TERMINAL_LAYOUT_RETIREMENT_FIX_COMMANDS.md
DELIVERY_REPORT_UI-001-P06_TERMINAL_LAYOUT_FIX.md
```

The fix commands explicitly remove the stale file and prove no production source reference remains.

## Expected closure

```text
TERMINAL_LAYOUT_FILE_EXISTS_AFTER_REMOVE: False
production source grep for TerminalLayout -> no output
test_terminal_layout_retired_shell_is_sole_frame -> PASS
```

## Governance disposition

UI-001-P06 remains not approved until corrected operator evidence is submitted and accepted by ITRGA. DA does not self-approve P06 and does not authorize UI-002.

---

**End of report**
