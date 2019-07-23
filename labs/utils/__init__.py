
from .decorators import (
    to_dict,
    to_list,
    to_tuple,
    to_set,
)

from .checks import (
    is_bytes,
    is_integer,
    is_str,
    is_strings,
    is_bool,
)

from .pad import (
    pad32,
    pad4,
)

from .converters import (
    int_to_big,
    int_to_big16,
    int_from_big,
    bit_length,
)


def read_only(name):
    return property(lambda self: getattr(self, name))


