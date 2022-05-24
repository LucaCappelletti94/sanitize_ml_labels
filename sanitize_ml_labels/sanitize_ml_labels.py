from typing import List, Dict, Union
import re
import compress_json
from more_itertools import rstrip
from sqlalchemy import false
from .find_true_hyphenated_words import find_true_hyphenated_words


def consonants_to_upper(label: str) -> str:
    """Return given label with consonants groups to uppercase.

    Examples
    --------
    Vanilla cnn model -> Vanilla CNN model
    mlp model -> MLP model

    Parameters
    ----------
    label: str
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
    label: str
        label to parse.
    targets: List[str]
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


def are_real_values_labels(labels: List[str]) -> bool:
    """Return whether all labels are floating point values.

    Parameters
    ----------
    labels: List[str],
        labels to parse.
    """
    for label in labels:
        try:
            float(label.strip())
        except ValueError:
            return False
    return True


def sanitize_real_valued_labels(labels: List[str]) -> List[str]:
    """Returns list of real valued labels without trailing zeros.

    Parameters
    ----------
    labels: List[str],
        labels to parse.
    """
    new_labels = []
    for label in labels:
        label = label.strip()
        if "." in label:
            if label.endswith(".0"):
                label = label.split(".")[0]
            else:
                label = ".".join((
                    label.split(".")[0],
                    label.split(".")[1].rstrip("0")
                ))
        new_labels.append(label)
    return new_labels


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
    labels: List[str]
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
    labels: List
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
    detect_and_remove_trailing_zeros: bool = True,
    replace_defaults: bool = True,
    soft_capitalization: bool = True,
    preserve_true_hyphenation: bool = True,
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
    detect_and_remove_trailing_zeros: bool = True
        Whether to remove trailing zeros when labels are all numeric.
    replace_defaults: bool = True
        Whetever to replace default terms.
    soft_capitalization: bool = True
        Whetever to apply soft capitalization,
        replacing capitalization only when no capitalization is already present.
    preserve_true_hyphenation: bool = True
        Whether we should try to preserve the true hyphenation
        when the hyphen character should be otherwise removed.
        Consider that this is done through a comprehensive heuristic
        using over 45k hyphenated words from the English language.
    custom_defaults: Dict[str, Union[List[str], str]] = None
        List of custom defaults to be used for remapping.

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

    if detect_and_remove_trailing_zeros:
        if are_real_values_labels(labels):
            labels = sanitize_real_valued_labels(labels)

    # If the hyphen character is among the characters that we should
    # remove to normalize the label and it is requested to preserve
    # the true hyphenation wherever possible, we try to identify
    # the true hyphenated words through an heuristic
    need_to_run_hyphenation_check = (
        "-" in replace_with_spaces and
        preserve_true_hyphenation and
        any("-" in label for label in labels)
    )

    if need_to_run_hyphenation_check:
        new_labels = []
        hyphenated_words = []
        for label in labels:
            if "-" in label:
                lowercase_label = label.lower()
                true_hyphenated_words = find_true_hyphenated_words(
                    lowercase_label)
                for true_hyphenated_word in true_hyphenated_words:
                    position = lowercase_label.find(true_hyphenated_word)
                    true_hyphenated_word_with_possible_capitalization = label[position:position+len(
                        true_hyphenated_word)]
                    label = label.replace(true_hyphenated_word_with_possible_capitalization, "{{word{number}}}".format(
                        number=len(hyphenated_words)
                    ))
                    hyphenated_words.append(
                        true_hyphenated_word_with_possible_capitalization)
            new_labels.append(label)

        # We update the current labels with the new labels
        # that are now wrapped to avoid to remove hyphenated words.
        labels = new_labels

    labels = [
        targets_to_spaces(label, replace_with_spaces)
        for label in labels
    ]

    labels = clear_spaces(labels)

    # We now need to restore the hyphenated words which we have
    # previously wrapped, if we have done so.
    if need_to_run_hyphenation_check:
        restored_labels = []
        for label in labels:
            for i, hyphenated_word in enumerate(hyphenated_words):
                label = label.replace(
                    "{{word{number}}}".format(number=i),
                    hyphenated_word
                )
            restored_labels.append(label)
        labels = restored_labels

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
