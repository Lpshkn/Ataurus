"""
Module represents a class that will process data to extract a vector of features from it.
"""
from preparing.preparator import Preparator


class FeaturesExtractor:
    def __init__(self, preparator: Preparator):
        if not isinstance(preparator, Preparator):
            raise TypeError("The preparator's instance isn't Preparator.")

        self._preparator = preparator
        self._features = None
        self._tokens = None
        self._sentences = None

    def fit(self):
        pass

    @property
    def features(self):
        return self._features

    @staticmethod
    def _avg_len_words(tokens: list):
        return sum(len(token) for token in tokens) / len(tokens)

    @staticmethod
    def _avg_len_sentences(sentences: list):
        return sum(len(sentence) for sentence in sentences) / len(sentences)
