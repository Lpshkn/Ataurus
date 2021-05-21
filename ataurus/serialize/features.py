import numpy as np
import pandas as pd
import joblib
import os


def serialize_features(features: pd.DataFrame, filename: str, authors: np.ndarray = None):
    """
    Serializes a DataFrame object containing extracted features and authors.

    :param features: extracted features
    :param authors: a list of authors
    :param filename: file where features will be serialized to
    """
    if type(features) != pd.DataFrame:
        raise ValueError("Serializing features don't represent a DataFrame object")

    # If y was passed, serialize it with features together
    serializing = features, authors if authors is not None else features
    joblib.dump(serializing, filename)


def deserialize_features(filename: str):
    """
    Deserializes a DataFrame object containing extracted features.

    :param filename: file where features will be deserialized from
    """
    if not os.path.exists(filename):
        raise FileNotFoundError("Specified file for deserializing doesn't exist")

    features, authors = None, None

    deserializing = joblib.load(filename)
    if type(deserializing) == tuple:
        try:
            features, authors = deserializing
        except ValueError:
            raise ValueError("Your deserializing file containing features isn't correct. It should contain either "
                             "DataFrame object or DataFrame object and numpy.ndarray")
    else:
        features = deserializing

    if type(features) != pd.DataFrame:
        raise TypeError("Deserialized object isn't pd.DataFrame")

    return features, authors if authors is not None else features
