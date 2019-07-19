
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


my_test_pub = b'\x04#\xbf\x1a\x84\xb73\xab`\xa3\x91\xed\xee\x82+n\xb9\xd5\xc9A\xa1\x9c\xfd\xe8r\x1cwy\xdc\xefG\xe0\xea\xbc\xa2\xc0D}\x06b)X\xe7\\\xda\xaa\xc36\xd0\x16\xef\x83\xa3\x02\x17\xf6\x93\xc0F\x81\x0f;\xc9NV'
a = encrypt(my_test_pub, data=b'halmony')
print(a)
