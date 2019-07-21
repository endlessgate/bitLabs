
from abc import (
    ABC,
    abstractmethod
)

from labs.utils.serialize import Serializer

from labs.core.datastructures.datatypes import (
    integer,
    bytes_string,
    address,
    signature
)


class BaseTransaction(Serializer, ABC):
    entries = [
        ('nonce', integer),
        ('value', integer),
        ('cost', integer),
        ('to', address),
        ('target', address),
        ('data', bytes_string),
        ('signature', signature)
    ]

    @property
    @abstractmethod
    def hash(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def sender(self):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def make(cls, nonce, cost, to, value, data=b''):
        raise NotImplementedError

    @abstractmethod
    def sign(self, privkey):
        raise NotImplementedError

    @abstractmethod
    def validate(self):
        raise NotImplementedError

    def __repr__(self):
        return '{}.{}'.format(self.__class__.__name__, str(self))

    def __str__(self):
        return 'Transaction(from:{}, {})'.format(self.sender, self.hash[2:10])


