
import plyvel

from contextlib import contextmanager
from labs.abstract.db import BaseDB
from labs.utils.checks import raise_diff_with_bytes


class DB(BaseDB):

    def __init__(self, path):
        self._db = plyvel.DB(
            path,
            create_if_missing=True
        )

    @contextmanager
    def write_batch(self, t=False):
        with self._db.write_batch(transaction=t) as db:
            batch = WriteBatch(self._db, db)
            yield batch

    def __setitem__(self, key: bytes, value: bytes):
        raise_diff_with_bytes(key, value)
        self._db.put(key, value)

    def __getitem__(self, key: bytes):
        raise_diff_with_bytes(key)
        value = self._db.get(key)
        if not value:
            raise KeyError(key)
        return value

    def __contains__(self, key: bytes):
        raise_diff_with_bytes(key)
        return self._db.get(key) is not None


class WriteBatch:
    def __init__(self, db, batch):
        self._raw_db = db
        self._batch = batch

    def __setitem__(self, key, value):
        self._batch.put(key, value)

    def __getitem__(self, key):
        return self._raw_db[key]

    def __delitem__(self, key):
        self._batch.delete(key)

