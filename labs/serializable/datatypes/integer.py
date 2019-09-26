
from labs.exceptions import SerializationError
from labs.utils import (
    int_to_big,
    int_from_big,
    is_integer
)


class Integer:
    """ byteorder = 'big-endian'
    """
    def __init__(self, size=None):
        self.size = size

    def constructor(self, size):
        return type(self)(size)

    def has_size(self, data):
        if self.size is not None:
            return b'\x00' * max(0, self.size - len(data)) + data
        else:
            return data

    def serialize(self, obj):
        if not is_integer(obj):
            raise SerializationError('serialize only integer, {}'.format(type(obj).__name__))

        if obj > 0:
            data = int_to_big(obj)
        elif obj == 0:
            data = b'\x00'
        else:
            raise SerializationError('Cannot serialize, deny of integer, {}'.format(obj))
        return self.has_size(data)

    def deserialize(self, data):
        return int_from_big(data)


integer = Integer()
