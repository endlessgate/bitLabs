
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import PublicFormat, Encoding

from labs.utils.keys.ecdsa import sign
from labs.utils import (
    read_only,
    int_to_big,
    int_from_big,
    pad32
)


class PrivateKey:

    def __init__(self, private_bytes, public_bytes):
        self._private_bytes = private_bytes
        self._private_numbers = int_from_big(self.private_bytes)
        self.public_bytes = public_bytes
        self.public_numbers = int_from_big(self.public_bytes)

    private_bytes = read_only('_private_bytes')
    private_numbers = read_only('_private_numbers')

    def sign(self, hashes: bytes):
        return sign(hashes, self.private_bytes)

    @classmethod
    def make(cls):
        private = ec.generate_private_key(ec.SECP256K1(), default_backend())
        public_bytes = private.public_key().public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)
        private_num = private.private_numbers().private_value
        private_bytes = pad32(int_to_big(private_num))
        return cls(private_bytes, public_bytes[1:])

