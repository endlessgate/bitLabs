
from labs.core.datastructures import Serializer


class BlockHeader(Serializer):

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

    def hash(self):
        pass

