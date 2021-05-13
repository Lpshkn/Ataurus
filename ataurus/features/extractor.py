"""
Module represents a class that will process data to extract a matrix of features from it.
"""
import numpy as np
import ataurus.features.functions as funcs
import warnings
from sklearn.base import BaseEstimator, TransformerMixin
from ataurus.preparing.preprocessor import Preprocessor
from joblib.parallel import Parallel, delayed


class FeaturesExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, avg_words=True, avg_sentences=True, pos_distribution=True,
                 foreign_words_ratio=True, vocabulary_richness=True, punctuation_distribution=True,
                 n_jobs=-1, verbose=0):
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
        self.n_jobs = n_jobs
        self.verbose = verbose

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # If at least one attribute doesn't exist, this specifies the fit method wasn't called
        # and all the retrieves must be executed
        texts, tokens, sentences = self._retrieve_lists(X)

        result = None
        if self.avg_words:
            aw_result = Parallel(n_jobs=self.n_jobs)(delayed(funcs.avg_length)(tokens_) for tokens_ in tokens)
            result = np.hstack((result, np.vstack(aw_result))) if result is not None \
                else np.vstack(aw_result)
        if self.avg_sentences:
            as_result = Parallel(n_jobs=self.n_jobs)(delayed(funcs.avg_length)(sentences_) for sentences_ in sentences)
            result = np.hstack((result, np.vstack(as_result))) if result is not None \
                else np.vstack(as_result)
        if self.pos_distribution:
            pos_result = Parallel(n_jobs=self.n_jobs)(delayed(funcs.pos_distribution)(tokens_) for tokens_ in tokens)
            result = np.hstack((result, np.vstack(pos_result))) if result is not None \
                else np.vstack(pos_result)
        if self.vocabulary_richness:
            voc_result = Parallel(n_jobs=self.n_jobs)(delayed(funcs.vocabulary_richness)(tokens_) for tokens_ in tokens)
            result = np.hstack((result, np.vstack(voc_result))) if result is not None \
                else np.vstack(voc_result)
        if self.foreign_words_ratio:
            fw_result = Parallel(n_jobs=self.n_jobs)(delayed(funcs.foreign_words_ratio)(tokens_) for tokens_ in tokens)
            result = np.hstack((result, np.vstack(fw_result))) if result is not None \
                else np.vstack(fw_result)
        if self.punctuation_distribution:
            puncs_result = Parallel(n_jobs=self.n_jobs)(delayed(funcs.punctuations_distribution)(text) for text in texts)
            result = np.hstack((result, np.vstack(puncs_result))) if result is not None \
                else np.vstack(puncs_result)

        if result is None:
            warnings.warn("You shouldn't make all the parameters None, because this case can't be processed. The "
                          "average length of words will be set True automatically.")
            result = funcs.avg_length(tokens)

        return result

    @staticmethod
    def _retrieve_lists(X):
        """
        Retrieve lists of texts, tokens and sentences from np.ndarray X. The list of texts must be the first column,
        the list of tokens - the second column and sentences - the third column.

        If all the values in tokens or sentences are None, Extractor gets tokens or sentences from the list of texts
        using the Preprocessor class.

        Note, if both the list of tokens and sentences are None, the list of texts will be retrieved from
        the Preprocessor too, because of the Extractor guesses the passed texts are unprocessed.
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

        return texts, tokens, sentences
