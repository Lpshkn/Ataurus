"""
This module contains functions to extract features from a list of tokens/sentences.
"""
import pymorphy2
import re
from collections import Counter


def avg_len_words(tokens: list):
    """Feature №10. Average length of words."""
    return sum(len(token) for token in tokens) / len(tokens)


def avg_len_sentences(sentences: list):
    """Feature №11. Average length of sentences."""
    return sum(len(sentence) for sentence in sentences) / len(sentences)


def pos_distribution(tokens: list) -> dict:
    """Feature №8. Part of speech distribution."""
    morph = pymorphy2.MorphAnalyzer()
    distribution = dict.fromkeys(list(morph.TagClass.PARTS_OF_SPEECH), 0)

    for token in tokens:
        pos = morph.parse(token)[0].tag.POS
        if pos in distribution:
            distribution[pos] += 1

    summary = sum(distribution.values())
    distribution = {first: second / summary for first, second in distribution.items()}

    return distribution


def foreign_words_ratio(tokens: list):
    """Feature №15. Foreign words / all words ratio."""
    foreign = [token for token in tokens if re.search(r"[^\s\d\Wа-яА-ЯёЁ]", token)]
    return len(foreign) / len(tokens)


def vocabulary_richness(tokens: list):
    """Feature №17. Vocabulary richness."""
    morph = pymorphy2.MorphAnalyzer()
    normal_tokens = []
    for token in tokens:
        normal_tokens.append(morph.parse(token)[0].normal_form)
    counter = Counter(normal_tokens)
    return len(counter) / len(tokens)