"""
This module contains functions to extract features from a list of tokens/sentences.
"""


def avg_len_words(tokens: list):
    """Feature №10. Average length of words."""
    return sum(len(token) for token in tokens) / len(tokens)


def avg_len_sentences(sentences: list):
    """Feature №11. Average length of sentences."""
    return sum(len(sentence) for sentence in sentences) / len(sentences)