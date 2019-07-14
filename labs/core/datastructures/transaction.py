
from labs.core.datastructures import AtomicStructure


class Transaction(AtomicStructure):

    __slots__ = ('nonce',
                 'to',
                 'value',
                 'cost',
                 'target',
                 'data',
                 'signature')

    @property
    def hash(self):
        return ''

