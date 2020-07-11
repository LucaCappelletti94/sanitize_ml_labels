from typing import List, Dict, Union
import re
import os
import json


def consonants_to_upper(label: str) -> str:
    """Return given label with consonants groups to uppercase.

    Examples
    --------
    Vanilla cnn model -> Vanilla CNN model
    mlp model -> MLP model

    Parameters
    ----------
    label: str,
        label to parse.

    Returns
    -------
    Label with formatted consonants.
    """
    return re.sub(
        r"\b([b-df-hj-np-tv-zB-DF-HJ-NP-TV-Z]{2,})\b",
        lambda x:  x.group(1).upper(),
        label
    )


def targets_to_spaces(label: str, targets: List[str]) -> str:
    """Return given label with consonants groups to uppercase.

    Examples
    --------
    vanilla-cnn_model -> vanilla cnn model
    mlp_model -> mlp_model

    Parameters
    ----------
    label: str,
        label to parse.
    targets: List[str],
        list of targets to replace to spaces.

    Returns
    -------
    Label with replaced spaces.
    """
    for target in targets:
        if target in label:
            label = label.replace(target, " ")
    return label


def all_vanillas(labels: List[str]) -> bool:
    """Return boolean representing if all labels contain the word 'vanilla'

    Parameters
    ----------
    labels: List[str],
        labels to parse.

    Returns
    -------
    Boolean representing whetever labels are all vanilla.
    """
    return all(
        "vanilla" in label
        for label in labels
    )


def remove_vanilla(labels: List[str]) -> List[str]:
    """Return list of labels without the term 'vanilla'"""
    return [
        label.replace("vanilla", "")
        for label in labels
    ]


def load_defaults() -> Dict[str, str]:
    """Return dictionary containing default labels."""
    path = "{root}/labels.json".format(
        root=os.path.dirname(os.path.realpath(__file__))
    )
    with open(path, "r") as f:
        return json.load(f)


def apply_replace_defaults(labels: List[str], custom_defaults: Dict[str, List[str]]) -> List[str]:
    """Return list of labels with replaced defaults."""
    defaults = {
        **load_defaults(),
        **custom_defaults
    }
    new_labels = []
    for label in labels:
        replace_candidates = []
        for default, targets in defaults.items():
            for target in targets:
                regex = re.compile(target)
                matches = regex.findall(label.lower())
                if bool(matches):
                    replace_candidates.append((matches[0], default))

        # The following is required to avoid replacing substrings.
        
        replace_candidates = sorted(
            replace_candidates,
            key=lambda x: len(x[0]),
            reverse=False
        )

        replace_candidates = [
            (j, val)
            for i, (j, val) in enumerate(replace_candidates)
            if all(j not in k.lower() for _, k in replace_candidates[i + 1:])
        ]

        replace_candidates = sorted(
            replace_candidates,
            key=lambda x: len(x[0]),
            reverse=True
        )

        for target, default in replace_candidates:
            label = re.compile(re.escape(target), re.IGNORECASE).sub(default, label)
        new_labels.append(label)
    return new_labels


def clear_spaces(labels: List[str]) -> List[str]:
    """Remove multiple sequences of spaces and strip spaces from labels."""
    return [
        " ".join(label.split()).strip()
        for label in labels
    ]


def apply_soft_capitalization(labels: List[str]) -> List[str]:
    """Return labels capitalized only when no other capitalization is present."""
    return [
        label.capitalize() if label.lower() == label
        else label
        for label in labels
    ]


def to_string(labels: List[str]) -> List[str]:
    """Convert all labels to strings."""
    return [
        str(label)
        for label in labels
    ]


def sanitize_ml_labels(
    labels: Union[List[str], str],
    upper_case_consonants_clusters: bool = True,
    replace_with_spaces: List[str] = ("-", "_"),
    detect_and_remove_vanilla: bool = True,
    replace_defaults: bool = True,
    soft_capitalization: bool = True,
    custom_defaults: Dict[str, Union[List[str], str]] = None
) -> List[str]:
    """Return sanitized labels in standard way.

    Parameters
    ----------
    labels: Union[List[str], str],
        Wither label or list of labels to sanitize.
    upper_case_consonants_clusters: bool = True,
        Whetever to convert to upper case detected initials.
    replace_with_spaces: List[str] = ("-", "_"),
        Characters to be replaced with spaces.
    detect_and_remove_vanilla: bool = True,
        Whetever to remove the term 'vanilla' when all terms contain it.
    replace_defaults: bool = True,
        Whetever to replace default terms.
    soft_capitalization: bool = True
        Whetever to apply soft capitalization,
        replacing capitalization only when no capitalization is already present.

    Returns
    -------
    Sanitized labels.
    """

    try:
        iter(labels)
        is_iterable = True
    except TypeError:
        is_iterable = False

    single_label = not is_iterable or isinstance(labels, str)
    if single_label:
        labels = [labels]

    labels = to_string(labels)

    if detect_and_remove_vanilla and all_vanillas(labels):
        labels = remove_vanilla(labels)

    if soft_capitalization:
        labels = apply_soft_capitalization(labels)

    if replace_defaults:
        if custom_defaults is None:
            custom_defaults = dict()

        custom_defaults = dict([
            (key, value) if isinstance(value, list)
            else (key, [value])
            for key, value in custom_defaults.items()
        ])
        labels = apply_replace_defaults(labels, custom_defaults)

    labels = [
        targets_to_spaces(label, replace_with_spaces)
        for label in labels
    ]

    if upper_case_consonants_clusters:
        labels = [
            consonants_to_upper(label)
            for label in labels
        ]

    labels = clear_spaces(labels)

    if single_label:
        return labels[0]
    return labels
