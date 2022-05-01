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
        (
            "Has gene product",
            "Interacts with",
            "subPropertyOf",
            "Other"
        ): [
            'biolink:has_gene_product',
            'biolink:interacts_with',
            'biolink:subPropertyOf',
            'other'
        ],
        ("MLP", "CNN", "FFNN", "CAE", "Other"): [
            "   vanilla mlp",
            "vanilla    cnn",
            "vanilla ffnn   ",
            "vanilla cae",
            "other"
        ],
        ("MLP", "CNN", "FFNN", "CAE", "Others"): [
            "   vanilla mlp",
            "vanilla    cnn",
            "vanilla ffnn   ",
            "vanilla cae",
            "Others"
        ],
        ("RAM", "RAM"): ["ram", "Ram"],
        ("CAE 500", ): [
            "cae_500"
        ],
        ("Positive likelihood ratio", "Negative likelihood ratio"): [
            "LR+", "LR-"
        ],
        ("COVID19", "COVID19"): [
            "covid",
            "covid19"
        ],
        ("Non-existent", "Non-existent edges non esistent", "Non-existent edges in graph"): [
            "Non-existent",
            "non-existent-edges non-esistent",
            "non-existent-edges-in-graph"
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
        "$e=100000$": "0.00001",
        "$e=10000$": "0.0001",
        "$e=1000$": "0.001",
        "$e=100$": "0.01",
        "$e=10$": "0.1",
        "$e=1$": "1",
        "$e=0.1$": "10",
        "$e=0.01$": "100",
        "$e=0.001$": "1000",
        "$e=0.0001$": "10000",
        "$e=0.00001$": "100000",
    }

    tests = {
        ("AE VS AP", "AE VS IP"): [
            "active enhancers vs active promoters",
            "active enhancers vs inactive promoters"
        ],
        ("$e=1$",): ["1"],
        ("$e=100000$", ): ["0.00001"],
        ("$e=10000$", ): ["0.0001"],
        ("$e=1000$", ): ["0.001"],
        ("$e=100$", ): ["0.01"],
        ("$e=10$", ): ["0.1"],
        ("$e=1$", ): ["1"],
        ("$e=0.1$", ): ["10"],
        ("$e=0.01$", ): ["100"],
        ("$e=0.001$", ): ["1000"],
        ("$e=0.0001$", ): ["10000"],
        ("$e=0.00001$", ): ["100000"],
        ("$e=100000$", "$e=10000$", "$e=1000$", "$e=100$", "$e=10$", "$e=1$", "$e=0.1$", "$e=0.01$", "$e=0.001$", "$e=0.0001$", "$e=0.00001$",): ["0.00001", "0.0001", "0.001", "0.01", "0.1", "1", "10", "100", "1000", "10000", "100000", ]
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
