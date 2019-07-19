
import math
from labs.exceptions import (
    SerializationError,
    DeSerializationError
)

from labs.utils import is_str


class String:

    def __init__(self, minsize=None, maxsize=None, allowed=False, encoding='utf-8'):
        self.minsize = minsize or 0
        self.maxsize = maxsize or math.inf
        self.allowed = allowed
        self.encoding = encoding

    def constructor(self, size, allowed=False, encoding='utf-8'):
        return type(self)(size, size, allowed, encoding)

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
        if not is_str(obj):
            raise SerializationError('serialize only string, {}'.format(type(obj).__name__))
        return self.has_size(obj).encode(self.encoding)

    def deserialize(self, data):
        if not is_str(data):
            raise DeSerializationError('serialize only string, {}'.format(type(data).__name__))
        try:
            decode_string = data.decode(self.encoding)
        except UnicodeDecodeError as err:
            raise DeSerializationError(str(err), data)
        return self.has_size(decode_string)


string = String()
