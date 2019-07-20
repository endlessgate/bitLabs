
from abc import ABC

from labs.utils.serialize import Serializer

from labs.core.datastructures.datatypes import (
    integer,
    bytes32,
    hash32,
    active32
)


class BaseAccount(Serializer, ABC):
    entries = [
        ('nonce', integer),
        ('balance', integer),
        ('access', bytes32),
        ('storage_root', hash32),
        ('path', bytes32),
        ('active', active32)
    ]

    def __repr__(self):
        return 'Account(balance={}, nonce={}, storage=0x{}, path=0x{})'.format(self.balance,
                                                                               self.nonce,
                                                                               self.storage_root.hex(),
                                                                               self.path.hex())

