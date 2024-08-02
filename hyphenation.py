"""Script to generate the index of hyphenated words."""

import os
import compress_json


def generate_hyphenated_words_index():
    """Generate the index of hyphenated words."""
    if os.path.exists("hyphenations.json"):
        compress_json.dump(
            sorted(compress_json.load("hyphenations.json")), "hyphenations.json.gz"
        )
        os.remove("hyphenations.json")

    index = {}
    for word in compress_json.load("hyphenations.json.gz"):
        word = word.lower()
        index.setdefault(word[0], []).append((word, word[1:]))

    compress_json.dump(index, "sanitize_ml_labels/hyphenated_words_index.json.gz")


if __name__ == "__main__":
    generate_hyphenated_words_index()
