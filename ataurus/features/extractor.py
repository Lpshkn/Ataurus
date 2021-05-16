"""
Module represents a class that will process data to extract a matrix of features from it.
"""
import numpy as np
import ataurus.features.functions as funcs
import warnings
from sklearn.base import BaseEstimator, TransformerMixin
from ataurus.preparing.preprocessor import Preprocessor
from ataurus.features.features import FEATURES
from joblib.parallel import Parallel, delayed


class FeaturesExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, avg_words=True, avg_sentences=True, pos_distribution=True,
                 foreign_words_ratio=True, lexicon=True, punctuation_distribution=True,
                 n_jobs=1, verbose=True):
        """
        Extractor of features matrix. All parameters are flags that specify to include a result of processing
        of each method to the final result.

        :param avg_words: an average length of all words
        :param avg_sentences: an average length of all sentences
        :param pos_distribution: a part of speech distribution
        :param foreign_words_ratio: ratio of foreign words count / count of all words
        :param lexicon: a lexicon size
        :param punctuation_distribution: a distribution of punctuation symbols
        """
        self.avg_words = avg_words
        self.avg_sentences = avg_sentences
        self.pos_distribution = pos_distribution
        self.foreign_words_ratio = foreign_words_ratio
        self.lexicon = lexicon
        self.punctuation_distribution = punctuation_distribution
        self.n_jobs = n_jobs
        self.verbose = verbose

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # If at least one attribute doesn't exist, this specifies the fit method wasn't called
        # and all the retrieves must be executed
        texts, tokens, sentences = self._retrieve_lists(X)

        if self.verbose:
            features = [param for param, flag in self.get_params().items()
                        if flag and param not in ['n_jobs', 'verbose']]
            print("Extracting features is beginning with follow features:")
            for feature in features:
                print(f'\t- {FEATURES[feature]}')

        def process(function, objects):
            result_ = Parallel(n_jobs=self.n_jobs)(delayed(function)(objects_) for objects_ in objects)
            return np.vstack(result_)

        result = None
        if self.avg_words:
            aw_result = process(funcs.avg_length, tokens)
            result = np.hstack((result, aw_result)) if result is not None \
                else aw_result
        if self.avg_sentences:
            as_result = process(funcs.avg_length, sentences)
            result = np.hstack((result, as_result)) if result is not None \
                else as_result
        if self.pos_distribution:
            pos_result = process(funcs.pos_distribution, tokens)
            result = np.hstack((result, pos_result)) if result is not None \
                else pos_result
        if self.lexicon:
            lexicon_result = process(funcs.lexicon, tokens)
            result = np.hstack((result, lexicon_result)) if result is not None \
                else lexicon_result
        if self.foreign_words_ratio:
            fw_result = process(funcs.foreign_words_ratio, tokens)
            result = np.hstack((result, fw_result)) if result is not None \
                else fw_result
        if self.punctuation_distribution:
            puncs_result = process(funcs.punctuations_distribution, texts)
            result = np.hstack((result, puncs_result)) if result is not None \
                else puncs_result

        if result is None:
            warnings.warn("You shouldn't make all the parameters None, because this case can't be processed. The "
                          "average length of words will be set True automatically.")
            result = funcs.avg_length(tokens)

        if self.verbose:
            print("Extracting features completed", end='\n\n')

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
