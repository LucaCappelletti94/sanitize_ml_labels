from sanitize_ml_labels import is_normalized_metric

def test_is_normalized_metric():
    tests = {
        True: [
            "acc", "accuracy", "Accuracy", "AUROC", "auroc", "auprc", "AUPRC"
        ],
        False: [
            "MLP"
        ]
    }

    for expected, metrics in tests.items():
        for metric in metrics:
            assert is_normalized_metric(metric) == expected