
import math

from labs.utils import is_bytes

from labs.exceptions import (
    SerializationError,
    DeSerializationError
)


class BytesString:

    def __init__(self, minsize=None, maxsize=None, allowed=False):
        self.minsize = minsize or 0
        self.maxsize = maxsize or math.inf
        self.allowed = allowed

    def constructor(self, size, allowed=False):
        return type(self)(size, size, allowed)

    def has_size(self, data):
        size = len(data)
        is_valid = any((
            self.minsize <= size <= self.maxsize,
            self.allowed and size == 0
        ))

        if not is_valid:
            raise SerializationError('serialize invalid size, expected size {}, got {}'
                                     .format(self.minsize, len(data)))
        return data

    def serialize(self, obj):
        if not is_bytes(obj):
            raise SerializationError('serialize only bytes-string, {}'.format(type(obj).__name__))
        return self.has_size(obj)

    def deserialize(self, data):
        if not is_bytes(data):
            raise DeSerializationError('deserialize only bytes-string, {}'.format(type(data).__name__))
        return self.has_size(data)


bytes_string = BytesString()
