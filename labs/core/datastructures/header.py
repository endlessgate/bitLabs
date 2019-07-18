
from labs.core.datastructures import DerivedBase


class BlockHeader(DerivedBase):

    __slots__ = ('previous_hash',
                 'base',
                 'number',
                 'transaction_root',
                 'state_root',
                 'receipt_root',
                 'timestamp',
                 'cost_limit',
                 'cost_used',
                 'signature')

    @property
    def hash(self):
        return ''

    def __repr__(self):
        return 'BlockHeader(#{}, {})'.format(self.number, self.hash[2:10])

