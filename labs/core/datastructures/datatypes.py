
from labs.utils.serialize.datatypes import (
    integer,
    bytes_string,
    List
)

bytes32 = bytes_string.constructor(32)
hash32 = bytes_string.constructor(32, allowed=True)
address = bytes_string.constructor(20, allowed=True)
active32 = List(address)
signature = List(integer, 3)
