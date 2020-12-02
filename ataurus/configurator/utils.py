"""
Module contains important constants and functions for the Configurator module.
"""

import os
import hashlib as hl


CONFIG_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(os.path.curdir)), '.config')
MODEL_FILE = os.path.join(CONFIG_DIRECTORY, 'model.pickle')
CACHE_CFG_FILE = os.path.join(CONFIG_DIRECTORY, 'cache_cfg.json')

CACHE_DIRECTORY = os.path.join(CONFIG_DIRECTORY, '.cache')
POSTFIX_CACHE_FEATURES = '_features'


def convert_to_cache_name(filename: str, extension=None):
    """
    Convert from the filename to the filename that will be in .cache directory.

    :param filename: the name of a file
    :param extension: this extension will be set to the filename as result of this function
    :return: the name of the cache file
    """
    name, _extension = os.path.basename(filename).rsplit('.', 1)

    if not extension:
        extension = _extension

    cache_filename = name + POSTFIX_CACHE_FEATURES + '.' + extension
    return cache_filename


def convert_from_cache_name(cache_filename: str, extension=None):
    """
    Convert from the filename of the cache file to the original filename.

    :param cache_filename: the name of a cache file
    :param extension: this extension will be set to the filename as result of this function
    :return: the name of the original file
    """
    name, _extension = os.path.basename(cache_filename).rsplit('.', 1)

    if not extension:
        extension = _extension

    name = name.rsplit(POSTFIX_CACHE_FEATURES, 1)[0]
    filename = name + '.' + extension
    return filename


def get_hash(filename: str) -> str:
    """
    Get the hash of the passed file.
    :param filename: the name of a file
    :return: hash string
    """
    sha = hl.sha256()
    with open(filename, 'rb') as file:
        data = file.read()
        sha.update(data)

    return sha.hexdigest()
