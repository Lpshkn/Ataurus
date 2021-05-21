import pickle
import os
from sklearn.pipeline import Pipeline


def serialize_model(model: Pipeline, filename: str):
    """
    Serializes a model into the .pickle file.

    :param model: serializing model
    :param filename: the name of the file
    """
    if type(model) != Pipeline:
        raise ValueError("Serializing model isn't a Pipeline instance")

    with open(filename, 'wb') as file:
        pickle.dump(model, file)


def deserialize_model(filename: str) -> Pipeline:
    """
    Deserializes a model from a .pickle file.

    :param filename: the name of the file
    """
    if not os.path.exists(filename):
        raise FileNotFoundError("Specified file for deserializing doesn't exist")

    with open(filename, 'rb') as file:
        model = pickle.load(file)

    if type(model) != Pipeline:
        raise TypeError("Deserialized object isn't Pipeline")

    return model
