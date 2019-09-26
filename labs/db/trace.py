
from collections import OrderedDict
from itertools import count
from labs.exceptions import TraceError

from labs.utils.decorators import (
    to_dict,
    to_tuple,
)


class EventTrace(str):
    ...


INSERTED_KEY = EventTrace("key was inserted")
DELETED_KEY = EventTrace("key was deleted")
MISSING_KEY = EventTrace("key was missing")


class TraceTables:

    def __init__(self):
        self._tables = OrderedDict()
        self._sequence = count().__next__

    def trace(self) -> 'TraceDB':
        return TraceDB(self._tables.copy())

    def __setitem__(self, key, value):
        self._tables[key] = (value, self._sequence(), INSERTED_KEY)

    def __getitem__(self, key):
        value, seq, trace = self._tables.get(key, (-1, -1, MISSING_KEY))
        if trace in (DELETED_KEY, MISSING_KEY):
            raise TraceError(key, trace)
        return value

    def __delitem__(self, key):
        value, seq, trace = self._tables.get(key, (-1, -1, MISSING_KEY))
        if trace is not MISSING_KEY:
            self._tables[key] = (value, seq, DELETED_KEY)


class TraceDB:

    def __init__(self, tables=None):
        if not tables:
            tables = {}
        self._traceable = self._as_dict(tables, traceable=True)

    @to_tuple
    def apply(self, db, traceable=False):
        for key, values in self._traceable.items():
            value, trace = values

            if not trace and traceable:
                yield key, value, trace
            elif trace:
                db[key] = value

    @to_dict
    def _as_dict(self, tables, traceable):
        for idx, items in enumerate(tables.items()):
            key, (value, seq, trace) = items

            if idx != seq:
                reason = "index={}, sequence={}, trace={}, does not matched".format(idx, seq, trace)
                raise TraceError(key, reason)

            if trace is DELETED_KEY:
                if traceable:
                    yield key, (value, 0)
            elif trace is INSERTED_KEY:
                yield key, (value, 1)
            else:
                yield key, (value, -1)

    def error_keys(self):
        for key, values in self._traceable.items():
            value, trace = values
            if trace == -1:
                yield key

    def error_items(self):
        for key, values in self._traceable.items():
            value, trace = values
            if trace == -1:
                yield key, value

    def deleted_keys(self):
        for key, values in self._traceable.items():
            value, trace = values
            if not trace:
                yield key

    def deleted_items(self):
        for key, values in self._traceable.items():
            value, trace = values
            if not trace:
                yield key, value

    def pending_keys(self):
        for key, values in self._traceable.items():
            value, trace = values
            if trace == 1:
                yield key

    def pending_items(self):
        for key, values in self._traceable.items():
            value, trace = values
            if trace == 1:
                yield key, value

    def __getitem__(self, key):
        value, trace = self._traceable.get(key, (-1, MISSING_KEY))
        if trace in (DELETED_KEY, MISSING_KEY):
            raise TraceError(key, trace)
        return value


class Trace:

    def __init__(self, raw_db):
        self._raw_db = raw_db
        self._traceable = TraceTables()

    def reset(self):
        self._traceable = TraceTables()

    def make_traceable(self) -> 'TraceDB':
        return self._traceable.trace()

    def __setitem__(self, key: bytes, value: bytes):
        self._traceable[key] = value

    def __getitem__(self, key):
        try:
            value = self._traceable[key]
        except TraceError as error:
            key, reason, *_ = error.args
            if reason is DELETED_KEY:
                raise KeyError(key)
            value = self._raw_db[key]

        return value

    def __delitem__(self, key):
        del self._traceable[key]


