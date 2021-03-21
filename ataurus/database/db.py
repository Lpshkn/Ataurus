import elasticsearch
from database.config import INDEX_SETTINGS


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

    def create_index(self, name, /, settings=INDEX_SETTINGS):
        """
        Creates an index in the Elasticsearch cluster and passes the settings of initializing index.

        :param name: tha name of index
        :param settings: the body of request
        """
        if not self.connection.indices.exists(name):
            self.connection.indices.create(index=name, body=settings)
