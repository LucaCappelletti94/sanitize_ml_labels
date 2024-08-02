"""Test suite for the should_be_maximized submodule."""

import pytest
import compress_json
from sanitize_ml_labels import should_be_maximized


def test_should_be_maximized_corner_cases():
    """Test the should_be_maximized method with corner cases."""
    with pytest.raises(NotImplementedError):
        should_be_maximized("not a valid metric")


def test_should_be_maximized():
    """Test the should_be_maximized method."""
    assert should_be_maximized("Accuracy")
    assert not should_be_maximized("MSE")
    assert should_be_maximized("AUROC")
    assert should_be_maximized("Recall")
    assert should_be_maximized("Precision")
    assert should_be_maximized("F1")
    assert should_be_maximized("F1 Score")
    assert should_be_maximized("F1-score")

    # All of the metrics reported in the
    # normalized_metrics.json files should
    # be executable in the should_be_maximized
    # method.

    exceptions = ["jaccard index"]

    for metric in compress_json.load("sanitize_ml_labels/normalized_metrics.json"):
        # None of these metrics should raise an error
        if metric not in exceptions:
            should_be_maximized(metric)
