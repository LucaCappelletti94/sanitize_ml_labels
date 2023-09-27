import compress_json
from .sanitize_ml_labels import sanitize_ml_labels


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
    sanized_metric_name = sanitize_ml_labels(metric_name)
    
    if sanized_metric_name in compress_json.local_load("should_be_maximized.json"):
        return True
    
    if sanized_metric_name in compress_json.local_load("should_be_minimized.json"):
        return False

    raise NotImplementedError(
        f"The provided metric {metric_name}, sanitized to {sanized_metric_name}, "
        "if not currently supported. Please open an issue and relative pull request "
        "to add this metric to this method. Thanks!"
    )
