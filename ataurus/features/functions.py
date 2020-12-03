"""
This module contains functions to extract features from a list of tokens/sentences.
"""
import pymorphy2
import re
from collections import Counter


# Predefined parts of speech
POS_FOREIGN = 'FRGN'
POS_NONE = 'NONE'
POS = list(pymorphy2.MorphAnalyzer().TagClass.PARTS_OF_SPEECH) + [POS_FOREIGN, POS_NONE]

# Compiled regex for foreign words
FOREIGN_WORD = re.compile(r"\b[^\s\d\Wа-яА-ЯёЁ_]+\b", re.IGNORECASE)


def avg_len_words(tokens: list):
    """Feature №10. Average length of words."""
    if not tokens:
        return None

    return sum(len(token) for token in tokens) / len(tokens)


def avg_len_sentences(sentences: list):
    """Feature №11. Average length of sentences."""
    if not sentences:
        return None

    return sum(len(sentence) for sentence in sentences) / len(sentences)


def pos_distribution(tokens: list) -> dict:
    """Feature №8. Part of speech distribution."""
    morph = pymorphy2.MorphAnalyzer()
    distribution = dict.fromkeys(POS, 0)

    for token in tokens:
        pos = morph.parse(token)[0].tag.POS
        if pos in distribution:
            distribution[pos] += 1
        # If the word is foreign
        elif FOREIGN_WORD.search(token):
            distribution[POS_FOREIGN] += 1
        # If the pos can't be determined
        else:
            distribution[POS_NONE] += 1

    summary = sum(distribution.values())
    distribution = {first: second / summary for first, second in distribution.items()}

    return distribution


def foreign_words_ratio(tokens: list):
    """Feature №15. Foreign words / all words ratio."""
    if not tokens:
        return None

    foreign = [token for token in tokens if FOREIGN_WORD.search(token)]
    return len(foreign) / len(tokens)


def vocabulary_richness(tokens: list):
    """Feature №17. Vocabulary richness."""
    if not tokens:
        return None

    morph = pymorphy2.MorphAnalyzer()
    normal_tokens = []
    for token in tokens:
        normal_tokens.append(morph.parse(token)[0].normal_form)
    counter = Counter(normal_tokens)
    return len(counter) / len(tokens)