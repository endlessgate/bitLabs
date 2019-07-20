
from abc import (
    ABC,
    abstractmethod
)

from labs.utils.serialize import Serializer

from labs.core.datastructures.datatypes import (
    integer,
    bytes_string,
    hash32,
    bytes32,
    address,
    signature
)


class BaseHeader(Serializer, ABC):
    entries = [
        ('previous_hash', bytes32),
        ('number', integer),
        ('base', address),
        ('transaction_root', hash32),
        ('seal_root', hash32),
        ('state_root', hash32),
        ('receipt_root', hash32),
        ('cost_limit', integer),
        ('cost_used', integer),
        ('creation_time', integer),
        ('extra', bytes_string),
        ('signature', signature)
    ]

    @property
    @abstractmethod
    def hash(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def is_genesis(self):
        raise NotImplementedError

    def __repr__(self):
        return 'BlockHeader(#{}, {})'.format(self.number, self.hash[2:10])

