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


def get_parts_file(filename: str, extension=None):
    """
    Gets the name, delimiter and extension from the filename.
    Delimiter may be empty or '.'.

    :param filename: original filename
    :param extension: extension that you want to set to this file
    :return: name, extension, delimiter
    """
    try:
        name, _extension = os.path.basename(filename).rsplit('.', 1)
        delimiter = '.'
    except ValueError:
        name = os.path.basename(filename)
        _extension = ''
        delimiter = ''

    if not extension:
        extension = _extension
    else:
        delimiter = '.'

    return name, extension, delimiter


def convert_to_cache_name(filename: str, extension=None):
    """
    Convert from the filename to the filename that will be in .cache directory.

    :param filename: the name of a file
    :param extension: this extension will be set to the filename as result of this function
    :return: the name of the cache file
    """
    name, extension, delimiter = get_parts_file(filename, extension)

    cache_filename = name + POSTFIX_CACHE_FEATURES + delimiter + extension
    return cache_filename


def convert_from_cache_name(cache_filename: str, extension=None):
    """
    Convert from the filename of the cache file to the original filename.

    :param cache_filename: the name of a cache file
    :param extension: this extension will be set to the filename as result of this function
    :return: the name of the original file
    """
    name, extension, delimiter = get_parts_file(cache_filename, extension)

    # Here ValueError may be occurred, if the name of cache file hasn't the postfix
    name = name.rsplit(POSTFIX_CACHE_FEATURES, 1)[0]

    filename = name + delimiter + extension
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
