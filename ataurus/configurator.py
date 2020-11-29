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


CONFIG_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(os.path.curdir)), '.config')
MODEL_FILE = 'model.pickle'
FEATURES_FILE = 'features.csv'
CACHE_DIRECTORY = os.path.join(CONFIG_DIRECTORY, '.cache')


class Configurator:
    NAME = 'Ataurus'
    DESCRIPTION = 'Ataurus = Attribution of Authorship Russian. ' \
                  'This program collects data from the sites(optional), processes this data, ' \
                  'gets the parameter vector from the data and trains the model of machine learning to specify ' \
                  'the author of an unknown text.'
    EPILOG = 'LPSHKN, 2020'

    def __init__(self, args):
        self._parser = self._get_parser(Configurator.NAME, Configurator.DESCRIPTION, Configurator.EPILOG)

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
                          default=os.path.join(CONFIG_DIRECTORY, MODEL_FILE),
                          type=str)

        # Train mode
        train = subparsers.add_parser('train',
                                      help='train a model')
        train.add_argument('input',
                           help="the name of a .csv file containing train data",
                           type=argparse.FileType(mode='r', encoding='utf-8'))
        train.add_argument('-o', '--output',
                           help="the name of a file where a model will be saved",
                           default=os.path.join(CONFIG_DIRECTORY, MODEL_FILE),
                           type=str)

        # Predict mode
        predict = subparsers.add_parser('predict',
                                        help='make predictions')
        predict.add_argument('input',
                             help="the name of a .csv file containing data that you need to predict authors for",
                             type=argparse.FileType(mode='r', encoding='utf-8'))
        predict.add_argument('-m', '--model',
                             help='the name of a file containing a model',
                             default=os.path.join(CONFIG_DIRECTORY, MODEL_FILE),
                             type=str)
        return parser

    def _get_parameters(self, args):
        """
        This method gets all parameters from the args of the command line.
        :param args: list of the arguments of the command line
        :return: parsed arguments
        """
        parameters = self._parser.parse_args(args)

        if parameters.command == 'info':
            pass
        elif parameters.command == 'train':
            # At least one of the parameters must be specified
            if not parameters.input:
                self._parser.error('No data was passed, add -i/--input to pass a csv file')
        elif parameters.command == 'predict':
            pass

        # If no errors occurred, create config directories
        self._initialize_directories()

        return parameters

    @staticmethod
    def _initialize_directories():
        """
        Create the directories for config files.
        """
        if not os.path.exists(CACHE_DIRECTORY):
            os.makedirs(CACHE_DIRECTORY)

    @property
    def command(self) -> str:
        return self._parameters.command

    @property
    def input_data(self) -> pd.DataFrame:
        if not ('input' in self._parameters):
            raise ValueError('You try to get an input data, but this option is None')
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

        return df

    @property
    def model(self):
        if not ('model' in self._parameters):
            raise ValueError('You try to get a model, but this option is None')

        with open(self._parameters.model, 'rb') as file:
            return pickle.load(file)

    @property
    def features(self):
        if not ('features' in self._parameters):
            raise ValueError('You try to get features, but this option is None')

        filename = self._parameters.features
        if 'input' in self._parameters:
            return open(filename, 'w')
        else:
            if not re.search(r'\.csv$', filename):
                raise ValueError("The features file isn't csv format")

            try:
                df = pd.read_csv(filename)
            except UnicodeDecodeError:
                raise ValueError("Data in the input file isn't UTF-8 encoding")

            return df

    @property
    def output_file(self):
        if not ('output' in self._parameters):
            raise ValueError('You try to get output filename to save a model, but this option is None')
        output = self._parameters.output
        parent_path = os.path.dirname(output)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)

        return output
