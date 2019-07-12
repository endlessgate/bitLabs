
from core.datastructures import Serializer


class Transaction(Serializer):

    __slots__ = ('nonce',
                 'to',
                 'value',
                 'cost',
                 'target',
                 'data',
                 'signature')

    def hash(self):
        pass

