
from abc import (
    ABC,
    abstractmethod
)

from labs.utils.serialize import Serializer


class BaseTransaction(Serializer, ABC):
    entries = [
        ()
    ]

    # __slots__ = ('nonce',
    #              'to',
    #              'value',
    #              'cost',
    #              'target',
    #              'data',
    #              'signature')

    @property
    @abstractmethod
    def hash(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def sender(self):
        raise NotImplementedError

    def __repr__(self):
        return '{}.{}'.format(self.__class__.__name__, str(self))

    def __str__(self):
        return 'Transaction(from:{}, {})'.format(self.sender, self.hash[2:10])


