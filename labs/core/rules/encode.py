
import struct
from labs.core.datastructures import Serializer, AtomicStructure
from labs.exceptions import EncodeError


def encode(obj):
    if not isinstance(obj, AtomicStructure):
        raise EncodeError('cannot encode object of {}'.format(type(obj).__name__))
    return _encode(obj)


def _encode(data):
    if isinstance(data, Serializer):
        payload = b''.join(_encode(field) for field in data)
        offset_type = 216    # obj
    elif isinstance(data, bytes):
        payload = data.rjust(32, b'\x00')
        offset_type = 27    # data

    prefix = encode_prefix(len(data), offset_type)
    return prefix + payload


def encode_prefix(length, oft):
    return encode_bytes(length + oft)


def encode_bytes(i):
    return struct.pack('B', i)


