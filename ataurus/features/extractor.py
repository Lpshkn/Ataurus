"""
Module represents a class that will process data to extract a vector of features from it.
"""
import numpy as np
import pandas as pd
import ataurus.features.functions as funcs
import tqdm
import time
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, LabelEncoder
from ataurus.preparing.preprocessor import Preprocessor


class FeaturesExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, avg_words=True, avg_sentences=True, pos_distribution=True,
                 foreign_words_ratio=True, vocabulary_richness=True, punctuation_distribution=True):
        """
        Extractor of features matrix. All parameters are flags that specify to include a result of processing
        of each method to the final result.

        :param avg_words: an average length of all words
        :param avg_sentences: an average length of all sentences
        :param pos_distribution: a part of speech distribution
        :param foreign_words_ratio: ratio of foreign words count / count of all words
        :param vocabulary_richness: a lexicon size
        :param punctuation_distribution: a distribution of punctuation symbols
        """
        self.avg_words = avg_words
        self.avg_sentences = avg_sentences
        self.pos_distribution = pos_distribution
        self.foreign_words_ratio = foreign_words_ratio
        self.vocabulary_richness = vocabulary_richness
        self.punctuation_distribution = punctuation_distribution

    def fit(self, X, y=None):
        return self

    def transform(self, X: dict, y=None):
        tokens = X['tokens']
        sentences = X['sentences']
        texts = X['texts']

        if tokens is None:
            preprocessor = Preprocessor(texts)
            tokens = preprocessor.tokens()
        if sentences is None:
            preprocessor = Preprocessor(texts)
            sentences = preprocessor.sentences()

        result = None
        if self.avg_words:
            result = np.hstack((result, funcs.avg_length(tokens))) if result else funcs.avg_length(tokens)
        if self.avg_sentences:
            result = np.hstack((result, funcs.avg_length(sentences))) if result else funcs.avg_length(sentences)

        if y:
            le = LabelEncoder()
            le.fit(y)
            self._classes = le.classes_
            targets = le.transform(y)
            return result, targets
        else:
            return result

    @property
    def classes(self):
        if hasattr(self, '_classes'):
            return self._classes
        else:
            return None
