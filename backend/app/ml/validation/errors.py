"""Statistical validation errors (W2-U07)."""

from __future__ import annotations


class StatisticalValidationError(RuntimeError):
    """Base validation error."""


class NonTemporalValidationError(StatisticalValidationError):
    """Raised when validation config requests random/non-temporal CV."""


class EmbargoViolationError(StatisticalValidationError):
    """Raised when validation folds violate embargo/purge gap."""


class MissingUncertaintyError(StatisticalValidationError):
    """Raised when a validation report lacks uncertainty fields."""


class ValidationPinError(StatisticalValidationError):
    """Raised when model/experiment pins do not resolve."""
