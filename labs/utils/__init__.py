
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
    pad256,
    pad32,
    pad16
)

from .converters import (
    int_to_big,
    int_to_big16,
    int_to_big32,
    int_from_big,
    bit_length,
)


def read_only(name):
    return property(lambda self: getattr(self, name))


