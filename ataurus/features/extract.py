"""
Module represents a class that will process data to extract a matrix of features from it.
"""
import numpy as np
import pandas as pd
import ataurus.features.functions as funcs
from sklearn.base import BaseEstimator, TransformerMixin
from ataurus.preparing.preprocessor import Preprocessor
from joblib.parallel import Parallel, delayed
from ataurus.features.features import (AVG_WORDS, AVG_SENTENCES, POS_DISTRIBUTION, PUNCTUATIONS_DISTRIBUTION,
                                       LEXICON_SIZE, FOREIGN_RATIO)


class FeaturesExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, n_jobs=1, verbose=True):
        """
        Extractor of features matrix. All parameters are flags that specify to include a result of processing
        of each method to the final result.
        """
        self.n_jobs = n_jobs
        self.verbose = verbose

    def fit(self, X, y=None):
        return self

    def transform(self, X) -> pd.DataFrame:
        # If at least one attribute doesn't exist, this specifies the fit method wasn't called
        # and all the retrieves must be executed
        texts, tokens, sentences = self._retrieve_lists(X)

        if self.verbose:
            print("Extracting features is beginning...")

        result = self._extract(texts, tokens, sentences, n_jobs=self.n_jobs)

        if self.verbose:
            print("Extracting features completed", end='\n\n')

        return result

    @staticmethod
    def _extract(texts: list[str], tokens: list[list[str]], sentences: list[list[str]], /,
                 avg_words=True, avg_sentences=True, pos_distribution=True,
                 foreign_words_ratio=True, lexicon=True, punctuation_distribution=True,
                 n_jobs=1) -> pd.DataFrame:
        """
        Returns DataFrame object contains extracted features with column names such as <feature_name>_<n>.
        """
        def process(function, objects: list, feature_name: str):
            result_ = np.vstack(Parallel(n_jobs)(delayed(function)(objects_) for objects_ in objects))

            # Build a list of the column names to create a features DataFrame
            n_columns = result_.shape[1]
            columns_name = [feature_name + f'_{i}' for i in range(1, n_columns + 1)]

            return pd.DataFrame(result_, columns=columns_name)

        results = []
        # Average length of words
        if avg_words:
            results.append(process(funcs.avg_length, tokens, AVG_WORDS))
        # Average length of sentences
        if avg_sentences:
            results.append(process(funcs.avg_length, sentences, AVG_SENTENCES))
        # POS distribution
        if pos_distribution:
            results.append(process(funcs.pos_distribution, tokens, POS_DISTRIBUTION))
        # Lexicon size
        if lexicon:
            results.append(process(funcs.lexicon, tokens, LEXICON_SIZE))
        # Foreign words ratio
        if foreign_words_ratio:
            results.append(process(funcs.foreign_words_ratio, tokens, FOREIGN_RATIO))
        # Punctuations distribution
        if punctuation_distribution:
            results.append(process(funcs.punctuations_distribution, texts, PUNCTUATIONS_DISTRIBUTION))

        if not results:
            raise ValueError("At least one feature must be chosen")

        return pd.concat(results, axis=1)

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
