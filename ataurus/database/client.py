import elasticsearch
from elasticsearch_dsl import Search


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
