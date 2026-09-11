"""V2 BE-3 P2 credential boundary — the SOLE secret-resolution module.

BO-V2-BE-3-P2-001 §3.1. No other module may import the backends defined here
(import-boundary test enforced). The resolved value:

- never enters module/global state;
- is never serialized, repr'd, logged, audited, or returned by any API;
- is held only inside the request-scoped runner call chain;
- is explicitly ABSENT for placeholder/empty values.

Documented mechanism (no secret value anywhere in workspace configuration):
- environment variable: ``AXIOM_TD_API_KEY`` (Operator environment only);
- file mount: path named by ``AXIOM_TD_API_KEY_FILE`` (container/CI style).

Default for every non-P2 path and all test runs remains the P1
``FixtureCredentialResolver`` (always absent, never reads the environment).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

#: Placeholder values that must NEVER be treated as a real secret.
_PLACEHOLDER_VALUES = frozenset(
    {"", "TD_TEST_KEY_PLACEHOLDER", "changeme", "placeholder", "none", "null"}
)

_ENV_VAR = "AXIOM_TD_API_KEY"
_ENV_FILE_VAR = "AXIOM_TD_API_KEY_FILE"


@dataclass(frozen=True, slots=True)
class ResolvedCredential:
    """Explicit credential state. ``value`` is intentionally excluded from
    repr/str so it can never leak through logging or error rendering."""

    state: str  # "present" | "absent"
    value: str | None = field(default=None, repr=False)

    def __str__(self) -> str:  # defence in depth — never render the value
        return f"ResolvedCredential(state={self.state})"


ABSENT = ResolvedCredential(state="absent")


class SecretBackend(Protocol):
    def resolve(self) -> ResolvedCredential: ...


class EnvSecretBackend:
    """Reads AXIOM_TD_API_KEY once per call; placeholder/empty → ABSENT."""

    def resolve(self) -> ResolvedCredential:
        raw = os.environ.get(_ENV_VAR)
        if raw is None or raw.strip() in _PLACEHOLDER_VALUES:
            return ABSENT
        return ResolvedCredential(state="present", value=raw.strip())


class FileSecretBackend:
    """Reads the file named by AXIOM_TD_API_KEY_FILE; missing/placeholder → ABSENT."""

    def resolve(self) -> ResolvedCredential:
        path_raw = os.environ.get(_ENV_FILE_VAR)
        if not path_raw:
            return ABSENT
        path = Path(path_raw)
        if not path.is_file():
            return ABSENT
        raw = path.read_text().strip()
        if raw in _PLACEHOLDER_VALUES:
            return ABSENT
        return ResolvedCredential(state="present", value=raw)


def resolve_contract_test_credential() -> ResolvedCredential:
    """P2 chain: env → file → ABSENT. Called ONLY by the contract-test
    runner inside the authenticated endpoint dependency chain."""
    for backend in (EnvSecretBackend(), FileSecretBackend()):
        resolved = backend.resolve()
        if resolved.state == "present":
            return resolved
    return ABSENT
