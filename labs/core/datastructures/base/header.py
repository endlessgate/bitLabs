
from abc import (
    ABC,
    abstractmethod
)

from labs.utils.serialize import Serializer


class BaseHeader(Serializer, ABC):

    # __slots__ = ('previous_hash',
    #              'base',
    #              'number',
    #              'transaction_root',
    #              'state_root',
    #              'receipt_root',
    #              'timestamp',
    #              'cost_limit',
    #              'cost_used',
    #              'signature')

    @property
    @abstractmethod
    def hash(self):
        raise NotImplementedError

    def __repr__(self):
        return 'BlockHeader(#{}, {})'.format(self.number, self.hash[2:10])

