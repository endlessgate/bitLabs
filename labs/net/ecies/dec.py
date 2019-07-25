
from hashlib import sha3_256

from cryptography.hazmat.backends import default_backend

from labs.exceptions import (
    InvalidKeys,
    PayloadError
)

from labs.utils import (
    int_from_big
)

from labs.net.ecies.crypto import (
    make_shared_secret,
    make_specific_keys,
    sha3_256_mac,
    kdf
)

from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes
)

AES = algorithms.AES    # aes
MODE = modes.CTR    # counter


def has_checksum(checksum, key, data):
    return checksum == sha3_256_mac(key, data)


def decode_payload(data):
    pubkey_len = 65
    enter_shared = data[:pubkey_len]
    size = -1 * (int_from_big(data[-4:]) + 4)
    checksum = data[pubkey_len:size]
    body = data[size:]
    return enter_shared, checksum, body


def decrypt(privkey: bytes, data: bytes, shared=b'') -> bytes:
    if data[:1] != b'\x04':
        raise PayloadError("unexpected header")

    enter_shared, checksum, body = decode_payload(data)
    try:
        shared_secret = make_shared_secret(privkey, enter_shared[1:])
    except InvalidKeys as err:
        raise PayloadError(str(err))

    key = kdf(shared_secret)
    enckey, mackey = make_specific_keys(key)
    mackey = sha3_256(mackey).digest()

    if not has_checksum(checksum, mackey, body + shared):
        raise PayloadError('unexpected checksum')

    # decryption
    aes = AES(enckey)
    iv_size = len(mackey) // 2    # 16bytes
    iv = body[:iv_size]
    ctext = body[iv_size:-4]
    cipher = Cipher(aes, MODE(iv), default_backend()).decryptor()
    # plain text
    return cipher.update(ctext) + cipher.finalize()


