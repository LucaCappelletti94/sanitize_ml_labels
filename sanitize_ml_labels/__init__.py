"""Module providing tools to standardize metric names and display ranges."""

from sanitize_ml_labels.sanitize_ml_labels import sanitize_ml_labels
from sanitize_ml_labels.is_normalized_metric import (
    is_normalized_metric,
    is_absolutely_normalized_metric,
)
from sanitize_ml_labels.should_be_maximized import should_be_maximized


__all__ = [
    "sanitize_ml_labels",
    "is_normalized_metric",
    "is_absolutely_normalized_metric",
    "should_be_maximized",
]
