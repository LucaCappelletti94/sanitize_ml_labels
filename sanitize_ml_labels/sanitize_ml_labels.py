"""Module to sanitize machine learning labels."""

from typing import List, Dict, Union, Optional, Tuple, Any
import re
import compress_json
from sanitize_ml_labels.find_true_hyphenated_words import find_true_hyphenated_words


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
        lambda x: x.group(1).upper(),
        label,
    )


def targets_to_spaces(label: str, targets: Union[Tuple[str, ...], List[str]]) -> str:
    """Return given label with consonants groups to uppercase.

    Examples
    --------
    vanilla-cnn_model -> vanilla cnn model
    mlp_model -> mlp_model

    Parameters
    ----------
    label: str
        label to parse.
    targets: Union[Tuple[str, ...], List[str]]
        list of targets to replace to spaces.

    Returns
    -------
    Label with replaced spaces.
    """
    for target in targets:
        if target in label:
            label = label.replace(target, " ")
    return label


def have_descriptor(
    labels: List[str],
    descriptor: str,
    generic_words_cooccurring_with_descriptors: List[str],
) -> bool:
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


def sanitize_real_valued_labels(
    labels: List[str], maximum_resolution: int
) -> List[str]:
    """Returns list of real valued labels without trailing zeros.

    Parameters
    ----------
    labels: List[str]
        labels to parse.
    maximum_resolution: int
        Maximum length of the floating point part.
    """
    new_labels = []
    for label in labels:
        label = label.strip()
        if "." in label:
            label = f"{{:.{maximum_resolution}f}}".format(float(label))
            label = ".".join(
                (label.split(".")[0], label.split(".")[1].rstrip("0"))
            ).strip(".")

        new_labels.append(label)
    return new_labels


def remove_descriptor(labels: List[str], descriptor: str) -> List[str]:
    """Return list of labels without the term descriptor"""
    # Escaping descriptor to avoid issues with special characters
    descriptor = re.escape(descriptor)
    # We remove the descriptor and any separator that might follow it
    return [re.sub(f"{descriptor}[\\.\\-_:\\s]?", "", label) for label in labels]


def apply_replace_defaults(
    labels: List[str], custom_defaults: Dict[str, List[str]]
) -> List[str]:
    """Return list of labels with replaced defaults."""
    defaults = {
        **{
            key: [f"(?<![a-z]){val}(?![a-z])" for val in values]
            for key, values in compress_json.local_load("labels.json").items()
        },
        **custom_defaults,
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
                        replace_candidates.append((match, default, regex))

        # The following is required to avoid replacing substrings.

        replace_candidates = sorted(
            replace_candidates, key=lambda x: len(x[0]), reverse=False
        )

        # If a smaller candidate default is fully contained in another
        # larger candidate default, we remove the smaller candidate default.

        replace_candidates = [
            (target, val, regex)
            for i, (target, val, regex) in enumerate(replace_candidates)
            if all(
                target.lower() not in k.lower()
                for _, k, _ in replace_candidates[i + 1 :]
            )
        ]

        replace_candidates = sorted(
            replace_candidates, key=lambda x: len(x[0]), reverse=True
        )

        for target, default, regex in replace_candidates:
            label = regex.sub(default, label)

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
    return [" ".join([term for term in label.split() if term]) for label in labels]


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
    return [label.capitalize() if label.lower() == label else label for label in labels]


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
    return [str(label) for label in labels]


def sanitize_ml_labels(
    labels: Union[List[Any], Any],
    upper_case_consonants_clusters: bool = True,
    replace_with_spaces: Union[Tuple[str, ...], List[str]] = ("-", "_", ":", "<", ">"),
    detect_and_remove_homogeneous_descriptors: bool = True,
    detect_and_remove_trailing_zeros: bool = True,
    replace_defaults: bool = True,
    soft_capitalization: bool = True,
    preserve_true_hyphenation: bool = True,
    maximum_resolution: int = 3,
    custom_defaults: Optional[Dict[str, Union[List[str], str]]] = None,
) -> Union[List[str], str]:
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
    maximum_resolution: int = 3
        Maximum number of digits to preserve in real-valued labels.
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
    if is_iterable and not isinstance(labels, str):
        normalized_labels: List[Any] = labels
    else:
        normalized_labels = [labels]

    string_labels: List[str] = to_string(normalized_labels)

    if detect_and_remove_homogeneous_descriptors:
        generic_words_cooccurring_with_descriptors = compress_json.local_load(
            "generic_words_cooccurring_with_descriptors.json"
        )
        for descriptor in compress_json.local_load("descriptors.json"):
            if have_descriptor(
                string_labels, descriptor, generic_words_cooccurring_with_descriptors
            ):
                string_labels = remove_descriptor(string_labels, descriptor)

    if soft_capitalization:
        string_labels = apply_soft_capitalization(string_labels)

    if replace_defaults:
        if custom_defaults is None:
            custom_defaults = {}

        normalized_custom_defaults: Dict[str, List[str]] = {
            key: value if isinstance(value, list) else [value]
            for key, value in custom_defaults.items()
        }

        string_labels = apply_replace_defaults(
            string_labels, normalized_custom_defaults
        )

    if detect_and_remove_trailing_zeros and are_real_values_labels(string_labels):
        string_labels = sanitize_real_valued_labels(
            string_labels, maximum_resolution=maximum_resolution
        )
    else:

        # If the hyphen character is among the characters that we should
        # remove to normalize the label and it is requested to preserve
        # the true hyphenation wherever possible, we try to identify
        # the true hyphenated words through an heuristic
        need_to_run_hyphenation_check = (
            "-" in replace_with_spaces
            and preserve_true_hyphenation
            and any("-" in label for label in string_labels)
        )

        if need_to_run_hyphenation_check:
            new_labels = []
            hyphenated_words: List[str] = []
            for label in string_labels:
                if "-" in label:
                    lowercase_label = label.lower()
                    true_hyphenated_words = find_true_hyphenated_words(lowercase_label)
                    for true_hyphenated_word in true_hyphenated_words:
                        lowercase_label = label.lower()
                        position = lowercase_label.find(true_hyphenated_word)
                        if position == -1:
                            continue
                        true_hyphenated_word_with_possible_capitalization = label[
                            position : position + len(true_hyphenated_word)
                        ]
                        label = label.replace(
                            true_hyphenated_word_with_possible_capitalization,
                            f"{{word{len(hyphenated_words)}}}",
                        )
                        hyphenated_words.append(
                            true_hyphenated_word_with_possible_capitalization
                        )
                new_labels.append(label)

            # We update the current labels with the new labels
            # that are now wrapped to avoid to remove hyphenated words.
            string_labels = new_labels

        string_labels = [
            targets_to_spaces(label, replace_with_spaces) for label in string_labels
        ]

        string_labels = clear_spaces(string_labels)

        # We now need to restore the hyphenated words which we have
        # previously wrapped, if we have done so.
        if need_to_run_hyphenation_check:
            restored_labels = []
            for label in string_labels:
                for number, hyphenated_word in enumerate(hyphenated_words):
                    label = label.replace(f"{{word{number}}}", hyphenated_word)
                restored_labels.append(label)
            string_labels = restored_labels

        if soft_capitalization:
            string_labels = apply_soft_capitalization(string_labels)

        if upper_case_consonants_clusters:
            string_labels = [consonants_to_upper(label) for label in string_labels]

    if single_label:
        return string_labels[0]
    return string_labels
