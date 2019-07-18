
from .datatypes import Serialize, MetaSerialize


class Serializer(Serialize, metaclass=MetaSerialize):
    # base serializer
    pass

