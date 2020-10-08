"""
This module contains Preparator class that will prepare the data in DataFrame object.
All unnecessary symbols, stop words and other incorrect symbols will be removed from the text.
"""

import pandas as pd


class Preparator:
    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("The data isn't instance of pd.DataFrame")