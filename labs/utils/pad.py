
from labs.utils import is_bytes


def pad32(value: bytes) -> bytes:
    if not is_bytes(value):
        raise ValueError("pad32, expected bytes, got {}".format(type(value).__name__))
    return value.rjust(32, b'\x00')

