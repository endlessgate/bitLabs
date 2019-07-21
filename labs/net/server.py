
import asyncio
from abc import ABC
from .peers import Tunnel

expected_errors = (
    TimeoutError,
    ConnectionRefusedError
)


class BaseListener(ABC):

    def __init__(self,
                 port: int,
                 ):
        self.port = port
        self._listener = None

    async def start_listener(self):
        self._listener = await asyncio.start_server(
            self.accept_handler,
            host='0.0.0.0',
            port=self.port
        )

    async def accept_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            await self._handshake(reader, writer)
        except expected_errors:
            self.disconnect(reader, writer)
        except Exception as err:
            print(err)
            self.disconnect(reader, writer)

    async def _handshake(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        # todo - stranger connection handshake, encryption schemes
        tunnel = Tunnel.accept_connect(reader, writer, 'privkey')

    def disconnect(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        if not reader.at_eof():
            reader.feed_eof()
        writer.close()


