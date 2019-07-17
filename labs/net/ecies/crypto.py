
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec

AES = algorithms.AES
COUNTER = modes.CTR
CURVE = ec.SECP256K1()


def sha3_256_mac(key: bytes, data: bytes) -> bytes:
    mac = hmac.HMAC(key, hashes.SHA3_256(), default_backend())
    mac.update(data)
    return mac.finalize()


def generate_random() -> ec.EllipticCurvePrivateKey:
    return ec.generate_private_key(CURVE, default_backend())


def int_to_big(value: int):
    return value.to_bytes((value.bit_length() + 7) // 8 or 1,
                          byteorder='big')


a = generate_random()


v = a.private_numbers().private_value

ib = int_to_big(v)
t = v.to_bytes(32, byteorder='big')
print(t == ib)
