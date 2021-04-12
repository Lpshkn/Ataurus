"""
Module represents a class that will process data to extract a matrix of features from it.
"""
import numpy as np
import ataurus.features.functions as funcs
from sklearn.base import BaseEstimator, TransformerMixin
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
        """
        Retrieve lists of texts, tokens and sentences from np.ndarray X. The list of texts must be the first column,
        the list of tokens - the second column and sentences - the third column.

        If all the values in tokens or sentences are None, Extractor gets tokens or sentences from the list of texts
        using the Preprocessor class.

        Note, if both the list of tokens and sentences are None, the list of texts will be retrieved from
        the Preprocessor too, because of the Extractor guesses the passed texts are unprocessed.
        """
        self._retrieve_lists(X)
        return self

    def transform(self, X):
        # If at least one attribute doesn't exist, this specifies the fit method wasn't called
        # and all the retrieves must be executed
        if not hasattr(self, 'texts') or not hasattr(self, 'tokens') or not hasattr(self, 'sentences'):
            self._retrieve_lists(X)

        result = None
        if self.avg_words:
            result = np.hstack((result, funcs.avg_length(self.tokens))) if result is not None \
                else funcs.avg_length(self.tokens)
        if self.avg_sentences:
            result = np.hstack((result, funcs.avg_length(self.sentences))) if result is not None \
                else funcs.avg_length(self.sentences)

        return result

    def _retrieve_lists(self, X):
        """
        Makes all retrieves described in the fit method.
        """
        texts = X[:, 0]
        tokens = X[:, 1]
        sentences = X[:, 2]

        preprocessor = Preprocessor(texts)
        if not any(tokens) and not any(sentences):
            texts = preprocessor.texts()
            tokens = preprocessor.tokens()
            sentences = preprocessor.sentences()
        elif not any(tokens):
            tokens = preprocessor.tokens()
        elif not any(sentences):
            sentences = preprocessor.sentences()

        self.texts = texts
        self.tokens = tokens
        self.sentences = sentences
