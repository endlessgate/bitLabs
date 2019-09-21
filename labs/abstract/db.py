
from abc import (
    ABC,
    abstractmethod
)


class BaseDB(ABC):

    @abstractmethod
    def __setitem__(self, key, value):
        ...

    @abstractmethod
    def __getitem__(self, key):
        ...

    @abstractmethod
    def __contains__(self, key):
        ...


