
from labs.core.datastructures.base import BaseTransaction


class Transaction(BaseTransaction):

    @property
    def hash(self):
        pass

    @property
    def sender(self):
        pass

    @classmethod
    def make(cls, nonce, cost, to, value, data=b''):
        pass

    def sign(self, privkey):
        pass

    def validate(self):
        pass


