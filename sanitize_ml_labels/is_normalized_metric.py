from typing import Dict
import os
import compress_json
from .sanitize_ml_labels import sanitize_ml_labels


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
    sanitized_metric = sanitize_ml_labels(metric)
    return any(
        candidate in sanitized_metric
        for candidate in compress_json.local_load("normalized_metrics.json")
    )


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
    sanitized_metric = sanitize_ml_labels(metric)
    return any(
        candidate in sanitized_metric
        for candidate in compress_json.local_load("absolutely_normalized_metrics.json")
    )
