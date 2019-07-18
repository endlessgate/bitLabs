
from labs.exceptions import SerializationError
from labs.utils import int_to_big, int_from_big


class Integer:
    """ byteorder = 'big-endian'
    """

    @classmethod
    def serialize(cls, obj):
        if not isinstance(obj, int):
            raise SerializationError('serialize only integer, {}'.format(type(obj).__name__))

        if obj > 0:
            data = int_to_big(obj)
        elif obj == 0:
            data = b'\x00'
        else:
            raise SerializationError('Cannot serialize, deny of integer, {}'.format(obj))
        return data

    @classmethod
    def deserialize(cls, data):
        return int_from_big(data)


integer = Integer

