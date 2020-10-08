"""
This module represents functions for options of the command line.
Also module implements a class containing information about the project and all the information that
will be printed in the command line.
"""

import re
import argparse
import pandas as pd


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

        parser.add_argument('input',
                            help='the input file in the CSV format',
                            type=argparse.FileType(mode='r', encoding='utf-8'))

        return parser

    def _get_parameters(self, args):
        """
        This method gets all parameters from the args of the command line.
        :param args: list of the arguments of the command line
        :return: parsed arguments
        """
        parameters = self._parser.parse_args(args)
        return parameters

    @property
    def data(self) -> pd.DataFrame:
        file = self._parameters.input
        # The input file must be csv format because of it will provide safe operations with data
        if not re.search(r'\.csv$', file.name):
            raise ValueError("The input file isn't csv format")

        try:
            it = pd.read_csv(file)
        except UnicodeDecodeError as e:
            raise ValueError("Data in the input file isn't UTF-8 encoding")

        return it
