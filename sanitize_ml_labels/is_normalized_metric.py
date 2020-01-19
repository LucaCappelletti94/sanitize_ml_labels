from typing import Dict
import os
import json
from .sanitize_ml_labels import sanitize_ml_labels


def load_normalized_metrics() -> Dict[str, str]:
    """Return dictionary containing default labels."""
    path = "{root}/normalized_metrics.json".format(
        root=os.path.dirname(os.path.realpath(__file__))
    )
    with open(path, "r") as f:
        return json.load(f)


def is_normalized_metric(metric: str) -> bool:
    """Return boolean representing if given metric is known to be between 0 and 1.

    Parameters
    ----------
    metric:str,
        The metric to check for

    Returns
    -------
    Boolean representing if given metric is known to be between 0 and 1.
    """
    sanitized_metric = sanitize_ml_labels(metric)
    return any(
        candidate in sanitized_metric
        for candidate in load_normalized_metrics()
    )
