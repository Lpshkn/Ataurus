import sys
import elasticsearch
import pandas as pd
import time
from elasticsearch_dsl import Search
from tqdm import tqdm


class Database:
    def __init__(self):
        self._es = None

    @staticmethod
    def connect(hosts: list[str], /):
        """
        Implements connecting to the Elasticsearch cluster and returns the Database object containing
        this connection.

        :param hosts: a list of hosts
        :return: Database object
        """
        database = Database()
        database._es = elasticsearch.Elasticsearch(hosts=hosts)

        if database._es.ping():
            return database
        else:
            raise ConnectionError("The connection to Elasticsearch wasn't made")

    @property
    def connection(self):
        if self._es is None:
            raise ValueError("You didn't initialize a connection with an ElasticSearch cluster")

        return self._es

    def get_authors_texts(self, index: str, author_field: str, text_field: str) -> tuple[list[str], list[str]]:
        """
        Gets all documents from the index of ElasticSearch cluster by its author- and text- fields.

        :param index: the name of index containing documents
        :param author_field: the name of field containing the name of an author of a document
        :param text_field: the name of field containing a text of a document
        :return: tuple of list of authors, list of texts
        """
        # Update the index before processing
        self.connection.indices.refresh(index=index)

        search = Search(index=index, using=self.connection).query("match_all")
        authors, texts = [], []
        for hit in search.scan():
            authors.append(hit[author_field])
            texts.append(hit[text_field])

        return authors, texts

    def upload_dataframe(self, index: str, dataframe: pd.DataFrame, verbose=False):
        """
        Method uploads a DataFrame object into an ElasticSearch cluster. This DataFrame object must contain 'author' and
        'text' columns. The 'post_number' column doesn't require, but if it's specified a document will have the id
        as the number of an article.

        :param index: the name of an index where data will be upload to
        :param dataframe: a DataFrame object containing data
        :param verbose: show a progress bar and other verbosity
        """
        if verbose:
            print('Loading data to the ElasticSearch cluster started...')
            time.sleep(1)

        for _, row in tqdm(dataframe.dropna().iterrows(), total=len(dataframe.index), disable=(not verbose)):
            try:
                body = {
                    "author": row["author"],
                    "text": row['text']
                }
            except KeyError:
                print("Uploading dataframe object is incorrect and doesn't contain 'author' or 'text' columns ",
                      file=sys.stderr)
                exit(-1)

            if 'post_number' in row:
                self.connection.index(index, body=body, id=row["post_number"])
            else:
                self.connection.index(index, body=body)
