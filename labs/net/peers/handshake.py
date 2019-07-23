
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


if __name__ == '__main__':
    # peer private, public
    priv, pub = ecies.generate_random()

    # ephemeral private, public
    r, p = ecies.generate_random()

    peer_key_shared_secret = ecies.make_shared_secret(priv, pub)

    random = os.urandom(16)
    nonce = sha3_256(random).digest()
    # todo: ecdsa first
    # create... pending

