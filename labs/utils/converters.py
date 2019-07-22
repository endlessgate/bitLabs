
import binascii
from labs.utils import is_bytes


def bit_length(x: int):
    return x.bit_length()


def int_to_big(value: int):
    if hasattr(value, 'to_bytes'):
        return value.to_bytes((bit_length(value) + 7) // 8 or 1,
                              byteorder='big')
    else:
        raise ValueError("int to big, value expected integer, got {}".format(type(value).__name__))


def int_to_big16(value: int):
    if hasattr(value, 'to_bytes'):
        try:
            return value.to_bytes(2, byteorder='big')
        except OverflowError:
            raise ValueError("int to big16, value must be smaller than 65535, got {}".format(value))
    else:
        raise ValueError("int to big16, value expected integer, got {}".format(type(value).__name__))


def int_from_big(value: bytes):
    if not is_bytes(value):
        raise ValueError("int from big, expected bytes, got {}".format(type(value).__name__))
    return int(binascii.hexlify(value), 16)


