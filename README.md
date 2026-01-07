# Sanitize ML Labels

[![PyPI](https://badge.fury.io/py/sanitize-ml-labels.svg)](https://badge.fury.io/py/sanitize-ml-labels)
[![Downloads](https://pepy.tech/badge/sanitize-ml-labels)](https://pepy.tech/badge/sanitize-ml-labels)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/LucaCappelletti94/sanitize_ml_labels/blob/master/LICENSE)
[![CI](https://github.com/LucaCappelletti94/sanitize_ml_labels/actions/workflows/python.yml/badge.svg)](https://github.com/LucaCappelletti94/sanitize_ml_labels/actions)

Sanitize ML Labels is a Python package designed to standardize and sanitize ML-related labels. Currently supports over 100 labels, including metric and model names.

If you have ML-related labels, and you find yourself renaming and sanitizing them in a consistent manner, with the proper capitalizaton, this package ensures they are always sanitized in a standard way.

## How do I install this package?

You can install it using pip:

```bash
pip install sanitize_ml_labels
```

## Usage examples

Here are some common use cases for normalizing labels:

### Example for metrics

```python
from sanitize_ml_labels import sanitize_ml_labels

labels = [
    "acc",
    "loss",
    "auroc",
    "lr"
]

assert sanitize_ml_labels(labels) == [
    "Accuracy",
    "Loss",
    "AUROC",
    "Learning rate"
]
```

### Example for models

```python
from sanitize_ml_labels import sanitize_ml_labels

labels = [
    "mlp",
    "cnn",
    "ffNN",
    "Feed-forward neural network",
    "perceptron",
    "recurrent neural network",
    "LStM"
]

assert sanitize_ml_labels(labels) == [
    "MLP",
    "CNN",
    "FFNN",
    "FFNN",
    "Perceptron",
    "RNN",
    "LSTM"
]

assert sanitize_ml_labels("vanilla mlp") == "MLP"
assert sanitize_ml_labels("vanilla cnn") == "CNN"

assert sanitize_ml_labels([
    "Large Language Model",
    "transe",
    "Generative Pre-trained Transformer",
    "Graph Convolutional Neural Network",
    "Convolutional Graph Neural Network",
    "Graph Neural Network",
    "Graph Attention Network",
    "Graph Attention Neural Network",
]) == ["LLM","TransE","GPT","GCN","GCN","GNN","GAT","GAT"]
```

Sometimes, it happens that you have prefixed all your models with "vanilla" or "simple" or "basic". This package can help you remove these prefixes.

```python
from sanitize_ml_labels import sanitize_ml_labels

labels = [
    "vanilla mlp",
    "vanilla cnn",
    "vanilla ffnn",
    "vanilla perceptron"
]

assert sanitize_ml_labels(labels) == ["MLP", "CNN", "FFNN", "Perceptron"]
```

## Corner cases

Sometimes, you might encounter hyphenated terms that need to be correctly identified and normalized. We use a heuristic approach based on an [extended list of over 45K hyphenated English words](https://github.com/LucaCappelletti94/sanitize_ml_labels/blob/master/hyphenations.json.gz), originally from the [Metadata consulting website](https://metadataconsulting.blogspot.com/2019/07/An-extensive-massive-near-complete-list-of-all-English-Hyphenated-words.html).

The lookup heuristic, written by [Tommaso Fontana](https://github.com/zommiommy), ensures efficient and accurate hyphenated word recognition.

```python
from sanitize_ml_labels import sanitize_ml_labels

# Running the following
assert sanitize_ml_labels("non-existent-edges-in-graph") == "Non-existent edges in graph"
```

## Extra utilities

In addition to label sanitization, the package provides methods to check metric normalization:

### Is normalized metric

Validates if a metric falls within the range [0, 1].

```python
from sanitize_ml_labels import is_normalized_metric

assert not is_normalized_metric("MSE")
assert is_normalized_metric("acc")
assert is_normalized_metric("accuracy")
assert is_normalized_metric("AUROC")
assert is_normalized_metric("auprc")
```

### Is absolutely normalized metric

Validates if a metric falls within the range [-1, 1].

```python
from sanitize_ml_labels import is_absolutely_normalized_metric

assert not is_absolutely_normalized_metric("auprc")
assert is_absolutely_normalized_metric("MCC")
assert is_absolutely_normalized_metric("Markedness")
```

### Shoud be maximized

Whether a metric should be maximized or minimized. Unknown metrics will raise a `NotImplementedError`.

```python
from sanitize_ml_labels import should_be_maximized

assert not should_be_maximized("MSE")
assert should_be_maximized("AUROC")
assert should_be_maximized("accuracy")
```

## License

This software is licensed under the MIT license. See the [LICENSE](https://github.com/LucaCappelletti94/sanitize_ml_labels/blob/master/LICENSE).
