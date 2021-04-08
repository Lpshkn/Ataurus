import unittest.mock
import pandas as pd
from ataurus.preparing.preprocessor import Preprocessor


class PreprocessorTest(unittest.TestCase):
    def setUp(self):
        self.test_texts = ['ЭТО первый ТЕКСТ', 'Это Второй Тестовый текст', '', 'Прежде был пустой   текст, теперь нет',
                           "РАЗРАБОТЧИКИ?, !$ LinkedIn    \n\n  объявили о появившейся возможности#%^^%!@#$%^&*(? "
                           "https://google.com/"]

    def tearDown(self):
        pass

    def test_preprocess_text(self):
        self.assertEqual(Preprocessor.preprocess_text(self.test_texts[4],
                                                      lower=True, delete_whitespace=True, delete_urls=True),
                         'разработчики?, ! linkedin объявили о появившейся возможности!?')
        self.assertEqual(Preprocessor.preprocess_text(self.test_texts[0],
                                                      lower=True, delete_whitespace=True, delete_urls=True),
                         'это первый текст')
        self.assertEqual(Preprocessor.preprocess_text(self.test_texts[1],
                                                      lower=False, delete_whitespace=True, delete_urls=True),
                         'Это Второй Тестовый текст')
        self.assertEqual(Preprocessor.preprocess_text(self.test_texts[3],
                                                      lower=False, delete_whitespace=False, delete_urls=True),
                         'Прежде был пустой   текст, теперь нет')
        self.assertEqual(Preprocessor.preprocess_text(self.test_texts[4],
                                                      lower=False, delete_whitespace=False, delete_urls=True),
                         "РАЗРАБОТЧИКИ?, ! LinkedIn    \n\n  объявили о появившейся возможности!?")
        self.assertEqual(Preprocessor.preprocess_text(self.test_texts[4],
                                                      lower=False, delete_whitespace=False, delete_urls=False),
                         "РАЗРАБОТЧИКИ?, ! LinkedIn    \n\n  объявили о появившейся возможности!?"
                         " httpsgoogle.com")

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
