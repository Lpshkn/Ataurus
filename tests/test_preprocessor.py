import unittest.mock
from ataurus.preparing.preprocessor import Preprocessor


class PreprocessorTest(unittest.TestCase):
    def setUp(self):
        self.test_texts = ['ЭТО первый ТЕКСТ', 'Это Второй Тестовый Текст', '', 'Прежде был пустой   текст, теперь нет',
                           "РАЗРАБОТЧИКИ?, !$ LinkedIn    \n\n  объявили о появившейся возможности#%^^%!@#$%^&*(? "
                           "https://google.com/"]

        self.test_sentences_texts = ['Это первый текст. И. Первое предложение. РИАЛИ.', '', 'ВТОРОЕ #$$%$& '
                                     'предложение. This https://lpshkn.xyz/ ЭТО! Сайт не!? мой.']

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
                         'Это Второй Тестовый Текст')
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
        preprocessor = Preprocessor(self.test_texts)
        self.assertEqual(preprocessor.tokens(lower=True, normalization=True, remove_stopwords=True),
                         [['текст'],
                          ['тестовый', 'текст'],
                          [],
                          ['прежде', 'быть', 'пустой', 'текст'],
                          ['разработчик', 'linkedin', 'объявить', 'появиться', 'возможность']])

        self.assertEqual(preprocessor.tokens(lower=False, normalization=True, remove_stopwords=True),
                         [['текст'],
                          ['тестовый', 'текст'],
                          [],
                          ['прежде', 'быть', 'пустой', 'текст'],
                          ['разработчик', 'linkedin', 'объявить', 'появиться', 'возможность']])

        self.assertEqual(preprocessor.tokens(lower=False, normalization=False, remove_stopwords=True),
                         [['ТЕКСТ'],
                          ['Тестовый', 'Текст'],
                          [],
                          ['Прежде', 'был', 'пустой', 'текст'],
                          ['РАЗРАБОТЧИКИ', 'LinkedIn', 'объявили', 'появившейся', 'возможности']])

        self.assertEqual(preprocessor.tokens(lower=False, normalization=False, remove_stopwords=False),
                         [['ЭТО', 'первый', 'ТЕКСТ'],
                          ['Это', 'Второй', 'Тестовый', 'Текст'],
                          [],
                          ['Прежде', 'был', 'пустой', 'текст', 'теперь', 'нет'],
                          ['РАЗРАБОТЧИКИ', 'LinkedIn', 'объявили', 'о', 'появившейся', 'возможности']])

    def test_sentences_method(self):
        preprocessor = Preprocessor(self.test_sentences_texts)
        self.assertEqual(preprocessor.sentences(lower=True, normalization=True, remove_stopwords=True),
                         [['это первый текст', 'и первое предложение', 'риали'],
                          [],
                          ['второе предложение', 'this это', 'сайт не мой']])

        self.assertEqual(preprocessor.sentences(lower=False, normalization=True, remove_stopwords=True),
                         [['Это первый текст', 'И Первое предложение', 'РИАЛИ'],
                          [],
                          ['ВТОРОЕ предложение', 'This ЭТО', 'Сайт не мой']])
