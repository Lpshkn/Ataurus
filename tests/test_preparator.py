import unittest.mock
import pandas as pd
from ataurus.preparing.preprocessor import Preprocessor


class PreprocessorTest(unittest.TestCase):
    def setUp(self):
        self.test_texts = ['ЭТО первый ТЕКСТ', 'Это Второй Тестовый текст', '', 'Прежде был пустой текст, теперь нет']

    def tearDown(self):
        pass

    def test_preprocess_text(self):
        texts = ["РАЗРАБОТЧИКИ LinkedIn    \n\n  объявили о появившейся возможности", "https://google.com/", "author"]

        self.assertEqual(Preprocessor.preprocess_text(texts[0]),
                         'разработчики linkedin объявили о появившейся возможности')
        self.assertEqual(Preprocessor.preprocess_text(texts[1]), '')
        self.assertEqual(Preprocessor.preprocess_text(texts[2]), 'author')
        self.assertEqual(Preprocessor.preprocess_text(self.test_texts[2]), '')
        self.assertEqual(Preprocessor.preprocess_text("РАЗРАБОТЧИКИ LinkedIn", lower=False), 'РАЗРАБОТЧИКИ LinkedIn')
        self.assertEqual(Preprocessor.preprocess_text(texts[0], lower=False, delete_whitespace=False), texts[0])
        self.assertEqual(Preprocessor.preprocess_text(texts[0] + ' ' + texts[1], lower=False, delete_whitespace=False),
                         texts[0])
        self.assertEqual(Preprocessor.preprocess_text(texts[0] + ' ' + texts[1], lower=False, delete_whitespace=False,
                                                      delete_urls=False), texts[0] + ' ' + texts[1])

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
