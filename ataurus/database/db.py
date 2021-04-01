import elasticsearch
from database.model import Article


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
            Article.init(using=database._es)
            return database
        else:
            raise ConnectionError("The connection to Elasticsearch wasn't made")

    @property
    def connection(self):
        return self._es
