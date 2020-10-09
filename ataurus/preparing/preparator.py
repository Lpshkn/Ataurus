"""
This module contains Preparator class that will prepare the data in DataFrame object.
All unnecessary symbols, stop words and other incorrect symbols will be removed from the text.
"""

import pandas as pd
import numpy as np


class Preparator:
    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("The data isn't instance of pd.DataFrame")
        self._data = data
        self._tokens = None

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

    @property
    def tokens(self):
        if self._tokens is None:
            raise ValueError("Attempt to get tokens from unprocessed data")
        return self._tokens

