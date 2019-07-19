
from labs.utils import is_bool

from labs.exceptions import (
    SerializationError,
    DeSerializationError
)


class Boolean:

    def serialize(self, obj):
        if not is_bool(obj):
            raise SerializationError('serialize only boolean, {}'.format(type(obj).__name__))

        if obj is True:
            return b'\x01'
        elif obj is False:
            return b'\x00'
        else:
            raise SerializationError('serialize only boolean, {}'.format(obj))

    def deserialize(self, data):
        is_valid = any((data == b'\x00', data == b'\x01'))
        if not is_valid:
            raise DeSerializationError('deserialize only boolean, {}'.format(data))

        if data == b'\x00':
            return False
        elif data == b'\x01':
            return True
        else:
            raise DeSerializationError('deserialize only boolean, {}'.format(data))


boolean = Boolean()
