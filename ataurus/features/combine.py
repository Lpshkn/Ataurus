import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from features.extract import FeaturesExtractor
from features.features import (AVG_WORDS, AVG_SENTENCES, POS_DISTRIBUTION, PUNCTUATIONS_DISTRIBUTION,
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

        result = []

        # If a features matrix wasn't prepared, extract tokens, sentences from texts and extract features
        if not self.X_extracted_:
            texts, tokens, sentences = FeaturesExtractor._retrieve_lists(X)

            features_dict = dict()
            for feature_name in FEATURES_DESCRIPTION.keys():
                features_dict[feature_name] = True if feature_name in self.features_names_ else False

            X = FeaturesExtractor._extract(texts, tokens, sentences, n_jobs=self.n_jobs, **features_dict)

        for feature_name in self.features_names_:
            # Get columns corresponding the name of selecting feature
            values = X.loc[:, X.columns.str.startswith(feature_name)].values
            result.append(values)
        result = np.hstack(result)

        if self.verbose:
            print("Extracting features completed", end='\n\n')

        return result
