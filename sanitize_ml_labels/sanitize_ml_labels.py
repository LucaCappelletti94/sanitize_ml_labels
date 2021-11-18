from typing import List, Dict, Union
import re
import compress_json


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


def have_descriptor(labels: List[str], descriptor: str, generic_words_cooccurring_with_descriptors: List[str]) -> bool:
    """Return boolean representing if all labels contain the given descriptor.

    Parameters
    ----------
    labels: List[str],
        labels to parse.
    descriptor: str,
        The descriptor that all texts need to contain.
        A descriptor is a term like 'vanilla' or 'biolink', that is often
        added to all the terms in a set. When all terms in a set have the
        same descriptor, there is no need for the descriptor to be shown
        in the first place and only contributes to cluttering in the
        visualization at hand.
    generic_words_cooccurring_with_descriptors: List[str],
        List of words that is known to appear with descriptors.
        Some words, like 'Other' or 'Unknown' often are added to descriptors
        sets, without the main descriptor. In these cases we still want to drop
        the descriptor if all the other terms have it.

    Returns
    -------
    Boolean representing whetever labels are all with descriptor.
    """
    return all(
        descriptor in label
        for label in labels
        if label.lower() not in generic_words_cooccurring_with_descriptors
    )


def remove_descriptor(labels: List[str], descriptor: str) -> List[str]:
    """Return list of labels without the term descriptor"""
    return [
        label.replace(descriptor, "")
        for label in labels
    ]


def apply_replace_defaults(labels: List[str], custom_defaults: Dict[str, List[str]]) -> List[str]:
    """Return list of labels with replaced defaults."""
    defaults = {
        **{
            key: [
                "(?<![a-z]){}(?![a-z])".format(val)
                for val in values
            ]
            for key, values in compress_json.local_load("labels.json").items()
        },
        **custom_defaults
    }
    new_labels = []
    for label in labels:
        replace_candidates = []
        for default, targets in defaults.items():
            for target in targets:
                regex = re.compile(target, re.IGNORECASE)
                matches = regex.findall(label)
                if bool(matches):
                    for match in matches:
                        replace_candidates.append((match, default))

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
            label = label.replace(target, default)
        new_labels.append(label)
    return new_labels


def clear_spaces(labels: List[str]) -> List[str]:
    """Remove multiple sequences of spaces and strip spaces from labels.

    Parameters
    ---------------------------------
    labels: List[str],
        The labels from where to remove the duplicated spaces.

    Returns
    ---------------------------------
    List of labels without duplicated spaces.
    """
    return [
        " ".join([
            term
            for term in label.split()
            if term
        ])
        for label in labels
    ]


def apply_soft_capitalization(labels: List[str]) -> List[str]:
    """Return labels capitalized only when no other capitalization is present.

    Parameters
    ------------------------
    labels: List[str],
        The labels where to apply soft capitalization.

    Returns
    ------------------------
    List of labels with soft capitalization applied.
    """
    return [
        label.capitalize() if label.lower() == label
        else label
        for label in labels
    ]


def to_string(labels: List) -> List[str]:
    """Convert all labels to strings.

    Parameters
    -----------------------
    labels: List,
        The labels to be converted  to strings if they are not already.

    Returns
    -----------------------
    List with labels converted to strings.
    """
    return [
        str(label)
        for label in labels
    ]


def sanitize_ml_labels(
    labels: Union[List[str], str],
    upper_case_consonants_clusters: bool = True,
    replace_with_spaces: List[str] = ("-", "_", ":", "<", ">"),
    detect_and_remove_homogeneous_descriptors: bool = True,
    replace_defaults: bool = True,
    soft_capitalization: bool = True,
    custom_defaults: Dict[str, Union[List[str], str]] = None
) -> List[str]:
    """Return sanitized labels in standard way.

    Parameters
    ----------
    labels: Union[List[str], str]
        Wither label or list of labels to sanitize.
    upper_case_consonants_clusters: bool = True
        Whetever to convert to upper case detected initials.
    replace_with_spaces: List[str] = ("-", "_", ":", "<", ">")
        Characters to be replaced with spaces.
    detect_and_remove_homogeneous_descriptors: bool = True
        Whetever to remove the known descriptors when all terms contain it.
    replace_defaults: bool = True
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

    if detect_and_remove_homogeneous_descriptors:
        generic_words_cooccurring_with_descriptors = compress_json.local_load(
            "generic_words_cooccurring_with_descriptors.json"
        )
        for descriptor in compress_json.local_load("descriptors.json"):
            if have_descriptor(labels, descriptor, generic_words_cooccurring_with_descriptors):
                labels = remove_descriptor(
                    labels,
                    descriptor
                )

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

    labels = clear_spaces(labels)

    if soft_capitalization:
        labels = apply_soft_capitalization(labels)

    if upper_case_consonants_clusters:
        labels = [
            consonants_to_upper(label)
            for label in labels
        ]

    if single_label:
        return labels[0]
    return labels
