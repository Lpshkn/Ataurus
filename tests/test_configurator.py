import os
import json
import unittest.mock
import ataurus.configurator.configurator as cfg
from ataurus.configurator.utils import (MODEL_FILE, CACHE_DIRECTORY, CACHE_CFG_FILE, POSTFIX_CACHE_FEATURES,
                                        convert_to_cache_name, convert_from_cache_name, get_hash, CONFIG_DIRECTORY)


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
        args = ['train test']
        with self.assertRaises(SystemExit):
            configurator = cfg.Configurator(args)

    def test_existed_file(self):
        args = ['train', self.incorrect_file]
        configurator = cfg.Configurator(args)

    def test_file_extension(self):
        args = ['train', self.incorrect_file]
        configurator = cfg.Configurator(args)
        with self.assertRaises(ValueError):
            data = configurator.input

    def test_correct_file(self):
        args = ['train', self.correct_file]
        configurator = cfg.Configurator(args)
        data = configurator.input

    def test_initializing_directories(self):
        args = ['train', self.correct_file]
        configurator = cfg.Configurator(args)

        configurator._initialize_directories()
        self.assertTrue(os.path.exists(CACHE_DIRECTORY))

    def test_initializing_cache(self):
        args = ['train', self.correct_file]
        configurator = cfg.Configurator(args)

        # Initialize and check that _cache is not None
        configurator._initialize_directories()
        configurator._initialize_cache()
        self.assertIsNotNone(configurator._cache)

        filename = os.path.join(CACHE_DIRECTORY, 'test')
        with open(filename, 'w') as file:
            file.write('teststring')

        self.assertTrue(os.path.exists(filename))
        # Now this file must be removed because _cache has no keys
        configurator._initialize_cache()
        self.assertFalse(os.path.exists(filename))


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
        self.assertEqual(convert_from_cache_name(filename), 'file')
