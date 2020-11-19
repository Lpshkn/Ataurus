"""
Module represents a class that will process data to extract a vector of features from it.
"""
import pandas as pd
import features.functions as funcs
import tqdm
from preparing.preparator import Preparator


class FeaturesExtractor:
    def __init__(self, preparator: Preparator):
        if not isinstance(preparator, Preparator):
            raise TypeError("The preparator's instance isn't Preparator.")

        self._preparator = preparator
        self._features = None
        self._tokens = None
        self._sentences = None

    def fit(self,
            avg_len_words=True,
            avg_len_sentences=True,
            pos_distribution=True,
            foreign_words_ratio=True,
            vocabulary_richness=True):
        """
        Extractor iterates for each text and extracts features like a dict.
        Returns a DataFrame object with columns such as authors and features.
        :param avg_len_words: an average length of tokens
        :param avg_len_sentences: an average length of sentences
        :param pos_distribution: distribution of part of speech
        :param foreign_words_ratio: foreign words / all words ratio
        :param vocabulary_richness: vocabulary richness
        :return: DataFrame object with columns 'Authors' and list of features
        """
        all_tokens = self._preparator.tokens()
        all_sentences = self._preparator.sentences(lower=True, delete_punctuations=True)

        all_features = []
        print('Begin fitting on the train data...')
        for tokens, sentences, author in tqdm.tqdm(list(zip(all_tokens, all_sentences, self._preparator.authors))):
            if not tokens or not sentences:
                continue

            features = {}

            foreign_ratio = funcs.foreign_words_ratio(tokens)
            # Check if it's an English article, we can't process it
            if foreign_ratio >= 0.6:
                continue
            if foreign_words_ratio:
                features['foreign_words_ratio'] = foreign_ratio

            if avg_len_words:
                features['avg_len_words'] = funcs.avg_len_words(tokens)
            if avg_len_sentences:
                features['avg_len_sentences'] = funcs.avg_len_sentences(sentences)
            if pos_distribution:
                features.update(funcs.pos_distribution(tokens))
            if vocabulary_richness:
                features['vocabulary_richness'] = funcs.vocabulary_richness(tokens)

            features['author'] = author
            all_features.append(features)

        if not all_features:
            raise ValueError("No features were extracted during fitting of FeaturesExtractor")

        self._features = pd.DataFrame(all_features)

    @property
    def features(self) -> pd.DataFrame:
        if self._features is None:
            raise ValueError("The list of features is None, the extractor wasn't fitted")
        return self._features

