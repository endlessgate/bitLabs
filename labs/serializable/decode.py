
from labs.utils import is_bytes
from labs.exceptions import DecodeError, PayloadError


def decode(data, pack=None):
    if not is_bytes(data):
        raise DecodeError('Decode only bytes, got {}'.format(type(data).__name__))

    fl, data, attrlen = decode_prefix(data)
    if attrlen != 33 * fl:
        raise PayloadError('Payload not enough {}'.format(data))

    return decode_payload(fl, data, pack)


def peek(index, data):
    return data[index:]


def decode_prefix(data):
    if data[0] > 216:
        length = data[0] - 216
        if length < 0:
            raise TypeError("Does not exists payload")
        return length, data[1:], len(data[1:])
    else:
        raise TypeError("Unexpected type {}".format(data[0]))


def decode_payload(fl, data, pack):
    attr_slots = []
    for x in range(fl):
        length = data[0] - 27
        value = data[1: 33].rsplit(b'\x00').pop()
        if len(value) != length:
            raise ValueError("Payload values length {}, got length {}".format(33, len(value)))
        attr_slots.append(
            value
        )
        data = peek(33, data)

    if pack:
        return pack(*attr_slots)

    return attr_slots

