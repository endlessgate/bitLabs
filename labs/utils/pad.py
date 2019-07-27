
from labs.utils import is_bytes


def has_padding(value):
    if not is_bytes(value):
        raise ValueError("padding, expected bytes, got {}".format(type(value).__name__))


def pad256(value: bytes) -> bytes:
    has_padding(value)
    return value.rjust(32, b'\x00')


def pad32(value: bytes) -> bytes:
    has_padding(value)
    return value.rjust(4, b'\x00')


def pad16(value: bytes) -> bytes:
    has_padding(value)
    return value.rjust(2, b'\x00')
