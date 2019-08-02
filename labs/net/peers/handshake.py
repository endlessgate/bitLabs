
import asyncio
import os

from hashlib import sha3_256
from labs.net import ecies
from labs.net.peers.endpoint import EndPoint
from labs.net.peers.secret import Secret

from labs.utils.keys import (
    encode_signature,
    decode_signature,
    recover
)

from labs.utils import (
    pad16,
    pad32,
    int_to_big16,
    int_to_big32,
    int_from_big
)


def encode_payload(*args):
    payload = b''.join(args)
    if len(payload) != 169:
        raise ValueError('handshake payload size error, got {}'.format(len(payload)))
    return payload


def decode_payload(payload):
    accept_sig = payload[:65]
    accept_public = payload[65:129]
    accept_random = payload[129:161]
    return accept_random, accept_public, accept_sig


async def open_handshake(endpoint: EndPoint, keys, token):
    reader, writer = await token.cancellable_wait(
        asyncio.open_connection(host=endpoint.address.ip_address,
                                port=endpoint.address.stream_port),
        timeout=3
    )
    await _handshake_shared_secret(reader,
                                   writer,
                                   endpoint,
                                   keys,
                                   token)

    return


async def accept_handshake(reader: asyncio.StreamReader,
                           writer: asyncio.StreamWriter,
                           keys,
                           cipher: bytes):
    exchange_random, ephem_pubkey, pubkey = _accept_decode_secret(keys, cipher)

    address, port, *_ = writer.get_extra_info('peername')
    endpoint = EndPoint.make(pubkey, address, port)

    # responder [keys, endpoint, token, (bool) got eip8]

    random = os.urandom(16)
    random_secret = sha3_256(random).digest()
    sequence = pad32(int_to_big32(1))

    ephemeral_keys = ecies.generate_random()
    payload = encode_payload(sequence,
                             ephemeral_keys.public_bytes,
                             random_secret)

    cipher = ecies.encrypt(payload, pubkey)


    return endpoint


async def _handshake_shared_secret(reader: asyncio.StreamReader,
                                   writer: asyncio.StreamWriter,
                                   endpoint: EndPoint,
                                   keys,
                                   token):
    ephemeral_keys = ecies.generate_random()

    shared_secret = ecies.make_shared_secret(keys.private_bytes, endpoint.pubkey)
    random = os.urandom(16)
    random_secret = sha3_256(random).digest()
    sequence = pad32(int_to_big32(0))

    exchange_secret = sha3_256(
        shared_secret + random_secret + sequence
    ).digest()

    sig = ephemeral_keys.sign(exchange_secret)
    encode_sig = encode_signature(sig)

    # --- temporary
    version = pad16(int_to_big16(1))
    handshake_suffix = pad16(int_to_big16(0))
    # --------------------------------------------- #

    payload = encode_payload(sequence,
                             encode_sig,
                             keys.public_bytes,
                             random_secret,
                             version,
                             handshake_suffix)

    cipher = ecies.encrypt(ephemeral_keys.public_bytes, payload)

    if writer.is_closing():
        raise ConnectionError('during open_connection handling, connection closed')

    writer.write(cipher)
    await writer.drain()

    token.cancellable_wait(reader.read(169), timeout=5)

    if reader.at_eof():
        raise ConnectionError('disconnected')


def _accept_decode_secret(keys, cipher):
    payload = ecies.decrypt(keys.private_bytes, cipher)
    raw_seq = payload[:4]
    raw_ver, raw_suf = payload[-4:-2], payload[-2:]

    # expected exception: not bytes, decode
    version = int_from_big(raw_ver)
    suffix = int_from_big(raw_suf)
    sequence = int_from_big(raw_seq)
    has_accept = all((version == 1, suffix == 0, sequence == 0))

    if not has_accept:
        raise ValueError('during accept handling, unexpected payload')

    random, pubkey, sig = decode_payload(payload[4:])
    shared_secret = ecies.make_shared_secret(keys.private_bytes, pubkey)

    exchange_secret = sha3_256(
        shared_secret + random + sequence
    ).digest()

    decode_sig = decode_signature(sig)
    accept_ephemeral_key = recover(exchange_secret, decode_sig)

    # ---- #

    return random, accept_ephemeral_key, pubkey




