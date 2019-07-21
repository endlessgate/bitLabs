
import asyncio

from labs.net.peers.handshake import (
    handshake,
    accept
)


class Tunnel:

    def __init__(self,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter,
                 privkey,
                 endpoint):

        self._reader = reader
        self._writer = writer
        self._privkey = privkey
        self._endpoint = endpoint

    @classmethod
    async def open_connect(cls, endpoint, privkey) -> 'Tunnel':
        await handshake('endpoint', 'privkey')
        return cls('reader', 'writer', 'privkey', 'endpoint')

    @classmethod
    async def accept_connect(cls,
                             reader: asyncio.StreamReader,
                             writer: asyncio.StreamWriter,
                             privkey) -> 'Tunnel':
        await accept('reader', 'writer', 'privkey')
        return cls('reader', 'writer', 'privkey', 'endpoint')

