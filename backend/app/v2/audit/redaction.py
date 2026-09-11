"""V2 Audit Redaction — sensitive field redaction before storage.

Per 17_INSTITUTIONAL_SECURITY_STANDARD.md:
- JWT tokens → [REDACTED]
- Passwords → [REDACTED]
- API keys → [REDACTED]
- DB connection strings → [REDACTED]
- Broker credentials → [REDACTED]
"""

from __future__ import annotations

import re
from typing import Any

# Sensitive patterns to redact
SENSITIVE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    # Bearer tokens
    (
        re.compile(r"(?i)(authorization\s*[:=]\s*bearer\s+)[A-Za-z0-9._~+/=-]+"),
        r"\1[REDACTED]",
    ),
    (re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]+"), r"\1[REDACTED]"),
    # Passwords
    (
        re.compile(r"(?i)(password\s*[:=]\s*)([^\s,;}&]+)"),
        r"\1[REDACTED]",
    ),
    # Tokens
    (
        re.compile(
            r"(?i)(refresh_token|access_token|token|ticket)(\s*[:=]\s*)([^\s,;}&]+)"
        ),
        r"\1\2[REDACTED]",
    ),
    # Database connection strings
    (
        re.compile(r"(?i)(postgresql(?:\+asyncpg)?://[^:\s/@]+:)([^@\s]+)(@)"),
        r"\1[REDACTED]\3",
    ),
    # API keys (generic pattern)
    (
        re.compile(r"(?i)(api[_-]?key\s*[:=]\s*)([^\s,;}&]+)"),
        r"\1[REDACTED]",
    ),
    # Broker credentials
    (
        re.compile(r"(?i)(broker[_-]?(?:key|secret|password|token)\s*[:=]\s*)([^\s,;}&]+)"),
        r"\1[REDACTED]",
    ),
    # Provider API keys — Twelve Data query-parameter form (BE-3 P1 defensive
    # pattern; no key exists in P1, added so any future accidental echo is
    # redacted before storage)
    (
        re.compile(r"(?i)(apikey\s*[:=]\s*)([^\s,;}&]+)"),
        r"\1[REDACTED]",
    ),
)


def redact(value: Any) -> Any:
    """Redact secrets from strings and recursively from simple containers."""
    if value is None:
        return None
    if isinstance(value, str):
        redacted = value
        for pattern, replacement in SENSITIVE_PATTERNS:
            redacted = pattern.sub(replacement, redacted)
        return redacted
    if isinstance(value, dict):
        return {str(k): redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, tuple):
        return tuple(redact(v) for v in value)
    return value


def has_sensitive_content(value: str) -> bool:
    """Check if a string contains sensitive content that should be redacted."""
    for pattern, _ in SENSITIVE_PATTERNS:
        if pattern.search(value):
            return True
    return False
