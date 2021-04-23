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
POS = list(pymorphy2.MorphAnalyzer().TagClass.PARTS_OF_SPEECH)

# Compiled regex for foreign words
FOREIGN_WORD = re.compile(r"\b[^\s\d\Wа-яА-ЯёЁ_]+\b", re.IGNORECASE)


def avg_length(items: list[list[str]]) -> np.ndarray:
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


def pos_distribution(tokens: list[list[str]]) -> np.ndarray:
    """Feature №8. Part of speech distribution."""
    morph = pymorphy2.MorphAnalyzer()

    # The final matrix of distributions
    result = []

    # tokens_ - a list of tokens of one text in a list of texts
    for tokens_ in tokens:
        # result_ - a list of POS of one text in a list of texts
        result_ = []
        # Get a list of POS of a passed text
        pos_tokens = list(pos for pos in map(lambda x: morph.parse(x)[0].tag.POS, tokens_) if pos is not None)
        counter = Counter(pos_tokens)
        all_count = sum(counter.values())

        # Make a list of distributions using predefined pymorphy2 POS labels. If a POS label isn't in Counter, put 0
        for pos in POS:
            result_.append(counter.get(pos, 0) / all_count)
        result.append(result_)

    return np.array(result)


def foreign_words_ratio(tokens: list):
    """Feature №15. Foreign words / all words ratio."""
    result = []

    for tokens_ in tokens:
        result.append(len(list(filter(FOREIGN_WORD.search, tokens_)))/len(tokens_))

    return np.array(result).reshape(-1, 1)


def vocabulary_richness(tokens: list[list[str]]) -> np.ndarray:
    """Feature №17. Vocabulary richness."""
    result = []

    for tokens_ in tokens:
        result.append(len(np.unique(tokens_)) / len(tokens_))

    return np.array(result).reshape(-1, 1)


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
