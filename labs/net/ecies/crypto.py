
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
    r = ec.generate_private_key(CURVE, default_backend())

    return





