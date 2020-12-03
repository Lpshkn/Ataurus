import unittest.mock
import os
from ataurus.ml.model import Model
from ataurus.features.extractor import FeaturesExtractor


class TestModel(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', open(os.devnull, 'w'))
    @unittest.mock.patch('sys.stderr', open(os.devnull, 'w'))
    def test_incorrect_data(self):
        model = Model()
        with self.assertRaises(ValueError):
            model.fit([], [])
        with self.assertRaises(TypeError):
            model.fit(None, None)

    @unittest.mock.patch('sys.stdout', open(os.devnull, 'w'))
    @unittest.mock.patch('sys.stderr', open(os.devnull, 'w'))
    def test_correct_data(self):
        extractor = FeaturesExtractor()
        extractor.fit([['ваапвап'], ['парпарпарпа'], ['собака']],
                      [['пвапврпарап'], ['teststring'], ['парпарпаропроhпа']], [[1], [2], [1]])
        model = Model()
        with self.assertRaises(ValueError):
            model.fit(extractor.X, extractor.y)
        model.fit(extractor.X, extractor.y, grid_search=False, cv=2)


if __name__ == '__main__':
    unittest.main()
