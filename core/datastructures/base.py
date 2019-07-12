
from copy import deepcopy
from abc import ABC, abstractmethod
from exceptions import UnexpectedStructures
from decorators import to_tuple


class Serializer(ABC):
    # base class for data-structures
    def __init__(self, *args, **kwargs):
        if kwargs:
            data_space = self._merge(args, kwargs)
        else:
            data_space = args

        if len(self.__slots__) != len(data_space):
            raise UnexpectedStructures("Expected args({}), "
                                       "Got args({})".format(
                                        len(self.__slots__), len(data_space)))

    @to_tuple
    def _merge(self, args, kwargs):
        freeze_space = self.__slots__[len(args):]
        yield from args
        for name in freeze_space:
            yield kwargs[name]

    def copy(self, **kwargs):
        unset = set(self.__slots__).difference(kwargs.keys())
        keep_space = {
            key: deepcopy(getattr(self, key))
            for key in unset
        }
        class_kwargs = dict(**keep_space, **kwargs)
        return type(self)(**class_kwargs)

    @abstractmethod
    def hash(self):
        raise NotImplementedError("data-structures: method not implement")

