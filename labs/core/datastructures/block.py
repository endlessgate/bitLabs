
from abc import (
    ABC,
    abstractmethod
)

from labs.core.datastructures import DerivedBase


class BaseBlock(DerivedBase, ABC):

    @property
    @abstractmethod
    def number(self):
        """
        Returns from block height
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def hash(self):
        raise NotImplementedError

    def __repr__(self):
        return 'Block(#{}, {})'.format(self.number, self.hash[2:10])

