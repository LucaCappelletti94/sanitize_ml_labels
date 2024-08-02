"""Module to determine whether a metric should be maximized or minimized."""

from sanitize_ml_labels.is_normalized_metric import check_in_set, sanitize_ml_labels


def should_be_maximized(metric_name: str) -> bool:
    """Returns whether the provided metric should be maximized.

    Examples
    ----------------------
    The MSE is a metric to mimize, so the method will return False.
    The Accuracy is a metric to maximize, so the method will return True.

    Returns
    ----------------------
    Boolean representing whether the provided metric should be maximized.
    """
    if check_in_set(metric_name, "should_be_maximized"):
        return True

    if check_in_set(metric_name, "should_be_minimized"):
        return False

    raise NotImplementedError(
        f"The provided metric {metric_name}, sanitized to {sanitize_ml_labels(metric_name)}, "
        "if not currently supported. Please open an issue and relative pull request "
        "to add this metric to this method. Thanks!"
    )
