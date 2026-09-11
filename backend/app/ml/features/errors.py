"""Feature framework errors (W2-U03)."""

from __future__ import annotations


class FeatureFrameworkError(RuntimeError):
    """Base feature framework error."""


class DuplicateFeatureDefinitionError(FeatureFrameworkError):
    """Raised when feature definition uniqueness is violated."""


class NonCausalFeatureError(FeatureFrameworkError):
    """Raised when a feature definition attempts look-ahead/peeking."""


class FeatureInputRejectedError(FeatureFrameworkError):
    """Raised when chronology guard rejects feature inputs."""
