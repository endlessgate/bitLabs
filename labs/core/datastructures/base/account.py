
from abc import ABC
from labs.utils.serialize import Serializer


class BaseAccount(Serializer, ABC):

    def __repr__(self):
        return 'Account(balance={}, nonce={})'.format(self.balance, self.nonce)

