
import os

from hashlib import sha3_256
from cryptography.hazmat.backends import default_backend

from labs.utils import (
    int_to_big,
    pad4
)

from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes
)

from labs.net.ecies.crypto import (
    generate_random,
    make_shared_secret,
    sha3_256_mac,
    kdf
)

AES = algorithms.AES    # aes
MODE = modes.CTR    # counter


def make_specific_keys(key):
    piece = len(key) // 2
    return key[:piece], key[piece:]


def encrypt(pubkey: bytes, data: bytes, shared=b''):

    # generate random number
    r, p = generate_random()    # random r, public p

    # shared secret s
    shared_secret = make_shared_secret(r, pubkey)

    # key derive
    key = kdf(shared_secret)
    enckey, mackey = make_specific_keys(key)
    mackey = sha3_256(mackey).digest()

    # encryption
    aes = AES(enckey)
    iv = os.urandom(len(r) // 2)    # 16bytes
    cipher = Cipher(aes, MODE(iv), default_backend()).encryptor()
    ctext = cipher.update(data) + cipher.finalize()

    # outputs
    body = iv + ctext
    body_length = pad4(int_to_big(len(body)))
    checksum = sha3_256_mac(mackey, body_length + body + shared)
    payload = [p, checksum, body_length, body]
    return b''.join(payload)

