"""
This module contains functions to extract features from a list of tokens/sentences.
"""
import pymorphy2
import re
import numpy as np
from collections import Counter
from preparing.rules import PUNCTUATIONS
from razdel.segmenters.punct import BRACKETS, QUOTES, SMILES

DEFINITIVE_PUNCTS = re.compile(r"(\.{3})|(\?!)|(\?\.{2,3})|(!\.{2,3})|(!!!)|([….?!])")
DIVIDING_PUNCTS = re.compile(r"[,;:‑–—−-]")
HIGHLIGHT_PUNCTS = re.compile(rf'[{BRACKETS}{QUOTES}]')
SMILES_PUNCTS = re.compile(SMILES)
DIGITS_PUNCTS = re.compile(r"[+$/*%^]")

# Predefined parts of speech
POS = list(pymorphy2.MorphAnalyzer().TagClass.PARTS_OF_SPEECH)
PUNCTS_NAMES = ["definitive_puncts", "dividing_puncts", "highlight_puncts", "smiles_puncts", "digits_puncts"]

# Compiled regex for foreign words
FOREIGN_WORD = re.compile(r"\b[^\s\d\Wа-яА-ЯёЁ_]+\b", re.IGNORECASE)


def avg_length(items: list[str]) -> np.ndarray:
    """
    Function to get average length of tokens and sentences.

    :param items: a list of lists of tokens/sentences
    :return: a list of average lengths of tokens/sentences
    """
    result = []
    if not items:
        result.append(np.nan)
    else:
        result.append(sum(map(len, items)) / len(items))

    return np.array(result)


def pos_distribution(tokens: list[str]) -> np.ndarray:
    """Feature №8. Part of speech distribution."""
    morph = pymorphy2.MorphAnalyzer()

    # Vector of distributions
    result = []

    # Get a list of POS of a passed text
    pos_tokens = list(pos for pos in map(lambda x: morph.parse(x)[0].tag.POS, tokens) if pos is not None)
    counter = Counter(pos_tokens)
    all_count = sum(counter.values())

    # Make a list of distributions using predefined pymorphy2 POS labels. If a POS label isn't in Counter, put 0
    for pos in POS:
        if all_count:
            result.append(counter.get(pos, 0) / all_count)
        else:
            result.append(np.nan)

    return np.array(result)


def foreign_words_ratio(tokens: list[str]) -> np.ndarray:
    """Feature №15. Foreign words / all words ratio."""
    result = []

    if not tokens:
        result.append(np.nan)
    else:
        result.append(len(list(filter(FOREIGN_WORD.search, tokens)))/len(tokens))

    return np.array(result)


def lexicon(tokens: list[str]) -> np.ndarray:
    """Feature №17. Vocabulary richness."""
    result = []

    if not tokens:
        result.append(np.nan)
    else:
        result.append(len(np.unique(tokens)) / len(tokens))

    return np.array(result)


def punctuations_distribution(text: str):
    # Vector of distributions
    result = []

    all_count = len(PUNCTUATIONS.findall(text))
    rules = {
        "definitive_puncts": DEFINITIVE_PUNCTS,
        "dividing_puncts": DIVIDING_PUNCTS,
        "highlight_puncts": HIGHLIGHT_PUNCTS,
        "smiles_puncts": SMILES_PUNCTS,
        "digits_puncts": DIGITS_PUNCTS
    }

    for punct_name in PUNCTS_NAMES:
        if all_count:
            result.append(len(rules[punct_name].findall(text)) / all_count)
        else:
            result.append(np.nan)

    return np.array(result)
