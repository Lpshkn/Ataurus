import os
import unittest.mock
import pandas as pd
import ataurus.preparing.preparator as prep


class PreparatorTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_incorrect_type_data(self):
        with self.assertRaises(TypeError):
            prep.Preparator([])

    def test_no_columnname_data(self):
        df = pd.DataFrame([1, 2, 3])
        with self.assertRaises(KeyError):
            prep.Preparator(df)

    def test_correct_data(self):
        df = pd.DataFrame([1, 2, 3], columns=['text'])
        preparator = prep.Preparator(df)
        self.assertTrue(all(df == preparator.data))

    def test_process_text_method(self):
        df = pd.DataFrame(["РАЗРАБОТЧИКИ LinkedIn    \n\n  объявили о появившейся возможности"
                           "https://google.com/"], columns=['text'])
        preparator = prep.Preparator(df)
        processed = preparator._process_text(0)
        self.assertEqual(processed, 'разработчики linkedin объявили о появившейся возможности')

        df = pd.DataFrame([1, 2, 3], columns=['text'], dtype=int)
        preparator = prep.Preparator(df)
        with self.assertRaises(TypeError):
            preparator._process_text(0)

    def test_tokens_method(self):
        df = pd.DataFrame(["РАЗРАБОТЧИКИ?, !$ LinkedIn    \n\n  объявили о появившейся возможности#%^^%!@#$%^&*(?"
                           "https://google.com/"], columns=['text'])
        preparator = prep.Preparator(df)
        tokens = preparator.tokens(0)
        self.assertEqual(tokens, [['разработчики', 'linkedin', 'объявили', 'о', 'появившейся', 'возможности']])

        df = pd.DataFrame(["РАЗРАБОТЧИКИ, LinkedIn    \n\n  объявили ? о появившейся возможности!"
                           "https://google.com/"], columns=['text'])
        preparator = prep.Preparator(df)
        tokens = preparator.tokens(0, False, False)
        self.assertEqual(tokens,
                         [['РАЗРАБОТЧИКИ', ',', 'LinkedIn', 'объявили', '?', 'о', 'появившейся', 'возможности', '!']])

    def test_sentences_method(self):
        df = pd.DataFrame(["Это расширение. Было!? Анонсировано в! Рамках продолжения политики LinkedIn. "
                           "О непрерывности,%;%:%* профессионального."], columns=['text'])
        preparator = prep.Preparator(df)
        sentences = preparator.sentences(0, True, True)
        self.assertEqual(sentences,
                         [['это расширение', 'было', 'анонсировано в', 'рамках продолжения политики linkedin',
                           'о непрерывности профессионального']])
