import os
import unittest.mock
import ataurus.features.functions as funcs
from ataurus.features.extractor import FeaturesExtractor


class TestFunctions(unittest.TestCase):
    def setUp(self) -> None:
        self.tokens = ['one', 'two', 'три', 'собака']
        self.tokens_pos = ['один', 'собака', 'fsdfsd', 'бежать', 'мы', 'ddgf546^6gfd767', '6^%#%$^', 'он']
        self.sentences = ['Это первое предложение', 'Второе предложение', 'Third sentence']

    def test_avg_len_words(self):
        self.assertIsNone(funcs.avg_len_words([]))
        self.assertIsNone(funcs.avg_len_words(None))
        self.assertEqual(funcs.avg_len_words(self.tokens), 3.75)

    def test_avg_len_sentences(self):
        self.assertIsNone(funcs.avg_len_sentences(None))
        self.assertIsNone(funcs.avg_len_sentences([]))
        self.assertEqual(funcs.avg_len_sentences(self.sentences), 18)

    def test_pos_distribution(self):
        pos = funcs.pos_distribution(self.tokens_pos)
        self.assertEqual(pos['ADJF'], 0.125)
        self.assertEqual(pos['CONJ'], 0)
        self.assertEqual(pos['NOUN'], 0.125)
        self.assertEqual(pos['INFN'], 0.125)
        self.assertEqual(pos['FRGN'], 0.125)
        self.assertEqual(pos['NPRO'], 0.25)
        self.assertEqual(pos['NONE'], 0.25)

    def test_foreign_ratio(self):
        self.assertIsNone(funcs.foreign_words_ratio(None))
        self.assertIsNone(funcs.foreign_words_ratio([]))
        self.assertEqual(funcs.foreign_words_ratio(self.tokens_pos), 0.125)

    def test_vocabulary_richness(self):
        self.assertIsNone(funcs.vocabulary_richness(None))
        self.assertIsNone(funcs.vocabulary_richness([]))
        self.assertEqual(funcs.vocabulary_richness(self.tokens_pos), 1)
        self.assertEqual(funcs.vocabulary_richness(['мы', 'мы', 'мы', 'мы']), 0.25)
        self.assertEqual(funcs.vocabulary_richness(['мы', 'z', 'мы', 'я']), 0.75)


class TestFeaturesExtractor(unittest.TestCase):
    def test_empty_properties(self):
        extractor = FeaturesExtractor()
        with self.assertRaises(ValueError):
            features = extractor.features
        with self.assertRaises(ValueError):
            X = extractor.X
        self.assertIsNone(extractor.y)
        with self.assertRaises(ValueError):
            classes = extractor.classes

    @unittest.mock.patch('sys.stdout', open(os.devnull, 'w'))
    @unittest.mock.patch('sys.stderr', open(os.devnull, 'w'))
    def test_correct_data(self):
        extractor = FeaturesExtractor()
        extractor.fit([['ваапвап'], ['парпарпарпа']], [['пвапврпарап'],['парпарпаропроhпа']], [])
        self.assertIsNotNone(extractor.X)
        self.assertIsNone(extractor.y)
        self.assertIsNone(extractor.classes)


if __name__ == '__main__':
    unittest.main()
