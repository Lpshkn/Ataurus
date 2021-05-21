"""
This module contains Preprocessor class that will prepare passed texts and returns a list of tokens,
sentences and processed or unprocessed texts.
All unnecessary symbols, stop words and other incorrect symbols will be removed from the text.
"""
import re
import time
import pandas as pd
import numpy as np

from razdel import tokenize, sentenize
from .rules import PUNCTUATIONS, URLS, STOPWORDS
from pymorphy2 import MorphAnalyzer
from joblib.parallel import Parallel, delayed
from tqdm import tqdm


class Preprocessor:
    def __init__(self, texts: list[str], authors: list[str] = None, n_jobs=-1):
        if not any(texts):
            raise ValueError("A list of texts is incorrect: it's may be None or empty")

        if authors is not None:
            df = pd.DataFrame(np.c_[texts, authors], columns=['texts', 'authors'])
        else:
            df = pd.DataFrame(texts, columns=['texts'])

        df = df[df['texts'].notnull()]
        self._texts = df['texts'].values
        self._authors = df['authors'].values if authors is not None else None
        self.n_jobs = n_jobs

    def tokens(self,
               lower=True,
               normalization=True,
               remove_stopwords=False,
               verbose=True) -> np.ndarray:
        """
        Get a list of tokens from a passed text.

        :param lower: to lower a result
        :param normalization: normalize each token in the sentence, each word is transformed to lower case
        :param remove_stopwords: remove stopwords from the tokens
        :param verbose:
        :return: a list of lists of tokens for an each passed text
        """
        morph = MorphAnalyzer()

        def process_text(text):
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
            return tokens

        if verbose:
            print('Start tokens processing...')
            time.sleep(1)
            results = Parallel(n_jobs=self.n_jobs)(delayed(process_text)(text) for text in tqdm(self._texts))
            print('Tokens processing completed')
        else:
            results = Parallel(n_jobs=self.n_jobs)(delayed(process_text)(text) for text in self._texts)

        return np.array(results, dtype=object)

    def sentences(self,
                  lower=True,
                  normalization=True,
                  remove_stopwords=True,
                  verbose=True) -> np.ndarray:
        """
        Get a list of sentences from a passed text.

        :param lower: to lower a result
        :param normalization:
        :param remove_stopwords:
        :param verbose:
        :return: a list of lists of sentences for an each passed text
        """
        def process_text(text):
            preprocessed_text = self.preprocess_text(text, lower=False, delete_whitespace=False, delete_urls=True)

            if lower:
                sentences = [re.sub(r'[\s]+', r' ', PUNCTUATIONS.sub(" ", sentence.text.lower())).strip()
                             for sentence in sentenize(preprocessed_text) if sentence.text]
            else:
                sentences = [re.sub(r'[\s]+', r' ', PUNCTUATIONS.sub(" ", sentence.text)).strip()
                             for sentence in sentenize(preprocessed_text) if sentence.text]

            return sentences

        if verbose:
            print('Start sentences processing...')
            time.sleep(1)
            results = Parallel(n_jobs=self.n_jobs)(delayed(process_text)(text) for text in tqdm(self._texts))
            print('Sentences processing completed')
        else:
            results = Parallel(n_jobs=self.n_jobs)(delayed(process_text)(text) for text in self._texts)

        return np.array(results, dtype=object)

    def texts(self) -> np.ndarray:
        return np.array(self._texts, dtype=object)

    @property
    def authors(self):
        return self._authors

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
