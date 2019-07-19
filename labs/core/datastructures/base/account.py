
from abc import ABC

from labs.utils.serialize import Serializer
from labs.utils.serialize.datatypes import (
    integer,
    List
)

from .datatypes import (
    bytes32,
    root32
)


class BaseAccount(Serializer, ABC):
    entries = [
        ('nonce', integer),
        ('balance', integer),
        ('storage_root', root32),
        ('path', bytes32),
        ('active', List(bytes32))
    ]

    def __repr__(self):
        return 'Account(balance={}, nonce={})'.format(self.balance, self.nonce)

