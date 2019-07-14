
from labs.core.datastructures import AtomicStructure


class Block(AtomicStructure):

    @property
    def number(self):
        return 0

    @property
    def hash(self):
        return ''

    def __repr__(self):
        return 'Block({}@{})'.format(self.number, self.hash[2:10])

