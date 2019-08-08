
from lru import LRU
from functools import wraps


def cached(func):
    @wraps(func)
    def wrapper(*args):
        store = func(*args)
        if store:
            key, value, *_ = args
            store[key] = value
        else:
            cls, key, value, *_ = args
            cls._cached[key] = value
    return wrapper


class Record:

    __slots__ = ('_db', '_cached', '_size')

    def __init__(self, db, size=1024):
        # hold 1024 items with cached
        self._db = db
        self._size = size
        self.realloc()

    def realloc(self):
        self._cached = LRU(self._size)

    @cached
    def __setitem__(self, key, value):
        self._db.put(key, value)

    def __getitem__(self, key):
        if key not in self._cached:
            self._cached[key] = self._db.get(key)
        return self._cached[key]

    def __delitem__(self, key):
        if key in self._cached:
            del self._cached[key]
        del self._db[key]

