from ataurus.database.db import Database
from ataurus.database.model import Article
import unittest
import elasticsearch
import elasticsearch_dsl as es_dsl


class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = Database.connect(['localhost:9200']).connection

    def tearDown(self) -> None:
        self.connection.indices.delete(index=Article.Index.name, ignore=[400, 404])

    def test_correct_connection(self):
        self.assertTrue(self.connection.ping())

    def test_wrong_connection(self):
        with self.assertRaises(ConnectionError):
            Database.connect(["wrong_address:9500"])

    def test_creating_index(self):
        Article.init(using=self.connection)
        self.assertTrue(self.connection.indices.exists(Article.Index.name))


if __name__ == '__main__':
    unittest.main()
