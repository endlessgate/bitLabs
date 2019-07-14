
from labs.core.datastructures import Serializer


class Account(Serializer):

    __slots__ = ('nonce',
                 'balance',
                 'storage',
                 'path')

    def __repr__(self):
        return 'Account(balance={}, nonce={})'.format(self.balance, self.nonce)


