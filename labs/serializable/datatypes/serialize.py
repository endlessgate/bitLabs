
from abc import ABCMeta
from copy import deepcopy
from collections.abc import Sequence
from labs.exceptions import SerializationError
from labs.utils import to_tuple
from labs.serializable.datatypes import SerialPort


class Meta:
    names = None
    entries = None


class MetaSerialize(ABCMeta):
    def __new__(cls, name, bases, attrs):
        new = super(MetaSerialize, cls).__new__
        is_entry = 'entries' in attrs

        if is_entry:
            _entries = tuple(
                (slot, _type)
                for slot, _type
                in attrs.pop('entries')
            )

            attrs['__slots__'] = tuple(name for name, _ in _entries)
            attr_names, entries = zip(*_entries)

        else:
            return new(cls, name, bases, attrs)

        data_space = {
            'names': attr_names,
            'entries': SerialPort(entries)
        }

        meta_class = attrs.pop('_meta', Meta)
        meta = type(
            'Meta',
            (meta_class,),
            data_space
        )
        attrs['_meta'] = meta

        return new(cls, name, bases, attrs)


class Serialize(Sequence):
    # base class for data-structures
    def __init__(self, *args, **kwargs):
        if kwargs:
            data_space = self._merge(args, kwargs)
        else:
            data_space = args

        if len(self._meta.names) != len(data_space):
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

    @classmethod
    def serialize(cls, obj):
        return cls._meta.entries.serialize(obj)

    @classmethod
    def deserialize(cls, data):
        return cls._meta.entries.deserialize(data)

    def __iter__(self):
        for attr in self.__slots__:
            yield getattr(self, attr)

    def __getitem__(self, index):
        return getattr(self, self.__slots__[index])

    def __len__(self):
        return len(self.__slots__)

