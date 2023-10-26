from typing import Optional


class Database:
    def __init__(self):
        self._db: dict[str, str] = {}

    def set(self, key: str, value: str):
        self._db[key] = value

    def get(self, key: str) -> Optional[str]:
        return self._db.get(key)
