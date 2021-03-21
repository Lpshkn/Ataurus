from ataurus.database.db import Database
import unittest


class DatabaseTest(unittest.TestCase):
    def test_correct_connection(self):
        db = Database.connect(['localhost:9200'])
        self.assertTrue(db.connection.ping())

    def test_wrong_connection(self):
        with self.assertRaises(ConnectionError):
            Database.connect(["wrong_address:9500"])


if __name__ == '__main__':
    unittest.main()
