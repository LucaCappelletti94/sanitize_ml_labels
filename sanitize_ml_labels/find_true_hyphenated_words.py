"""Submodule providing functions to identify true hyphenated words from the english language."""
from typing import List
import compress_json


def find_true_hyphenated_words(
    lowercase_label: str
) -> List[str]:
    """Returns list of true english hyphenated words in given label, sorted by decreasing length.

    Parameters
    --------------------
    lowercase_label: str
        The label to be parsed, expected to be in lowercase.

    Authorship
    --------------------
    This function was authored by Tommaso Fontana.
    You can see [his GitHub profile here](https://github.com/zommiommy)
    """
    stack = []
    result = []
    words_index = compress_json.local_load(
        "hyphenated_words_index.json.gz",
        use_cache=True
    )

    for char in lowercase_label:
        new_stack = []
        for word, substr in stack:
            if substr == "":
                result.append(word)
            elif substr[0] == char:
                new_stack.append((word, substr[1:]))

        new_stack.extend(
            words_index.get(char, [])
        )

        stack = new_stack
    
    for word, substr in stack:
        if substr == "":
            result.append(word)

    return sorted(
        result,
        key=lambda word: len(word),
        reverse=True
    )
