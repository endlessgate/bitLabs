
import os

from hashlib import sha3_256
from labs.net import ecies
from labs.utils.keys import (
    encode_signature,
    decode_signature
)

from labs.utils.keys.ecdsa import recover
from labs.utils import int_from_big, int_to_big


def handshake_flows():

    # $ exchange keys $ #

    # peer private, public
    my_keys = ecies.generate_random()
    # ephemeral private, public
    my_ephem_keys = ecies.generate_random()

    # stranger key
    keys = ecies.generate_random()

    # *-- connect --* #

    # my private key, stranger public key = shared secret
    shared_secret = ecies.make_shared_secret(my_keys.private_bytes, keys.public_bytes)

    random = os.urandom(16)
    nonce = sha3_256(random).digest()
    secret = sha3_256(shared_secret + nonce).digest()

    s = my_ephem_keys.sign(secret)
    encode_sig = encode_signature(s)

    # 65, 65, 32, 4, 4
    # signature, public, nonce, version, suffix (170): handshake messages
    encode_payload = b''.join((encode_sig, my_keys.public_bytes, nonce, b'\x00\x00\x00\x01', b'\x00\x00\x00\x00'))
    cipher = ecies.encrypt(keys.public_bytes, encode_payload)

    # -------------------------------------------------------------------------------#

    # *-- accept --* #
    plain = ecies.decrypt(keys.private_bytes, cipher)
    if plain != encode_payload:
        raise ValueError('plain != payload')
    if len(plain) != 169:
        raise ValueError('payload size error')

    # decode payload
    accept_sig = plain[:65]
    accept_public = plain[65:129]
    accept_nonce = plain[129:161]
    ve, suff = plain[-8:-4], plain[-4:]

    if ve != b'\x00\x00\x00\x01':
        raise ValueError
    if suff != b'\x00\x00\x00\x00':
        raise ValueError

    # stranger private key, my public key = shared secret
    stranger_shared_secret = ecies.make_shared_secret(keys.private_bytes, accept_public)

    accept_secret = sha3_256(stranger_shared_secret + accept_nonce).digest()
    if accept_secret != secret:
        raise ValueError

    decode_sig = decode_signature(accept_sig)
    if s != decode_sig:
        raise ValueError

    accept_ephem_key = recover(accept_secret, decode_sig)
    handshake_sset = (accept_ephem_key, accept_nonce, accept_public)

    # $ exchange data, verify $ #

    # todo ... peer version, peer type, etc..........

    # $ heartbeat $ #


if __name__ == '__main__':
    handshake_flows()

