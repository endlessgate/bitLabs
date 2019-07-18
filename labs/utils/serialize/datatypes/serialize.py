
from labs.utils import to_list
from labs.exceptions import SerializationError


def has_serialize(obj):
    return hasattr(obj, 'serialize') and hasattr(obj, 'deserialize')


class Serialize(list):

    def __init__(self, objs):
        super(Serialize, self).__init__()
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



