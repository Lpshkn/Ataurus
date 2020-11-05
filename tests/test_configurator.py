import os
import unittest.mock
import ataurus.configurator as cfg


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
        args = ['-i' 'incorrect']
        with self.assertRaises(SystemExit):
            cfg.Configurator(args)

    @unittest.mock.patch('sys.stderr', open(os.devnull, 'w'))
    def test_incorrect_input_file(self):
        args = ['file']
        with self.assertRaises(SystemExit):
            configurator = cfg.Configurator(args)

    def test_existed_file(self):
        args = [self.incorrect_file]
        configurator = cfg.Configurator(args)
        parameters = configurator._get_parameters(args)

    def test_file_extension(self):
        args = [self.incorrect_file]
        configurator = cfg.Configurator(args)
        with self.assertRaises(ValueError):
            data = configurator.data

    def test_correct_file(self):
        args = [self.correct_file]
        configurator = cfg.Configurator(args)
        data = configurator.data
