import unittest.mock
import pandas as pd
import ataurus.preparing.preprocessor as prep


class preprocessorTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_incorrect_type_data(self):
        with self.assertRaises(TypeError):
            prep.preprocessor().fit([])

    def test_no_columnname_data(self):
        df = pd.DataFrame([1, 2, 3])
        with self.assertRaises(KeyError):
            prep.Preprocessor().fit(df)

    def test_process_text_method(self):
        df = pd.DataFrame([["РАЗРАБОТЧИКИ LinkedIn    \n\n  объявили о появившейся возможности"
                           "https://google.com/", "author"]], columns=['text', 'author'])
        preprocessor = prep.Preprocessor().fit(df)
        processed = preprocessor._process_text(0)
        self.assertEqual(processed, 'разработчики linkedin объявили о появившейся возможности')

        df = pd.DataFrame([[1, 'aa'], [2, 'bb'], [3, 'cc']], columns=['text', 'author'])
        preprocessor = prep.Preprocessor().fit(df)
        with self.assertRaises(TypeError):
            preprocessor._process_text(0)

    def test_tokens_method(self):
        df = pd.DataFrame([["РАЗРАБОТЧИКИ?, !$ LinkedIn    \n\n  объявили о появившейся возможности#%^^%!@#$%^&*(?"
                           "https://google.com/", "author"]], columns=['text', 'author'])
        preprocessor = prep.Preprocessor().fit(df)
        tokens = preprocessor.tokens(0)
        self.assertEqual(tokens, [['разработчики', 'linkedin', 'объявили', 'о', 'появившейся', 'возможности']])

        df = pd.DataFrame([["РАЗРАБОТЧИКИ, LinkedIn    \n\n  объявили ? о появившейся возможности!"
                           "https://google.com/", "author"]], columns=['text', 'author'])
        preprocessor = prep.Preprocessor().fit(df)
        tokens = preprocessor.tokens(0, False, False)
        self.assertEqual(tokens,
                         [['РАЗРАБОТЧИКИ', ',', 'LinkedIn', 'объявили', '?', 'о', 'появившейся', 'возможности', '!']])

    def test_sentences_method(self):
        df = pd.DataFrame([["Это расширение. Было!? Анонсировано в! Рамках продолжения политики LinkedIn. "
                           "О непрерывности,%;%:%* профессионального.", "author"]], columns=['text', 'author'])
        preprocessor = prep.Preprocessor().fit(df)
        sentences = preprocessor.sentences(0, True, True)
        self.assertEqual(sentences,
                         [['это расширение', 'было', 'анонсировано в', 'рамках продолжения политики linkedin',
                           'о непрерывности профессионального']])
