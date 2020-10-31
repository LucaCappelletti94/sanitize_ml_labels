from sanitize_ml_labels import sanitize_ml_labels


def test_sanitize_ml_labels():
    tests = {
        ("Accuracy", "Accuracy", "AUROC", "Vanilla MLP", "Loss", "Train AUROC", "Categorical accuracy", "Precision", "Precision", "Recall", "Recall"): [
            "acc", "accuracy", "auroc", "vanilla_mlp", "loss", "train_auroc", "categorical_accuracy", "precision_67", "Precision_67", "recall_5", "Recall_5"
        ],
        ("MLP", "CNN", "FFNN", "CAE"): [
            "   vanilla mlp",
            "vanilla    cnn",
            "vanilla ffnn   ",
            "vanilla cae"
        ],
        ("RAM", "RAM"): ["ram", "Ram"],
        ("CAE 500", ): [
            "cae_500"
        ]
    }
    errors = []
    for goals, starts in tests.items():
        for goal, result in zip(goals, sanitize_ml_labels(starts)):
            if goal != result:
                errors.append((goal, result))

    custom_defaults = {
        "P": "promoters",
        "E": "enhancers",
        "A": "active ",
        "I": "inactive ",
        "$e=1$": "1",
    }

    tests = {
        ("AE VS AP", "AE VS IP"): [
            "active enhancers vs active promoters",
            "active enhancers vs inactive promoters"
        ],
        ("$e=1$", ): ["1"]
    }

    for goals, starts in tests.items():
        for goal, result in zip(goals, sanitize_ml_labels(starts, custom_defaults=custom_defaults)):
            if goal != result:
                errors.append((goal, result))

    tests = {
        ("Acc", "Auroc", "Vanilla MLP", "Loss"): [
            "acc", "auroc", "vanilla_mlp", "loss"
        ]
    }

    for goals, starts in tests.items():
        for goal, result in zip(goals, sanitize_ml_labels(starts, replace_defaults=False)):
            if goal != result:
                errors.append((goal, result))

    assert not errors

    assert "12" == sanitize_ml_labels(12)
