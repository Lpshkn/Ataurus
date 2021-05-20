import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from ataurus.features.extract import FeaturesExtractor
from ataurus.features.features import (AVG_WORDS, AVG_SENTENCES, POS_DISTRIBUTION, PUNCTUATIONS_DISTRIBUTION,
                                       LEXICON_SIZE, FOREIGN_RATIO, FEATURES_DESCRIPTION)


class FeaturesCombiner(BaseEstimator, TransformerMixin):
    def __init__(self, avg_words=True, avg_sentences=True, pos_distribution=True,
                 foreign_words_ratio=True, lexicon=True, punctuation_distribution=True,
                 n_jobs=1, verbose=False):
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
        # Check either input matrix is extracted features or just input texts and they should be processed
        if type(X) == pd.DataFrame:
            self.X_extracted_ = True
        else:
            self.X_extracted_ = False

        # Create a list of names of extracting features
        self.features_names_ = []
        if self.avg_words:
            self.features_names_.append(AVG_WORDS)
        if self.avg_sentences:
            self.features_names_.append(AVG_SENTENCES)
        if self.pos_distribution:
            self.features_names_.append(POS_DISTRIBUTION)
        if self.foreign_words_ratio:
            self.features_names_.append(FOREIGN_RATIO)
        if self.lexicon:
            self.features_names_.append(LEXICON_SIZE)
        if self.punctuation_distribution:
            self.features_names_.append(PUNCTUATIONS_DISTRIBUTION)

        return self

    def transform(self, X):
        if self.verbose:
            print("Extracting features is beginning with follow features:")
            for feature_name in self.features_names_:
                print(f'\t- {FEATURES_DESCRIPTION[feature_name]}')

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
