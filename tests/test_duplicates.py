"""Test that there are no duplicates in the JSON files."""

import compress_json
from sanitize_ml_labels import sanitize_ml_labels


def test_no_duplicates():
    """Test that there are no duplicates in the JSON files."""
    paths = [
        "absolutely_normalized_metrics.json",
        "descriptors.json",
        "normalized_metrics.json",
        "should_be_maximized.json",
        "should_be_minimized.json",
    ]

    for path in paths:
        data = compress_json.load(f"sanitize_ml_labels/{path}")
        assert len(data) == len(set(data)), f"Duplicate values in {path}"


def test_normalized():
    """All labels in the JSON files should be normalized."""

    paths = [
        "absolutely_normalized_metrics.json",
        "normalized_metrics.json",
        "should_be_maximized.json",
        "should_be_minimized.json",
    ]

    for path in paths:
        for label in compress_json.load(f"sanitize_ml_labels/{path}"):
            # Test that the label is lowecase
            assert label.lower() == label, f"Label {label} in {path} is not lowercase"

            assert (
                sanitize_ml_labels(label).lower() == label
            ), f"Label {label} in {path} is not normalized"
