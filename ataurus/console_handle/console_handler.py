"""
This module represents functions for options of the command line.
Also module implements a class containing information about the project and all the information that
will be printed in the command line.
"""
import os
import re
import argparse
import pickle
import pandas as pd
import json
import joblib
from database.client import Database
from features.extract import FeaturesExtractor
from .utils import (MODEL_FILE, CACHE_DIRECTORY, CACHE_CFG_FILE, convert_to_cache_name,
                    convert_from_cache_name, get_hash)


class ConsoleHandler:
    NAME = 'ataurus'
    DESCRIPTION = 'Ataurus = Attribution of Authorship Russian. ' \
                  'This program receives texts with their authors, fit a model on that data and serializes ' \
                  'the fitted model in an output file. Ataurus allows to predict authors of unknown texts.'
    EPILOG = 'LPSHKN, 2020'

    def __init__(self, args):
        self._parser = self._get_parser(ConsoleHandler.NAME, ConsoleHandler.DESCRIPTION, ConsoleHandler.EPILOG)

        self._cache = None
        # Get parameters from the arguments received from the command line
        self._parameters = self._get_parameters(args)

    @staticmethod
    def _get_parser(program_name: str = None, description: str = None, epilog: str = None) -> argparse.ArgumentParser:
        """
        Method creates the instance of the ArgumentParser class, adds arguments in here and returns that instance.
        :param program_name: name of the program
        :param description: description of the program
        :param epilog: epilog of the program
        :return: an instance of the ArgumentParser class
        """
        parser = argparse.ArgumentParser(prog=program_name, description=description, epilog=epilog)
        modes = parser.add_subparsers(title='Modes', dest='mode')

        # Train mode
        train = modes.add_parser('train',
                                 help='mode for training a model using special parameters')
        train.add_argument('input',
                           help="it should be .csv file, containing 'author, text' columns or an ElasticSearch "
                                "config file .cfg, containing the hostname and the port, or it should be string "
                                "such as 'hostname:port/index_name', or it may be serialized DataFrame object, "
                                "containing extracted features",
                           type=str)
        train.add_argument('-o', '--output',
                           help="the name of a file where a model will be serialized",
                           default=MODEL_FILE,
                           type=str)

        # Predict mode
        predict = modes.add_parser('predict',
                                   help='make predictions')
        predict.add_argument('input',
                             help="it should be .csv file, containing 'author, text' columns or an ElasticSearch "
                                  "config file .cfg, containing the hostname and the port, or it should be string "
                                  "such as 'hostname:port/index_name', or it may be serialized DataFrame object, "
                                  "containing extracted features",
                             type=str)
        predict.add_argument('-m', '--model',
                             help='the name of a file containing a serialized model',
                             default=MODEL_FILE,
                             type=str)
        return parser

    def _get_parameters(self, args):
        """
        This method gets all parameters from the args of the command line.
        :param args: list of the arguments of the command line
        :return: parsed arguments
        """
        parameters = self._parser.parse_args(args)

        if parameters.mode is None:
            self._parser.error("You must specify 1 of 2 commands: train or predict")

        return parameters

    @staticmethod
    def _initialize_directories():
        """
        Create the directories for config files.
        """
        if not os.path.exists(CACHE_DIRECTORY):
            os.makedirs(CACHE_DIRECTORY)

    def _initialize_cache(self):
        """
        Method initialize the config cache file containing information about filenames and its cache.
        If there are some troubles with matching the names of files and files in .cache directory,
        this method will remove these values and files.
        """
        if not os.path.exists(CACHE_CFG_FILE):
            self._cache = {}
            for filename in os.listdir(CACHE_DIRECTORY):
                os.remove(os.path.join(CACHE_DIRECTORY, filename))
        else:
            with open(CACHE_CFG_FILE, 'r') as file:
                self._cache = json.load(file)

            filenames = set(self._cache.keys())
            cache_filenames = set(os.listdir(CACHE_DIRECTORY))

            # Delete lost keys from the dict
            for filename in filenames:
                cache_filename = convert_to_cache_name(filename)

                # If file wasn't found in the .cache directory, remove it from the dict
                if cache_filename not in cache_filenames:
                    del self._cache[filename]

            # Delete lost files in the .cache directory
            for cache_filename in cache_filenames:
                filename = convert_from_cache_name(cache_filename)

                if filename not in filenames:
                    os.remove(os.path.join(CACHE_DIRECTORY, filename))

    @property
    def mode(self) -> str:
        return self._parameters.mode

    @property
    def input(self):
        file = self._parameters.input

        # The input file must be csv format because of it will provide safe operations with data
        if not re.search(r'\.csv$', file.name):
            file.close()
            raise ValueError("The input file isn't csv format")

        try:
            df = pd.read_csv(file)
        except UnicodeDecodeError:
            file.close()
            raise ValueError("Data in the input file isn't UTF-8 encoding")

        # Attempt of getting cached data from the special directory
        basename = os.path.basename(file.name)
        if basename in self._cache:
            if self._cache[basename] == get_hash(file.name):
                with open(os.path.join(CACHE_DIRECTORY, convert_to_cache_name(basename)), 'rb') as file:
                    extractor = pickle.load(file)
                    if isinstance(extractor, FeaturesExtractor):
                        return extractor

        return df

    @property
    def model(self):
        if not ('model' in self._parameters):
            raise ValueError('You try to get a model, but this option is None')

        with open(self._parameters.model, 'rb') as file:
            return pickle.load(file)

    @property
    def output_file(self):
        if not ('output' in self._parameters):
            raise ValueError('You try to get output filename to save a model, but this option is None')
        output = self._parameters.output
        parent_path = os.path.dirname(output)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)

        return output

    def to_cache(self, extractor: FeaturesExtractor):
        """
        Dumps an instance of the FeaturesExtractor to the cache directory.

        :param extractor: an instance of FeaturesExtractor
        """
        if not isinstance(extractor, FeaturesExtractor):
            raise TypeError("You're trying to cache not FeatureExtractor's instance")

        filename = self._parameters.input.name
        basename = os.path.basename(filename)
        self._cache[basename] = get_hash(filename)

        cache_filename = convert_to_cache_name(filename)
        with open(os.path.join(CACHE_DIRECTORY, cache_filename), 'wb') as file:
            pickle.dump(extractor, file)

        with open(CACHE_CFG_FILE, 'w') as file:
            json.dump(self._cache, file, indent=4)
