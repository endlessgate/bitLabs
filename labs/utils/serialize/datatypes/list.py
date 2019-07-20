
import math
from labs.utils import to_list
from labs.exceptions import (
    SerializationError,
    DeSerializationError
)


def has_serialize(obj):
    return hasattr(obj, 'serialize') and hasattr(obj, 'deserialize')


class List:

    def __init__(self, props, size=None):
        if not has_serialize(props):
            raise TypeError('list element not included, serialize and deserialize')
        self.props = props
        self.size = size or math.inf

    def constructor(self, props, size):
        return type(self)(props, size)

    @to_list
    def serialize(self, obj):
        is_valid = any((
            self.size and len(obj) == 0,
            len(obj) == self.size
        ))
        if not is_valid:
            raise SerializationError('invalid elements, expected size {}, got {}, {}'
                                     .format(self.size, len(obj), obj))

        for element in obj:
            yield self.props.serialize(element)

    @to_list
    def deserialize(self, data):
        for counter, element in enumerate(data):
            is_valid = any((
                self.size and counter == 0,
                counter <= self.size
            ))
            if not is_valid:
                raise DeSerializationError('invalid elements, count {}, {}'.format(counter, element))

            yield self.props.deserialize(element)


