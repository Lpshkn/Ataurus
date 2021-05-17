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
from ataurus.features.extractor import FeaturesExtractor
from .utils import (MODEL_FILE, CACHE_DIRECTORY, CACHE_CFG_FILE, convert_to_cache_name,
                    convert_from_cache_name, get_hash)


class ConsoleHandler:
    NAME = 'ataurus'
    DESCRIPTION = 'Ataurus = Attribution of Authorship Russian. ' \
                  'This program collects data from the sites(optional), processes this data, ' \
                  'gets the parameter vector from the data and trains the model of machine learning to specify ' \
                  'the author of an unknown text.'
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
        subparsers = parser.add_subparsers(title='Commands', dest='command')

        # Info mode
        info = subparsers.add_parser('info',
                                     help='info mode to get more information about a model or additional settings')
        info.add_argument('-m', '--model',
                          help='the name of a file containing a model',
                          default=MODEL_FILE,
                          type=str)

        # Train mode
        train = subparsers.add_parser('train',
                                      help='train a model')
        train.add_argument('input',
                           help="the name of a .csv file containing train data",
                           type=argparse.FileType(mode='r', encoding='utf-8'))
        train.add_argument('-o', '--output',
                           help="the name of a file where a model will be saved",
                           default=MODEL_FILE,
                           type=str)

        # Predict mode
        predict = subparsers.add_parser('predict',
                                        help='make predictions')
        predict.add_argument('input',
                             help="the name of a .csv file containing data that you need to predict authors for",
                             type=argparse.FileType(mode='r', encoding='utf-8'))
        predict.add_argument('-m', '--model',
                             help='the name of a file containing a model',
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

        if parameters.command is None:
            self._parser.error("You must specify 1 of 3 commands: train, predict or info")

        # If no errors occurred, create config directories
        self._initialize_directories()
        # Load cfg file and check that files are contained in the .cache directory
        self._initialize_cache()

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
    def command(self) -> str:
        return self._parameters.command

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
