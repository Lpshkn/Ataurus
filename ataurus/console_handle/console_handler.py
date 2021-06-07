"""
This module represents functions for options of the command line.
Also module implements a class containing information about the project and all the information that
will be printed in the command line.
"""
import os
import re
import json
import argparse
import pandas as pd
from database.client import Database
from serialize.features import deserialize_features
from serialize.model import deserialize_model
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier


class ConsoleHandler:
    NAME = 'ataurus'
    DESCRIPTION = 'Ataurus = Attribution of Authorship Russian. ' \
                  'This program receives texts with their authors, fit a model on that data and serializes ' \
                  'the fitted model in an output file. Ataurus allows to predict authors of unknown texts.'
    EPILOG = 'LPSHKN, 2020'

    def __init__(self, args):
        self._parser = self._get_parser(ConsoleHandler.NAME, ConsoleHandler.DESCRIPTION, ConsoleHandler.EPILOG)

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
        train.add_argument('output',
                           help="the name of a file where a model will be serialized",
                           type=str)
        train.add_argument('-f', '--features',
                           help="where extracted features will be serialized",
                           type=str)
        train.add_argument('-c', '--train_config',
                           help="path to a config file containing parameters for a grid search "
                                "of parameters while training",
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

        # Parse mode
        parse = modes.add_parser('parse',
                                 help='parse web sites to get data')
        parse.add_argument('-m', '--max_count',
                           help='maximum articles by one author',
                           default=10 ** 10)
        parse.add_argument('--host',
                           help='the host address of the Elasticsearch cluster',
                           type=str)
        parse.add_argument('--port',
                           help='the port of the Elasticsearch cluster',
                           type=str)

        parse_resources = parse.add_subparsers(title='Resources', dest='resource')

        # Habr parsing mode
        habr_resource = parse_resources.add_parser('habr', help='Habr.com site')
        habr_resource.add_argument('authors',
                                   help="a list of authors represents a file or a string where authors "
                                        "separated by ','")
        habr_resource.add_argument('index',
                                   help='the name of an index of an ElasticSearch cluster where data will be loaded')

        habr_resource.add_argument('-o', '--output',
                                   help=".csv file where data will be loaded to")

        return parser

    def _get_parameters(self, args):
        """
        This method gets all parameters from the args of the command line.
        :param args: list of the arguments of the command line
        :return: parsed arguments
        """
        parameters = self._parser.parse_args(args)

        if parameters.mode is None:
            self._parser.error("You must specify 1 of 3 commands: train, predict or parse")
        if parameters.mode == 'parse':
            if parameters.resource is None:
                self._parser.error("You must specify 1 of 1 resources: habr")

        return parameters

    @property
    def mode(self) -> str:
        return self._parameters.mode

    @property
    def resource(self) -> str:
        return self._parameters.resource

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
            # If the input is DataFrame serialized object containing extracted features and a list of authors (optional)
            else:
                return deserialize_features(self._parameters.input)

        # If the input is connection string of ElasticSearch such as <hostname:port/index>
        elif re.search(r'^[\w.-]+:[\d]{2,5}/[^\s]+$', self._parameters.input):
            hostname_port, index_name = self._parameters.input.strip().split('/')
            database = Database.connect([hostname_port])
            authors, texts = database.get_authors_texts(index_name, 'author', 'text')

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

    @property
    def train_config(self):
        """
        Gets and returns a grid params for the GridSearchCV class to search optimal hyper parameters of a model.
        """
        if not self._parameters.train_config:
            return None

        if not os.path.exists(self._parameters.train_config):
            raise FileNotFoundError("The training config file wasn't found")

        with open(self._parameters.train_config, 'r') as file:
            json_parameters = json.load(file)

        # Iterate through the whole list of blocks and change 'model__estimator' parameter to an object of Sklearn.
        parameters = []
        for parameters_block in json_parameters['parameters']:
            if 'model__estimator' in parameters_block:
                estimator = parameters_block['model__estimator'][0]
                if estimator == 'RandomForestClassifier':
                    estimator = [RandomForestClassifier()]
                elif estimator == 'SVM':
                    estimator = [SVC()]
                else:
                    raise ValueError("Invalid model was specified in the training config file: you may specify SVM or "
                                     "RandomForestClassifier")

                parameters_block['model__estimator'] = estimator

            parameters.append(parameters_block)

        return parameters

    @property
    def authors(self):
        if self._parameters.authors is None:
            raise ValueError('You try to get access to a list of authors that is None')

        if os.path.exists(self._parameters.authors):
            with open(self._parameters.authors, 'r') as file:
                authors = [author.strip() for author in file.read().splitlines() if author]
        else:
            authors = [author.strip() for author in self._parameters.authors.split(',') if author]

        if not authors:
            raise ValueError('A list of authors is empty. May be you pass incorrect file or a string, '
                             'containing authors')

        return authors

    @property
    def max_count(self):
        return self._parameters.max_count

    @property
    def index(self):
        if self._parameters.index is None:
            raise ValueError('The name of index is None.')

        return self._parameters.index

    @property
    def host(self) -> str:
        if (host := self._parameters.host) is None:
            host = os.getenv('ES_HOST', 'localhost')
            if host is None:
                self._parser.error("hostname of Elasticsearch server wasn't specify, please, enter it or set ES_HOST "
                                   "environment value")

        return host

    @property
    def port(self) -> str:
        if (port := self._parameters.port) is None:
            port = os.getenv("ES_PORT", '9200')
            if port is None:
                self._parser.error("port of Elasticsearch server wasn't specify, please, enter it or set ES_PORT "
                                   "environment value")

        return port
