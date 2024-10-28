"""Check if a metric is known to be between 0 and 1 or -1 and 1."""

from typing import cast
import compress_json
from sanitize_ml_labels.sanitize_ml_labels import sanitize_ml_labels


def check_in_set(metric: str, set_name: str) -> bool:
    """Check if a metric is in a given set.

    Parameters
    ----------
    metric:str
        The metric to check for
    set_name:str
        The set to check in

    Returns
    -------
    Boolean representing if given metric is in the given set.
    """
    sanitized_metric: str = cast(str, sanitize_ml_labels(metric)).lower()
    return any(
        candidate in sanitized_metric
        for candidate in compress_json.local_load(f"{set_name}.json")
    )


def is_normalized_metric(metric: str) -> bool:
    """Return boolean representing if given metric is known to be between 0 and 1.

    Parameters
    ----------
    metric:str
        The metric to check for

    Returns
    -------
    Boolean representing if given metric is known to be between 0 and 1.
    """
    return check_in_set(metric, "normalized_metrics")


def is_absolutely_normalized_metric(metric: str) -> bool:
    """Return boolean representing if given metric is known to be between -1 and 1.

    Parameters
    ----------
    metric:str
        The metric to check for

    Returns
    -------
    Boolean representing if given metric is known to be between -1 and 1.
    """
    return check_in_set(metric, "absolutely_normalized_metrics")
