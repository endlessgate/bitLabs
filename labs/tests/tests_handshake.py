
import os

from hashlib import sha3_256
from labs.net import ecies
from labs.utils.keys import (
    encode_signature,
    decode_signature
)

from labs.utils.keys import recover
from labs.utils.keys.ecdsa import verifies
from labs.utils import (
    pad32,
    pad16,
    int_from_big,
    int_to_big
)


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
    seq = pad32(int_to_big(0))
    secret = sha3_256(shared_secret + nonce + seq).digest()

    s = my_ephem_keys.sign(secret)
    encode_sig = encode_signature(s)

    # 65, 65, 32, 4, 4
    # signature, public, nonce, version, suffix (170): handshake messages

    encode_payload = b''.join((seq,
                               encode_sig,
                               my_keys.public_bytes,
                               nonce, pad16(int_to_big(1)),
                               pad16(int_to_big(0))))
    cipher = ecies.encrypt(keys.public_bytes, encode_payload)

    # -------------------------------------------------------------------------------#

    # *-- accept --* #
    plain = ecies.decrypt(keys.private_bytes, cipher)
    if plain != encode_payload:
        raise ValueError('plain != payload')
    if len(plain) != 169:
        raise ValueError('payload size error', len(plain))

    # decode payload
    seqe = plain[:4]
    plain = plain[4:]
    accept_sig = plain[:65]
    accept_public = plain[65:129]
    accept_nonce = plain[129:161]
    ve, suff = plain[-4:-2], plain[-2:]

    if ve != b'\x00\x01':
        raise ValueError
    if suff != b'\x00\x00':
        raise ValueError

    # stranger private key, my public key = shared secret
    stranger_shared_secret = ecies.make_shared_secret(keys.private_bytes, accept_public)

    accept_secret = sha3_256(
        stranger_shared_secret + accept_nonce + seqe).digest()
    if accept_secret != secret:
        raise ValueError

    decode_sig = decode_signature(accept_sig)
    if s != decode_sig:
        raise ValueError

    accept_ephem_key = recover(accept_secret, decode_sig)
    handshake_sset = (accept_ephem_key, accept_nonce, accept_public)

    print('verifies:', verifies(
        accept_secret, decode_sig[:2], accept_ephem_key
    ))

    # $ exchange data, verify $ #

    # todo ... peer version, peer type, etc..........

    # $ heartbeat $ #


if __name__ == '__main__':
    handshake_flows()

