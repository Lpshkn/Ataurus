"""
This module contains functions to extract features from a list of tokens/sentences.
"""
import pymorphy2
import re
import numpy as np
from collections import Counter
from ataurus.preparing.rules import PUNCTUATIONS
from razdel.segmenters.punct import BRACKETS, QUOTES, SMILES

DEFINITIVE_PUNCTS = re.compile(r"(...)|(\?!)|(\?\.{2,3})|(!\.{2,3})|(!!!)|([….?!])")
DIVIDING_PUNCTS = re.compile(r"[,;:‑–—−-]")
HIGHLIGHT_PUNCTS = re.compile(rf'[{BRACKETS}{QUOTES}]')
SMILES_PUNCTS = re.compile(SMILES)
DIGITS_PUNCTS = re.compile(r"[+$/*%^]")

# Predefined parts of speech
POS_FOREIGN = 'FRGN'
POS_NONE = 'NONE'
POS = list(pymorphy2.MorphAnalyzer().TagClass.PARTS_OF_SPEECH) + [POS_FOREIGN, POS_NONE]

# Compiled regex for foreign words
FOREIGN_WORD = re.compile(r"\b[^\s\d\Wа-яА-ЯёЁ_]+\b", re.IGNORECASE)


def avg_length(items: list[list[str]]):
    """
    Function to get average length of tokens and sentences.

    :param items: a list of lists of tokens/sentences
    :return: a list of average lengths of tokens/sentences
    """
    result = []
    for items_ in items:
        if not items_:
            result.append(np.nan)
        else:
            result.append(sum(map(len, items_)) / len(items_))

    return np.array(result).reshape(-1, 1)


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


def punctuations_distribution(text: str):
    columns = ["definitive_puncts", "dividing_puncts", "highlight_puncts", "smiles_puncts"]
    if not text:
        return dict.fromkeys(columns, 0)

    all_count = len(PUNCTUATIONS.findall(text))
    distribution = {
        "definitive_puncts": len(DEFINITIVE_PUNCTS.findall(text)) / all_count if all_count else 0,
        "dividing_puncts": len(DIVIDING_PUNCTS.findall(text)) / all_count if all_count else 0,
        "highlight_puncts": len(HIGHLIGHT_PUNCTS.findall(text)) / all_count if all_count else 0,
        "smiles_puncts": len(SMILES_PUNCTS.findall(text)) / all_count if all_count else 0,
        "digits_puncts": len(DIGITS_PUNCTS.findall(text)) / all_count if all_count else 0
    }
    return distribution
