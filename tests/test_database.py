from ataurus.database.db import Database
import unittest
import elasticsearch


class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = Database.connect(['localhost:9200']).connection
        self.test_index = 'test'

    def tearDown(self) -> None:
        self.connection.indices.delete(index=self.test_index, ignore=[400, 404])

    def test_correct_connection(self):
        self.assertTrue(self.connection.ping())

    def test_wrong_connection(self):
        with self.assertRaises(ConnectionError):
            Database.connect(["wrong_address:9500"])

    def test_creating_index(self):
        self.connection.indices.create(self.test_index)
        self.assertTrue(self.connection.indices.exists(self.test_index))

    def test_incorrect_index(self):
        self.connection.indices.create(self.test_index)
        with self.assertRaises(elasticsearch.exceptions.RequestError) as e:
            self.connection.indices.create(self.test_index)
            self.assertEqual(e.exception.status_code, 400)


if __name__ == '__main__':
    unittest.main()
