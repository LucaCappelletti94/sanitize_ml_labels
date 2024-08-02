# Sanitize ML Labels

[![PyPI](https://badge.fury.io/py/sanitize-ml-labels.svg)](https://badge.fury.io/py/sanitize-ml-labels)
[![Downloads](https://pepy.tech/badge/sanitize-ml-labels)](https://pepy.tech/badge/sanitize-ml-labels)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/LucaCappelletti94/sanitize_ml_labels/blob/master/LICENSE)
![CI](https://github.com/LucaCappelletti94/sanitize-ml-labels/actions/workflows/python.yml/badge.svg)

Sanitize ML Labels is a Python package designed to standardize and sanitize ML-related labels.

If you have ML-related labels, and you find yourself renaming and sanitizing them in a consistent manner, this package ensures they are always sanitized in a standard way.

## How Do I Install This Package?

You can install it using pip:

```bash
pip install sanitize_ml_labels
```

## Usage Examples

Here are some common use cases for normalizing labels:

### Example for Metrics

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

### Example for Models

```python
from sanitize_ml_labels import sanitize_ml_labels

labels = [
    "vanilla mlp",
    "vanilla cnn",
    "vanilla ffnn",
    "vanilla perceptron"
]

print(sanitize_ml_labels(labels))
# Output: ["MLP", "CNN", "FFNN", "Perceptron"]
```

## Corner Cases

Sometimes, you might encounter hyphenated terms that need to be correctly identified and normalized. We use a heuristic approach based on an [extended list of over 45K hyphenated English words](https://github.com/LucaCappelletti94/sanitize_ml_labels/blob/master/hyphenations.json.gz), originally from the [Metadata consulting website](https://metadataconsulting.blogspot.com/2019/07/An-extensive-massive-near-complete-list-of-all-English-Hyphenated-words.html).

The lookup heuristic, written by [Tommaso Fontana](https://github.com/zommiommy), ensures efficient and accurate hyphenated word recognition.

```python
from sanitize_ml_labels import sanitize_ml_labels

# Running the following
print(sanitize_ml_labels("non-existent-edges-in-graph"))
# Output: Non-existent edges in graph
```

## Extra Utilities

In addition to label sanitization, the package provides methods to check metric normalization:

### `is_normalized_metric`

Validates if a metric falls within the range [0, 1].

```python
from sanitize_ml_labels import is_normalized_metric

print(is_normalized_metric("MSE")) # False
print(is_normalized_metric("acc")) # True
print(is_normalized_metric("accuracy")) # True
print(is_normalized_metric("AUROC")) # True
print(is_normalized_metric("auprc")) # True
```

### `is_absolutely_normalized_metric`

Validates if a metric falls within the range [-1, 1].

```python
from sanitize_ml_labels import is_absolutely_normalized_metric

print(is_absolutely_normalized_metric("auprc")) # False
print(is_absolutely_normalized_metric("MCC")) # True
print(is_absolutely_normalized_metric("Markedness")) # True
```

## New Features and Issues

For new features or issues, you can open a new issue or submit a pull request. Pull requests are typically processed faster, but all issues will be reviewed when time permits.
