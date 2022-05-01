sanitize_ml_labels
=========================================================================================
|pip| |downloads|

Simple python package to sanitize in a standard way ML-related labels.

Why do I need this?
-------------------
So you have some kind of plot and you have some ML-related labels.
Since I always rename and sanitize them the same way, I have prepared
this package to always sanitize them in a standard fashion.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install sanitize_ml_labels


Usage examples
----------------------------------------------
Here you have a couple of common examples: you have a set of metrics to normalize or a set of model names to normalize.

.. code:: python

    from sanitize_ml_labels import sanitize_ml_labels

    # Example for metrics
    labels = [
        "acc",
        "loss",
        "auroc",
        "lr"
    ]

    sanitize_ml_labels(labels)

    # ["Accuracy", "Loss", "AUROC", "Learning rate"]

    # Example for models
    labels = [
        "vanilla mlp",
        "vanilla cnn",
        "vanilla ffnn",
        "vanilla perceptron"
    ]

    sanitize_ml_labels(labels)

    # ["MLP", "CNN", "FFNN", "Perceptron"]

Corner cases
~~~~~~~~~~~~~~~~
In some cases, you may have a combination of terms separated by hyphens that must be removed, plus words
that are actually correctly written separated by hyphens. We approach this problem with an heuristic
based on an `extended list of over 45K hyphenated english words <https://github.com/LucaCappelletti94/sanitize_ml_labels/blob/master/hyphenations.json.gz>`__, originally retrieved from
the `Metadata consulting website <https://metadataconsulting.blogspot.com/2019/07/An-extensive-massive-near-complete-list-of-all-English-Hyphenated-words.html>`__.

From such a word list, we generate an index by running:

.. code:: python

    index = {}
    for word in words:
        word = word.lower()
        index.setdefault(word[0], []).append((word, word[1:]))

And from there the user experience is transparent and looks as follows:

.. code:: python

    # Running the following
    sanitize_ml_labels("non-existent-edges-in-graph")
    # will yield the string `Non-existent edges in graph`

The lookup heuristic to quickly find an hyphenated word in a given label from the large haystack
was written by `Tommaso Fontana <https://github.com/zommiommy>`__.


Extra utilities
---------------
Since I always use metric sanitization alongside axis normalization, it is useful to know which axis
should be maxed between zero and one to avoid any visualization bias to the metrics.

For this reason I have created the method :code:`is_normalized_metric`, which after having normalized the given metric
validates it against known normalized metrics (metrics between 0 and 1, is there another name? I could not figure out a better one).

Analogously, I have also created the method :code:`is_absolutely_normalized_metric` to validate a metric for the range
between -1 and 1.

.. code:: python

    from sanitize_ml_labels import is_normalized_metric, is_absolutely_normalized_metric

    is_normalized_metric("MSE") # False
    is_normalized_metric("acc") # True
    is_normalized_metric("accuracy") # True
    is_normalized_metric("AUROC") # True
    is_normalized_metric("auprc") # True
    is_absolutely_normalized_metric("auprc") # False
    is_absolutely_normalized_metric("MCC") # True
    is_absolutely_normalized_metric("Markedness") # True


New features and issues
-----------------------
As always, for new features and issues you can either open a new issue and pull request.
A pull request will always be the quicker way, but I'll look into the issues when I get the time.

Tests Coverage
----------------------------------------------
I have strived to mantain a 100% code coverage in this project:

+---------------------------------------------------+------------+---------+----------+----------+
| Module                                            | statements | missing | excluded | coverage |
+===================================================+============+=========+==========+==========+
| Total                                             | 84         | 0       | 0        | 100%     |
+---------------------------------------------------+------------+---------+----------+----------+
| sanitize_ml_labels/__init__.py                    | 3          | 0       | 0        | 100%     |
+---------------------------------------------------+------------+---------+----------+----------+
| sanitize_ml_labels/__version__.py                 | 1          | 0       | 0        | 100%     |
+---------------------------------------------------+------------+---------+----------+----------+
| sanitize_ml_labels/is_normalized_metric.py        | 10         | 0       | 0        | 100%     |
+---------------------------------------------------+------------+---------+----------+----------+
| sanitize_ml_labels/find_true_hyphenated_words.py  | 19         | 0       | 0        | 100%     |
+---------------------------------------------------+------------+---------+----------+----------+
| sanitize_ml_labels/sanitize_ml_labels.py          | 70         | 0       | 0        | 100%     |
+---------------------------------------------------+------------+---------+----------+----------+

You can verify the test coverage of this repository by running in its root:

.. code:: bash

    pytest --cov

.. |pip| image:: https://badge.fury.io/py/sanitize-ml-labels.svg
    :target: https://badge.fury.io/py/sanitize-ml-labels
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/sanitize-ml-labels
    :target: https://pepy.tech/badge/sanitize-ml-labels
    :alt: Pypi total project downloads 