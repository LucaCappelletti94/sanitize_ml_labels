from sanitize_ml_labels import sanitize_ml_labels


def test_sanitize_ml_labels():
    tests = {
        ("Accuracy", "Accuracy", "AUROC", "Vanilla MLP", "Loss", "Train AUROC"): [
            "acc", "accuracy", "auroc", "vanilla_mlp", "loss", "train_auroc"
        ],
        ("MLP", "CNN", "FFNN"): [
            "   vanilla mlp",
            "vanilla    cnn",
            "vanilla ffnn   "
        ]
    }
    for goals, starts in tests.items():
        for goal, result in zip(goals, sanitize_ml_labels(starts)):
            assert goal == result

    assert "12" == sanitize_ml_labels(12)

    custom_defaults = {
        "P": "promoters",
        "E": "enhancers",
        "A": "active ",
        "I": "inactive "
    }

    tests = {
        ("AE VS AP", "AE VS IP"): [
            "active enhancers vs active promoters",
            "active enhancers vs inactive promoters"
        ]
    }

    for goals, starts in tests.items():
        for goal, result in zip(goals, sanitize_ml_labels(starts, custom_defaults=custom_defaults)):
            assert goal == result

    tests = {
        ("Acc", "Auroc", "Vanilla MLP", "Loss"): [
            "acc", "auroc", "vanilla_mlp", "loss"
        ]
    }

    for goals, starts in tests.items():
        for goal, result in zip(goals, sanitize_ml_labels(starts, replace_defaults=False)):
            assert goal == result
