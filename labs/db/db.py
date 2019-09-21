
import plyvel

from labs.abstract.db import BaseDB
from labs.utils.checks import raise_diff_with_bytes


class DB(BaseDB):

    def __init__(self, path):
        self._db = plyvel.DB(
            path,
            create_if_missing=True
        )

    def write_batch(self, t=False):
        return self._db.write_batch(transaction=t)

    def __setitem__(self, key: bytes, value: bytes):
        raise_diff_with_bytes(key)
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
