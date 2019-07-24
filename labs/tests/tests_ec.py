
import hashlib
from labs.utils.keys import PrivateKey
from labs.utils.keys.ecdsa import (
    sign,
    recover,
    verifies
)


def tests_ec():
    keys = PrivateKey.make()
    hashes = hashlib.sha3_256('testMessages'.encode()).digest()
    sig_vrs = sign(hashes, keys.private_bytes)

    recovery = recover(hashes, sig_vrs)
    sig_rs = sig_vrs[:2]

    if verifies(hashes, sig_rs, recovery):
        print('verified')
    else:
        raise ValueError
