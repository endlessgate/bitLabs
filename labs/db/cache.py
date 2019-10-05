
from lru import LRU
from labs.abstract.db import BaseDB


class RecordDB(BaseDB):

    def __init__(self, db: BaseDB, size=1024):
        self._db = db
        self._size = size
        self._cached = LRU(self._size)

    def reset(self):
        self._cached.clear()

    def __setitem__(self, key, value):
        self._cached[key] = value
        self._db[key] = value

    def __getitem__(self, key):
        if key not in self._cached:
            self._cached[key] = self._db[key]
        return self._cached[key]

    def __contains__(self, key):
        return key in self._cached

