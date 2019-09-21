
from labs.abstract.db import BaseDB


class Record(BaseDB):

    def __init__(self, db: BaseDB):
        self._db = db
        self._batch = db.write_batch()

    def write(self):
        self._batch.write()

    def __setitem__(self, key, value):
        self._batch.put(key, value)

    def __getitem__(self, key):
        return self._db[key]

    def __contains__(self, key):
        return key in self._db

