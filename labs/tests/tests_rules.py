
import labs.utils.serialize as rules
from labs.core.datastructures import AtomicStructure


class TestCase(AtomicStructure):

    __slots__ = ('name',
                 'hub')

    def hash(self): pass


def tests_encode():
    tc = TestCase(name=b'mynames', hub=b'mytests')
    return serializer.encode(tc)


def tests_decode(data: bytes):
    tc = serializer.decode(data, pack=TestCase)
    return tc


if __name__ == '__main__':
    a = tests_encode()
    print('encode:', a)
    b = tests_decode(a)
    print('decode: {}({}, {})'.format(type(b).__name__, b.name, b.hub))

