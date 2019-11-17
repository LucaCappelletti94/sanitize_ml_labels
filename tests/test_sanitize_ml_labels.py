from sanitize_ml_labels import sanitize_ml_labels

def test_sanitize_ml_labels():
    tests = {
        ("Accuracy", "AUROC", "Vanilla MLP", "Loss"): [
            "acc", "auroc", "vanilla_mlp", "loss"
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
    
    custom_defaults = {
        "P":"promoters",
        "E":"enhancers",
        "A":"active ",
        "I":"inactive "
    }

    tests = {
        ("AE VS AP", "AE VS IP"):[
            "active enhancers vs active promoters",
            "active enhancers vs inactive promoters"
        ]
    }

    for goals, starts in tests.items():
        for goal, result in zip(goals, sanitize_ml_labels(starts, custom_defaults=custom_defaults)):
            assert goal == result