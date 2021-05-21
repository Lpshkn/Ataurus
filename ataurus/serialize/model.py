import pickle
import os
from ml.model import Model


def serialize_model(model: Model, filename: str):
    """
    Serializes a model into the .pickle file.

    :param model: serializing model
    :param filename: the name of the file
    """
    if type(model) != Model:
        raise ValueError("Serializing model isn't a Model instance")

    with open(filename, 'wb') as file:
        pickle.dump(model, file)


def deserialize_model(filename: str) -> Model:
    """
    Deserializes a model from a .pickle file.

    :param filename: the name of the file
    """
    if not os.path.exists(filename):
        raise FileNotFoundError("Specified file for deserializing doesn't exist")

    with open(filename, 'rb') as file:
        model = pickle.load(file)

    if type(model) != Model:
        raise TypeError("Deserialized object isn't Model")

    return model
