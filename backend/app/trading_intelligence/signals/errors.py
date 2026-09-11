"""Advisory signal service errors (W3-U02)."""

from __future__ import annotations


class AdvisorySignalError(ValueError):
    """Base advisory signal error."""


class AdvisorySignalStateError(AdvisorySignalError):
    """Raised when a signal state transition contract is violated."""
