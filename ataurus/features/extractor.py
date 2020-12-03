"""
Module represents a class that will process data to extract a vector of features from it.
"""
import numpy as np
import pandas as pd
import features.functions as funcs
import tqdm
import time
from sklearn.preprocessing import StandardScaler, LabelEncoder


class FeaturesExtractor:
    def __init__(self):
        self._features = None
        self._tokens = None
        self._sentences = None
        self._classes = None
        self._X = None
        self._y = None

    def fit(self,
            tokens,
            sentences,
            authors=None,
            avg_len_words=True,
            avg_len_sentences=True,
            pos_distribution=True,
            foreign_words_ratio=True,
            vocabulary_richness=True):
        """
        Extractor iterates for each text and extracts features like a dict.
        Returns a DataFrame object with columns such as authors and features.
        :param tokens: the tokens from the text
        :param sentences: the sentences from the text
        :param authors: a list of authors
        :param avg_len_words: an average length of tokens
        :param avg_len_sentences: an average length of sentences
        :param pos_distribution: distribution of part of speech
        :param foreign_words_ratio: foreign words / all words ratio
        :param vocabulary_richness: vocabulary richness
        :return: DataFrame object with columns 'Authors' and list of features
        """
        print('Begin extracting features from the data...')
        # Sleep for normal printing of message, because of a tqdm's message may be printed earlier than this message
        time.sleep(1)

        tokens = np.array(tokens)
        sentences = np.array(sentences)
        if authors is not None:
            authors = np.array(authors)

        all_features = []
        indexes = []
        for _tokens, _sentences in tqdm.tqdm(list(zip(tokens, sentences))):
            if not _tokens or not _sentences:
                indexes.append(False)
                continue

            features = {}

            foreign_ratio = funcs.foreign_words_ratio(_tokens)
            # Check if it's an English article, we can't process it
            if foreign_ratio >= 0.6:
                indexes.append(False)
                continue
            if foreign_words_ratio:
                features['foreign_words_ratio'] = foreign_ratio
            if avg_len_words:
                features['avg_len_words'] = funcs.avg_len_words(_tokens)
            if avg_len_sentences:
                features['avg_len_sentences'] = funcs.avg_len_sentences(_sentences)
            if pos_distribution:
                features.update(funcs.pos_distribution(_tokens))
            if vocabulary_richness:
                features['vocabulary_richness'] = funcs.vocabulary_richness(_tokens)

            indexes.append(True)
            all_features.append(features)

        if not all_features:
            raise ValueError("No features were extracted during fitting of FeaturesExtractor")

        all_features = pd.DataFrame(all_features)

        if any(authors):
            all_features['author'] = authors[indexes]
            X = StandardScaler().fit_transform(all_features.drop('author', axis=1))
            le = LabelEncoder()
            le.fit(all_features['author'])
            classes = le.classes_
            y = le.transform(all_features['author'])
        else:
            X = StandardScaler().fit_transform(all_features)
            y = None
            classes = None

        self._X = X
        self._y = y
        self._classes = classes
        self._features = pd.DataFrame(all_features)

        return self

    @property
    def features(self) -> pd.DataFrame:
        if self._features is None:
            raise ValueError("The list of features is None, the extractor wasn't fitted")
        return self._features

    @property
    def X(self) -> pd.DataFrame:
        if self._features is None:
            raise ValueError("The list of features is None, the extractor wasn't fitted")

        return self._X

    @property
    def y(self) -> pd.DataFrame:
        return self._y

    @property
    def classes(self) -> list:
        if self._features is None:
            raise ValueError("The list of features is None, the extractor wasn't fitted")

        return self._classes
