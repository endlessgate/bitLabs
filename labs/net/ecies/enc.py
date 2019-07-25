
import os

from hashlib import sha3_256
from cryptography.hazmat.backends import default_backend

from labs.utils import (
    int_to_big,
    pad4
)

from labs.exceptions import (
    InvalidKeys,
    PayloadError
)

from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes
)

from labs.net.ecies.crypto import (
    make_specific_keys,
    generate_random,
    make_shared_secret,
    sha3_256_mac,
    kdf
)

AES = algorithms.AES    # aes
MODE = modes.CTR    # counter


def encode_payload(body, mackey, shared, pubkey):
    body_size = pad4(int_to_big(len(body)))
    checksum = sha3_256_mac(mackey, body + body_size + shared)
    payload = [b'\x04' + pubkey, checksum, body, body_size]
    return b''.join(payload)


def encrypt(pubkey: bytes, data: bytes, shared=b'') -> bytes:

    # generate random number
    keys = generate_random()    # random r, public p

    # shared secret s
    try:
        shared_secret = make_shared_secret(keys.private_bytes, pubkey)
    except InvalidKeys as err:
        raise PayloadError(str(err))

    # key derive
    key = kdf(shared_secret)
    enckey, mackey = make_specific_keys(key)
    mackey = sha3_256(mackey).digest()

    # encryption
    aes = AES(enckey)
    iv = os.urandom(len(mackey) // 2)    # 16bytes
    cipher = Cipher(aes, MODE(iv), default_backend()).encryptor()
    ctext = cipher.update(data) + cipher.finalize()

    # outputs
    body = iv + ctext
    return encode_payload(body, mackey, shared, keys.public_bytes)

