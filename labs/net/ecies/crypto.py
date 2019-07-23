
import math
import struct

from labs.utils.keys import PrivateKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import ec
from labs.exceptions import InvalidKeys

from labs.utils import (
    int_from_big,
    is_bytes
)


CURVE = ec.SECP256K1()


def make_specific_keys(key):
    piece = len(key) // 2
    return key[:piece], key[piece:]


def sha3_256_mac(key: bytes, data: bytes) -> bytes:
    mac = hmac.HMAC(key, hashes.SHA3_256(), default_backend())
    mac.update(data)
    return mac.finalize()


def generate_random() -> PrivateKey:
    return PrivateKey.make()


def make_shared_secret(privkey, pubkey) -> bytes:
    # priv_numbers = privkey.private_numbers().private_value
    priv_numbers = int_from_big(privkey)    # Todo: keys management class
    ec_privkey = ec.derive_private_key(priv_numbers, CURVE, default_backend())
    try:
        exchange_nums = ec.EllipticCurvePublicKey.from_encoded_point(CURVE, pubkey)
        exchange_pubkey = exchange_nums.public_numbers().public_key(default_backend())
    except ValueError as err:
        raise InvalidKeys(name='ExchangePubKeys', errors=err)

    return ec_privkey.exchange(ec.ECDH(), exchange_pubkey)


def kdf(material: bytes) -> bytes:
    # NIST.SP.800-56A
    # key derivation function
    if not is_bytes(material):
        raise InvalidKeys(name="KDF",
                          errors="key expected bytes, got {}".format(type(material).__name__))

    hash_length = 32 * 8
    material_length = int_from_big(material).bit_length()
    if material_length > hash_length * (2 ** 32 - 1):
        raise InvalidKeys(name="KDF",
                          errors="secret material-key error, length={}".format(material_length))

    reps = math.ceil(material_length / hash_length)
    counter = []
    for i in range(reps):
        counter.append(
            struct.pack(">I", i + 1)
        )  # 32bit

    ctx = hashes.SHA3_256()
    for salt in counter:
        ctx.update(salt)

    ctx.update(material)
    key = ctx.finalize()
    if len(key) != 32:
        raise InvalidKeys(name="KDF",
                          errors="derived key error, length={} ".format(len(key)))
    return key


