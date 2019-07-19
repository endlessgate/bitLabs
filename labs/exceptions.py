

class SerializationError(Exception):
    pass


class DeSerializationError(Exception):
    pass


class EncodeError(Exception):
    pass


class PayloadError(Exception):
    pass


class DecodeError(Exception):
    pass


class InvalidKeys(Exception):
    def __init__(self, name, errors):
        self.name = name
        self.errors = errors

    def __str__(self):
        return "InvalidKeys(type: {}, {})".format(self.name, self.errors)

