
import ipaddress
from labs.utils import (
    read_only,
    int_to_big16,
    int_from_big
)


class IPAddress:
    def __init__(self, address: str, stream_port: bytes, datagram_port: bytes):
        self._ip_address = ipaddress.ip_address(address)
        self._stream_port = stream_port
        self._datagram_port = datagram_port

    ip_address = read_only('_ip_address')

    @property
    def stream_port(self):
        return int_from_big(self._stream_port)

    @property
    def datagram_port(self):
        return int_from_big(self._datagram_port)

    @property
    def pack(self):
        return (self.ip_address,
                self.stream_port,
                self.datagram_port)

    @classmethod
    def make(cls, address: str, stream_port: int, datagram_port: int):
        return cls(address,
                   int_to_big16(stream_port),
                   int_to_big16(datagram_port))


class EndPoint:

    def __init__(self, pubkey: bytes, address: IPAddress):
        self.address = address
        self.pubkey = pubkey

    @classmethod
    def make(cls, pubkey: bytes, address: str, stream_port: int, datagram_port: int = 0):
        address = IPAddress.make(address, stream_port, datagram_port)
        return cls(pubkey, address)

    def __str__(self):
        return '0x{}, {}'.format(self.pubkey.hex()[:20], self.address.ip_address)

    def __repr__(self):
        return 'EndPoint({}:{})'.format(str(self), self.address.stream_port)

    # todo: kd

