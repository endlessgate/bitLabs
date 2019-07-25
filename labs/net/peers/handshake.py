
import asyncio
import os

from hashlib import sha3_256
from labs.net import ecies
from labs.net.peers.endpoint import EndPoint


async def handshake(endpoint: EndPoint, privkey: bytes, token):
    reader, writer = await token.cancellable_wait(
        asyncio.open_connection(host=endpoint.address.ip_address,
                                port=endpoint.address.stream_port),
        timeout=3
    )
    ephem_privkey, ephem_pubkey = ecies.generate_random()
    return


async def accept(reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter,
                 privkey: bytes):
    pass

