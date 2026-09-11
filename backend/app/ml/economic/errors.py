"""Economic validation errors (W2-U09)."""

from __future__ import annotations


class EconomicValidationError(RuntimeError):
    """Base economic validation error."""


class CostInputInvalidError(EconomicValidationError):
    """Raised when cost inputs lack provenance or sensitivity."""


class EconomicReportInvalidError(EconomicValidationError):
    """Raised when economic/statistical conclusions are conflated or incomplete."""


class EconomicPinError(EconomicValidationError):
    """Raised when experiment/model/report pins do not resolve."""
