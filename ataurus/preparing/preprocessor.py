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
        self.texts = texts

    def tokens(self,
               lower=True,
               normalization=True,
               remove_stopwords=True) -> list[list[str]]:
        """
        Get a list of tokens from the text received by the index from the DataFrame.

        :param lower: to lower a result
        :param normalization: normalize each token in the sentence
        :param remove_stopwords: remove stopwords from the tokens
        :return: a list of lists of tokens for an each passed text
        """
        results = []
        morph = MorphAnalyzer()

        for text in self.texts:
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
                  index: int = None,
                  lower=True,
                  delete_punctuations=True) -> list:
        """
        Get a list of sentences from the text received by the index from the DataFrame.

        :param index: index of a text of the DataFrame that you want to process.
                      If it's None, all the texts will be processed.
        :param lower: to lower a result
        :param delete_punctuations: delete all punctuations from a result
        :return: list - the list of sentences
        """
        results = []
        if index is None:
            index = range(len(self._texts))
        else:
            if not isinstance(index, int):
                raise TypeError("The index that you want to use to get a text isn't int!")
            index = [index]

        for i in index:
            text = self._process_text(i, lower=False, delete_whitespace=False, delete_urls=True)
            if not text:
                continue

            if lower:
                sentences = [sentence.text.lower() for sentence in sentenize(text)]
            else:
                sentences = [sentence.text for sentence in sentenize(text)]

            if delete_punctuations:
                sentences = [re.sub(r'[\s]+', r' ', PUNCTUATIONS.sub(" ", sentence)).strip() for sentence in sentences]

            results.append(sentences)

        return results

    @staticmethod
    def preprocess_text(text: str,
                        lower=True,
                        delete_whitespace=True,
                        delete_urls=True) -> str:
        """
        Process the text depending on specified options.

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
        return text
