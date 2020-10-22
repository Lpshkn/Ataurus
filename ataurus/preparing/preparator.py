"""
This module contains Preparator class that will prepare the data in DataFrame object.
All unnecessary symbols, stop words and other incorrect symbols will be removed from the text.
"""

import pandas as pd
import re
from razdel import tokenize, sentenize
from .rules import PUNCTUATIONS


class Preparator:
    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("The data isn't instance of pd.DataFrame")
        self._data = data

        try:
            self._texts = self.data['text'].to_numpy()
        except KeyError:
            raise KeyError("The input data in .csv format hasn't 'text' column, please fix your file")

    @property
    def data(self):
        """
        It's unprocessed data, necessary if a programmer will want to process the source data himself.
        """
        return self._data

    def tokens(self, index: int, lower=True, delete_punctuations=True) -> list:
        """
        Get a list of tokens from the text received by the index from the DataFrame.

        :param index: index of a text of the DataFrame that you want to process
        :param lower: to lower a result
        :param delete_punctuations: delete all punctuations from a result
        :return: list - the list of tokens
        """
        text = self._texts[index]
        if not isinstance(text, str):
            raise TypeError("Text value is not string")

        if lower:
            text = text.lower()

        text = re.sub(r'[\s]+', r' ', text).strip()

        if delete_punctuations:
            tokens = [token.text for token in tokenize(text) if not PUNCTUATIONS.search(token.text)]
        else:
            tokens = [token.text for token in tokenize(text)]
        return tokens

    def sentences(self, index: int, lower=False, delete_punctuations=True) -> list:
        """
        Get a list of sentences from the text received by the index from the DataFrame.

        :param index: index of a text of the DataFrame that you want to process
        :param lower: to lower a result
        :param delete_punctuations: delete all punctuations from a result
        :return: list - the list of sentences
        """
        text = self._texts[index]
        if not isinstance(text, str):
            raise TypeError("Text value is not string")

        if lower:
            sentences = [sentence.text.lower() for sentence in sentenize(text)]
        else:
            sentences = [sentence.text for sentence in sentenize(text)]

        if delete_punctuations:
            sentences = [PUNCTUATIONS.sub(" ", sentence) for sentence in sentences]

        return sentences
