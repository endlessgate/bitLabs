
from labs.utils import to_list
from labs.exceptions import (
    SerializationError,
    DeSerializationError
)

def has_serialize(obj):
    return hasattr(obj, 'serialize') and hasattr(obj, 'deserialize')


class SerialPort(list):

    def __init__(self, objs):
        super(SerialPort, self).__init__()
        for obj in objs:
            if has_serialize(obj):
                self.append(obj)
            else:
                raise TypeError('object has not serialize')

    @to_list
    def serialize(self, obj):
        if len(self) != len(obj):
            raise SerializationError('object length does not matched, '
                                     'Serialize({}), Object({})'
                                     .format(len(self), len(obj)))

        for value, props in zip(obj, self):
            yield props.serialize(value)

    @to_list
    def deserialize(self, obj):
        if len(self) != len(obj):
            raise DeSerializationError('object length does not matched, '
                                       'DeSerialize({}), Object({})'
                                       .format(len(self), len(obj)))

        for props, value in zip(self, obj):
            yield props.deserialize(value)

