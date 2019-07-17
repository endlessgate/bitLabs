
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac


def sha3_256_mac(key: bytes, data: bytes) -> bytes:
    mac = hmac.HMAC(key, hashes.SHA3_256(), default_backend())
    mac.update(data)
    return mac.finalize()


