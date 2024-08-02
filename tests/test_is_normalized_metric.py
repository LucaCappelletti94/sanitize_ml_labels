"""Tests for the is_normalized_metric function."""

from sanitize_ml_labels import is_normalized_metric, sanitize_ml_labels


def test_is_normalized_metric():
    """Test the is_normalized_metric function."""
    tests = {
        True: [
            "acc",
            "accuracy",
            "Accuracy",
            "AUROC",
            "auroc",
            "auprc",
            "AUPRC",
            "test auroc",
            "train auroc",
            "train categorical_accuracy",
            "val_auroc",
            "precision",
            "recall_1",
            "recall_6",
            "F1Score",
            "F1 Score",
            "F1 score",
        ],
        False: ["MLP", "Relu"],
    }

    for expected, metrics in tests.items():
        for metric in metrics:
            normalized_metric_name = sanitize_ml_labels(metric)
            assert (
                is_normalized_metric(metric) == expected
            ), f"Expected normalize status to be {expected} for {metric} ({normalized_metric_name})"
