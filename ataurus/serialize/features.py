import pandas as pd
import joblib
import os


def serialize_features(features: pd.DataFrame, filename: str):
    """
    Serializes a DataFrame object containing extracted features.

    :param features: extracted features
    :param filename: file where features will be serialized to
    """
    if type(features) != pd.DataFrame:
        raise ValueError("Serializing features don't represent a DataFrame object")

    with open(filename, 'wb') as file:
        joblib.dump(features, file)


def deserialize_features(filename: str):
    """
    Deserializes a DataFrame object containing extracted features.

    :param filename: file where features will be deserialized from
    """
    if not os.path.exists(filename):
        raise FileNotFoundError("Specified file for deserializing doesn't exist")

    with open(filename, 'wb') as file:
        df = joblib.load(filename)

    if type(df) != pd.DataFrame:
        raise TypeError("Deserialized object isn't pd.DataFrame")

    return df
