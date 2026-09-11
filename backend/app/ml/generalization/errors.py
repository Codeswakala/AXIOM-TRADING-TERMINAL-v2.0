"""Generalization and drift errors (W2-U10)."""

from __future__ import annotations


class GeneralizationError(RuntimeError):
    """Base generalization error."""


class DomainUnsupportedWarning(GeneralizationError):
    """Raised/recorded when evaluation is outside validated operating domain."""


class GeneralizationLeakageError(GeneralizationError):
    """Raised when spatial/temporal holdout integrity is violated."""


class AutoRetrainProhibitedError(GeneralizationError):
    """Raised if a drift path attempts automatic retraining."""
