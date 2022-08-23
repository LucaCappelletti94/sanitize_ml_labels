"""Module providing tools to standardize metric names and display ranges."""
from support_developer import support_luca
from .sanitize_ml_labels import sanitize_ml_labels
from .is_normalized_metric import is_normalized_metric, is_absolutely_normalized_metric

support_luca("sanitize_ml_labels")

__all__ = [
    "sanitize_ml_labels",
    "is_normalized_metric",
    "is_absolutely_normalized_metric"
]
