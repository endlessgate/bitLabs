
from labs.core.datastructures import DerivedBase


class Transaction(DerivedBase):

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

