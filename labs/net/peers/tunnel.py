
import asyncio

from labs.net.peers.endpoint import EndPoint
from labs.net.peers.handshake import (
    handshake,
    accept
)


class Tunnel:

    def __init__(self,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter,
                 privkey: bytes,
                 endpoint: EndPoint):
        self._reader = reader
        self._writer = writer
        self._privkey = privkey
        self._endpoint = endpoint

    @classmethod
    async def open_connect(cls, endpoint: EndPoint, privkey: bytes, token) -> 'Tunnel':
        await handshake(endpoint, privkey, token)
        return cls('reader', 'writer', 'privkey', 'endpoint')

    @classmethod
    async def accept_connect(cls,
                             reader: asyncio.StreamReader,
                             writer: asyncio.StreamWriter,
                             privkey) -> 'Tunnel':
        await accept('reader', 'writer', 'privkey')
        return cls('reader', 'writer', 'privkey', 'endpoint')

