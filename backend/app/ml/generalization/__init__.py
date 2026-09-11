"""Generalization, model registry maturation, and drift design (W2-U10)."""

from app.ml.generalization.errors import (
    AutoRetrainProhibitedError,
    DomainUnsupportedWarning,
    GeneralizationError,
    GeneralizationLeakageError,
)
from app.ml.generalization.service import Domain, GeneralizationInput, GeneralizationService

__all__ = [
    "AutoRetrainProhibitedError",
    "Domain",
    "DomainUnsupportedWarning",
    "GeneralizationError",
    "GeneralizationInput",
    "GeneralizationLeakageError",
    "GeneralizationService",
]
