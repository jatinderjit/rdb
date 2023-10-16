import unittest
from typing import Optional


class Database:
    def __init__(self):
        self._db: dict[str, str] = {}

    def set(self, key: str, value: str):
        self._db[key] = value

    def get(self, key: str) -> Optional[str]:
        return self._db.get(key)


db = Database()


class DatabaseTestCase(unittest.TestCase):
    def test_db(self):
        db = Database()

        self.assertIsNone(db.get("a"))
        self.assertIsNone(db.get("b"))

        db.set("a", "A")
        self.assertEqual(db.get("a"), "A")
        self.assertIsNone(db.get("b"))
