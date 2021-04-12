"""
This module contains Preprocessor class that will prepare passed texts and returns a list of tokens,
sentences and processed or unprocessed texts.
All unnecessary symbols, stop words and other incorrect symbols will be removed from the text.
"""
import re
from razdel import tokenize, sentenize
from .rules import PUNCTUATIONS, URLS, STOPWORDS
from pymorphy2 import MorphAnalyzer


class Preprocessor:
    def __init__(self, texts: list[str]):
        if not any(texts):
            raise ValueError("A list of texts is incorrect: it's may be None or empty")
        self._texts = texts

    def tokens(self,
               lower=True,
               normalization=True,
               remove_stopwords=True) -> list[list[str]]:
        """
        Get a list of tokens from a passed text.

        :param lower: to lower a result
        :param normalization: normalize each token in the sentence, each word is transformed to lower case
        :param remove_stopwords: remove stopwords from the tokens
        :return: a list of lists of tokens for an each passed text
        """
        results = []
        morph = MorphAnalyzer()

        for text in self._texts:
            preprocessed_text = self.preprocess_text(text, lower=lower, delete_whitespace=True, delete_urls=True)

            # Nested conditions - it's faster than make it separately
            if normalization:
                if remove_stopwords:
                    tokens = [normal_form for token in tokenize(preprocessed_text)
                              if not PUNCTUATIONS.match(token.text)
                              and not STOPWORDS.match((normal_form := morph.parse(token.text)[0].normal_form))]
                else:
                    tokens = [morph.parse(token.text)[0].normal_form for token in tokenize(preprocessed_text)
                              if not PUNCTUATIONS.match(token.text)]
            else:
                if remove_stopwords:
                    tokens = [token.text for token in tokenize(preprocessed_text)
                              if not PUNCTUATIONS.match(token.text) and not STOPWORDS.match(token.text)]
                else:
                    tokens = [token.text for token in tokenize(preprocessed_text) if not PUNCTUATIONS.match(token.text)]

            results.append(tokens)

        return results

    def sentences(self,
                  lower=True,
                  normalization=True,
                  remove_stopwords=True) -> list[list[str]]:
        """
        Get a list of sentences from a passed text.

        :param lower: to lower a result
        :return: a list of lists of sentences for an each passed text
        """
        results = []

        for text in self._texts:
            preprocessed_text = self.preprocess_text(text, lower=False, delete_whitespace=False, delete_urls=True)

            if lower:
                sentences = [re.sub(r'[\s]+', r' ', PUNCTUATIONS.sub(" ", sentence.text.lower())).strip()
                             for sentence in sentenize(preprocessed_text) if sentence.text]
            else:
                sentences = [re.sub(r'[\s]+', r' ', PUNCTUATIONS.sub(" ", sentence.text)).strip()
                             for sentence in sentenize(preprocessed_text) if sentence.text]

            results.append(sentences)

        return results

    def texts(self):
        return self._texts

    @staticmethod
    def preprocess_text(text: str,
                        lower=True,
                        delete_whitespace=True,
                        delete_urls=True) -> str:
        """
        Processes the text depending on specified options. Remove incorrect symbols except of: , . ! ? " -

        :param text: a text that will be processed
        :param lower: to lower a result
        :param delete_whitespace: remove redundant whitespaces
        :param delete_urls: remove all url links
        :return: processed text
        """
        if lower:
            text = text.lower()
        if delete_whitespace:
            text = re.sub(r'[\s]+', r' ', text).strip()
        if delete_urls:
            text = URLS.sub('', text)

        text = re.sub(r'[%№@#$^&*)(_=+/\\|~`\[\]}{:;]', '', text)

        return text.strip()
