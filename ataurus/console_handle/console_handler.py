"""
This module represents functions for options of the command line.
Also module implements a class containing information about the project and all the information that
will be printed in the command line.
"""
import os
import re
import argparse
import pandas as pd
from database.client import Database
from serialize.features import deserialize_features
from serialize.model import deserialize_model


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
                                "or it should be string such as 'hostname:port/index_name', "
                                "or it may be serialized DataFrame object, containing extracted features",
                           type=str)
        train.add_argument('-o', '--output',
                           help="the name of a file where a model will be serialized",
                           type=str)
        train.add_argument('-f', '--features',
                           help="where extracted features will be serialized",
                           type=str)

        # Predict mode
        predict = modes.add_parser('predict',
                                   help='make predictions')
        predict.add_argument('input',
                             help="it should be .csv file, containing 'author, text' columns or an ElasticSearch "
                                  "or it should be string such as 'hostname:port/index_name', "
                                  "or it may be serialized DataFrame object, containing extracted features",
                             type=str)
        predict.add_argument('model',
                             help='the name of a file containing a serialized model',
                             type=str)
        predict.add_argument('-f', '--features',
                             help="where extracted features will be serialized",
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

    @property
    def mode(self) -> str:
        return self._parameters.mode

    @property
    def features_path(self):
        if self._parameters.features:
            return self._parameters.features
        return None

    @property
    def input(self):
        # The input may be either an input file or a connection string
        if os.path.exists(self._parameters.input):
            # If the input file has csv format
            if re.search(r'\.csv$', self._parameters.input):
                df = pd.read_csv(self._parameters.input)

                try:
                    texts = df['text'].values
                    authors = df['author'].values
                except Exception:
                    raise ValueError('Your .csv input file has no correct format: '
                                     'it must have "text" and "author" columns')
                return texts, authors
            # If the input is DataFrame serialized object containing extracted features
            else:
                df = deserialize_features(self._parameters.input)
                return df

        # If the input is connection string of ElasticSearch such as <hostname:port/index>
        elif re.search(r'^[\w.-]+:[\d]{2,5}/[^\s]+$', self._parameters.input):
            hostname_port, index_name = self._parameters.input.strip().split('/')
            database = Database.connect([hostname_port])
            authors, texts = database.get_authors_texts(index_name, 'author_nickname', 'text')

            return texts, authors
        else:
            raise ValueError("The input is neither input file nor a connection string of ElasticSearch")

    @property
    def model(self):
        if not ('model' in self._parameters):
            raise ValueError('You try to get a model, but this option is None')

        return deserialize_model(self._parameters.model)

    @property
    def output(self):
        if self._parameters.output:
            return self._parameters.output
        return None
