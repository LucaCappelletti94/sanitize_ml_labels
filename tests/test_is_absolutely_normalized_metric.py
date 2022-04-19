from sanitize_ml_labels import is_absolutely_normalized_metric


def test_is_absolutely_normalized_metric():
    tests = {
        True: [
            "MCC",
            "Markedness"
        ],
        False: [
            "MLP", "Relu", "acc", "Accuracy", "AUROC"
        ]
    }

    for expected, metrics in tests.items():
        for metric in metrics:
            assert is_absolutely_normalized_metric(metric) == expected
