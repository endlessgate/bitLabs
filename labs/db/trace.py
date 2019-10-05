
from itertools import count
from labs.exceptions import TraceError

from labs.utils.decorators import (
    to_dict,
    to_tuple,
)


class EventTrace(str):
    ...


INSERTED_KEY = EventTrace("key was inserted")
CHANGED_KEY = EventTrace("key was changed")
DELETED_KEY = EventTrace("key was deleted")
MISSING_KEY = EventTrace("key was missing")


class TraceDB:

    def __init__(self, raw_db):
        self._raw_db = raw_db
        self._traceable = Trace()

    def reset(self):
        self._traceable = Trace()

    def make_traceable(self) -> 'TraceBatch':
        return self._traceable.trace()

    def __setitem__(self, key: bytes, value: bytes):
        self._traceable[key] = value

    def __getitem__(self, key):
        try:
            value = self._traceable[key]
        except TraceError as error:
            key, reason, *_ = error.args
            if reason in (DELETED_KEY, CHANGED_KEY):
                raise KeyError(key)
            value = self._raw_db[key]

        return value

    def __delitem__(self, key):
        del self._traceable[key]


class IndexTable(dict):

    def __setitem__(self, key, value):
        if key not in self:
            data = {key: (value, )}
            self.update(data)
        else:
            values = self.get(key)
            data = {key: values + (value, )}
            self.update(data)


class Trace:

    def __init__(self):
        self._index = IndexTable()
        self._traceable = {}
        self._sequence = count().__next__

    def trace(self) -> 'TraceBatch':
        return TraceBatch(self._as_dict())

    @to_dict
    def _as_dict(self):
        for k, v in self._index.items():
            values = []
            for index in v:
                values.append(self._traceable[index])
            yield k, values

    def _get_index(self, key):
        index = self._index.get(key, MISSING_KEY)
        if index is MISSING_KEY:
            raise TraceError(key, index)
        return index[-1]

    def __setitem__(self, key, value):
        index = self._sequence()
        if key not in self._index:
            self._traceable[index] = (value, INSERTED_KEY)
        else:
            change_index = self._get_index(key)
            change_value, trace = self._traceable[change_index]
            if trace is DELETED_KEY:
                raise TraceError(key, trace)

            self._traceable[change_index] = (change_value, CHANGED_KEY)
            self._traceable[index] = (value, INSERTED_KEY)

        self._index[key] = index

    def __getitem__(self, key):
        index = self._get_index(key)
        value, trace = self._traceable.get(index, (-1, MISSING_KEY))
        if trace in (DELETED_KEY, CHANGED_KEY, MISSING_KEY):
            raise TraceError(key, trace)
        return value

    def __delitem__(self, key):
        index = self._get_index(key)
        value, trace = self._traceable.get(key, (-1, -1, MISSING_KEY))
        if trace is INSERTED_KEY:
            self._traceable[index] = (value, DELETED_KEY)


class TraceBatch:

    def __init__(self, tables=None):
        if not tables:
            tables = {}
        self._trace_batch = tables

    @to_tuple
    def apply(self, db):
        for key, value in self.pending_items():
            db[key] = value

    def changed_keys(self):
        for key, trace_set in self._trace_batch.items():
            for value, trace in trace_set:
                if trace is CHANGED_KEY:
                    yield key

    def changed_items(self):
        for key, trace_set in self._trace_batch.items():
            for value, trace in trace_set:
                if trace is CHANGED_KEY:
                    yield key, value

    def deleted_keys(self):
        for key, trace_set in self._trace_batch.items():
            for value, trace in trace_set:
                if trace is DELETED_KEY:
                    yield key

    def deleted_items(self):
        for key, trace_set in self._trace_batch.items():
            for value, trace in trace_set:
                if trace is DELETED_KEY:
                    yield key, value

    def pending_keys(self):
        for key, trace_set in self._trace_batch.items():
            value, trace = trace_set[-1]
            if trace is INSERTED_KEY:
                yield key
            else:
                raise TraceError(key, trace)

    def pending_items(self):
        for key, trace_set in self._trace_batch.items():
            value, trace = trace_set[-1]
            if trace is INSERTED_KEY:
                yield key, value
            else:
                raise TraceError(key, trace)

