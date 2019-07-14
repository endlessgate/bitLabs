
from copy import deepcopy
from collections.abc import Sequence
from abc import ABC, abstractmethod
from labs.exceptions import SerializationError
from labs.core.utils import to_tuple


class Serializer(Sequence):
    # base class for data-structures
    def __init__(self, *args, **kwargs):
        if kwargs:
            data_space = self._merge(args, kwargs)
        else:
            data_space = args

        if len(self.__slots__) != len(data_space):
            raise SerializationError("Expected args({}), "
                                     "Got args({})".format(
                                      len(self.__slots__), len(data_space)))

        for attr, value in zip(self.__slots__, data_space):
            setattr(self, attr, value)

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

    def serialize(self):
        pass

    @classmethod
    def deserialize(cls, items):
        pass

    def __iter__(self):
        for attr in self.__slots__:
            yield getattr(self, attr)

    def __getitem__(self, index):
        return getattr(self, self.__slots__[index])

    def __len__(self):
        return len(self.__slots__)


class AtomicStructure(Serializer, ABC):

    @property
    @abstractmethod
    def hash(self):
        raise NotImplementedError



