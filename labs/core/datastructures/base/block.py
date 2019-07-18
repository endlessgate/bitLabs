
from abc import (
    ABC,
    abstractmethod
)

from labs.utils.serialize import Serializer


class BaseBlock(Serializer, ABC):

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
        return '<{}.{}>'.format(self.__class__.__name__, str(self))

    def __str__(self):
        return 'Block(#{}, {})'.format(self.number, self.hash[2:10])
