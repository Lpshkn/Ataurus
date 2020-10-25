"""
Module represents a class that will process data to extract a vector of features from it.
"""
from preparing.preparator import Preparator


class FeaturesExtractor:
    def __init__(self, preparator: Preparator):
        if not isinstance(preparator, Preparator):
            raise TypeError("The preparator's instance isn't Preparator.")

        self._preparator = preparator
        self._features = None

    def fit(self):
        pass

    @property
    def features(self):
        return self._features
