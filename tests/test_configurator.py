import os
import unittest.mock
import ataurus.configurator.configurator as cfg
from ataurus.configurator.utils import (MODEL_FILE, CACHE_DIRECTORY, CACHE_CFG_FILE, POSTFIX_CACHE_FEATURES,
                                        convert_to_cache_name, convert_from_cache_name, get_hash)


class ConfiguratorTest(unittest.TestCase):
    def setUp(self):
        self.incorrect_file = 'test_incorrect_file'
        self.correct_file = 'test_correct_file.csv'

        with open(self.incorrect_file, 'w') as file:
            file.write('teststring')
        with open(self.correct_file, 'w') as file:
            file.write('teststring')

    def tearDown(self):
        if os.path.isfile(self.incorrect_file):
            os.remove(self.incorrect_file)
        if os.path.isfile(self.correct_file):
            os.remove(self.correct_file)

    @unittest.mock.patch('sys.stderr', open(os.devnull, 'w'))
    def test_empty_args(self):
        args = []
        with self.assertRaises(SystemExit):
            cfg.Configurator(args)

    @unittest.mock.patch('sys.stderr', open(os.devnull, 'w'))
    def test_incorrect_args(self):
        args = ['-g' 'incorrect']
        with self.assertRaises(SystemExit):
            cfg.Configurator(args)

    @unittest.mock.patch('sys.stderr', open(os.devnull, 'w'))
    def test_incorrect_input_file(self):
        args = ['-f', 'file']
        with self.assertRaises(SystemExit):
            configurator = cfg.Configurator(args)

    def test_existed_file(self):
        args = ['-f', self.incorrect_file]
        configurator = cfg.Configurator(args)

    def test_file_extension(self):
        args = ['-f', self.incorrect_file]
        configurator = cfg.Configurator(args)
        with self.assertRaises(ValueError):
            data = configurator.data

    def test_correct_file(self):
        args = ['-f', self.correct_file]
        configurator = cfg.Configurator(args)
        data = configurator.data


class ConfiguratorUtilsTest(unittest.TestCase):
    def test_converting_to_cache(self):
        filename = 'file.csv'
        self.assertEqual(convert_to_cache_name(filename), 'file' + POSTFIX_CACHE_FEATURES + '.csv')
        self.assertEqual(convert_to_cache_name(filename, 'pickle'), 'file' + POSTFIX_CACHE_FEATURES + '.pickle')
        filename = 'file.exe.csv'
        self.assertEqual(convert_to_cache_name(filename, 'pickle'), 'file.exe' + POSTFIX_CACHE_FEATURES + '.pickle')
        self.assertEqual(convert_to_cache_name(filename, 'pickle'), 'file.exe' + POSTFIX_CACHE_FEATURES + '.pickle')
        filename = 'file'
        self.assertEqual(convert_to_cache_name(filename), 'file' + POSTFIX_CACHE_FEATURES)
        self.assertEqual(convert_to_cache_name(filename, 'pickle'), 'file' + POSTFIX_CACHE_FEATURES + '.pickle')

    def test_converting_from_cache(self):
        filename = 'file_features.csv'
        self.assertEqual(convert_from_cache_name(filename), 'file' + '.csv')
        self.assertEqual(convert_from_cache_name(filename, 'pickle'), 'file' + '.pickle')
        filename = 'file.exe_features.csv'
        self.assertEqual(convert_from_cache_name(filename, 'pickle'), 'file.exe' + '.pickle')
        filename = 'file_features'
        self.assertEqual(convert_from_cache_name(filename, 'pickle'), 'file.pickle')
        self.assertEqual(convert_from_cache_name(filename), 'file')
        filename = 'file'
        with self.assertRaises(ValueError):
            convert_from_cache_name(filename, 'pickle')
