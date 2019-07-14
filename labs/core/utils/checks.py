
types_bytes = (bytes, bytearray)
types_int = int
types_str = str
types_strings = (str, bytes, bytearray)


def is_bytes(value) -> bool:
    return isinstance(value, types_bytes)


def is_integer(value) -> bool:
    return isinstance(value, types_int)


def is_str(value) -> bool:
    return isinstance(value, types_str)


def is_strings(value) -> bool:
    return isinstance(value, types_strings)

