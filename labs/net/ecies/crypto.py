
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec
from labs.utils import pad32, int_to_big, int_from_big

AES = algorithms.AES
COUNTER = modes.CTR
CURVE = ec.SECP256K1()


def sha3_256_mac(key: bytes, data: bytes) -> bytes:
    mac = hmac.HMAC(key, hashes.SHA3_256(), default_backend())
    mac.update(data)
    return mac.finalize()


def generate_random() -> ec.EllipticCurvePrivateKey:
    return ec.generate_private_key(CURVE, default_backend())


for i in range(100000):
    a = generate_random()

    v = a.private_numbers().private_value

    ib = int_to_big(v)
    t = v.to_bytes(32, byteorder='big')
    s = int_from_big(ib)
    print(v)
    print(ib)
    print(s)
    if v != s:
        raise ValueError



