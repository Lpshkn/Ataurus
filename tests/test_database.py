import os
import unittest
from ataurus.database.db import Database


ES_HOST = os.getenv('ES_HOST', 'localhost')
ES_PORT = os.getenv('ES_PORT', '9200')


class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.correct_host = f'{ES_HOST}:{ES_PORT}'
        self.incorrect_host = 'wrong'
        self.db = Database.connect([self.correct_host])
        self.test_index = 'test_index'
        self.db.connection.index(index=self.test_index, body={'author': 'test', 'text': 'test'})

    def tearDown(self) -> None:
        self.db.connection.indices.delete(self.test_index)

    def test_correct_connection(self):
        self.assertTrue(self.db.connection.ping())

    def test_wrong_connection(self):
        with self.assertRaises(ConnectionError):
            Database.connect([self.incorrect_host])

    def test_get_texts(self):
        authors, texts = self.db.get_authors_texts(self.test_index, 'author', 'text')
        self.assertEqual(authors, ['test'])
        self.assertEqual(texts, ['test'])


if __name__ == '__main__':
    unittest.main()
