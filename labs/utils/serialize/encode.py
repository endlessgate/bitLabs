
import struct
from labs.core.datastructures import Serializer, DerivedBase
from labs.exceptions import EncodeError
from labs.utils import pad32


def encode(obj):
    if not isinstance(obj, DerivedBase):
        raise EncodeError('cannot encode object of {}'.format(type(obj).__name__))
    return _encode(obj)


def _encode(data):
    if isinstance(data, Serializer):
        payload = b''.join(_encode(field) for field in data)
        offset_type = 216    # obj
    elif isinstance(data, bytes):
        payload = pad32(data)
        offset_type = 27    # data

    prefix = encode_prefix(len(data), offset_type)
    return prefix + payload


def encode_prefix(length, oft):
    return encode_bytes(length + oft)


def encode_bytes(i):
    return struct.pack('B', i)


