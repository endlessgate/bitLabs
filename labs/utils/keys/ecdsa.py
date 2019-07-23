
import hashlib
import hmac

from labs.utils.keys.const import SECP256K1
from labs.utils import (
    int_to_big,
    int_from_big
)


CURVE = SECP256K1()


def inv(p: int, q: int):
    if p == 0:
        return 0

    l, h = 1, 0
    low, high = p % q, q
    while low > 1:
        r = high // low
        _n, n = h - l * r, high - low * r
        l, low, h, high = _n, n, l, low
    return l % q


def from_jacob(p):
    k = inv(p[2], CURVE.P)
    return (p[0] * k**2) % CURVE.P, (p[1] * k**3) % CURVE.P


def to_jacob(p):
    return p[0], p[1], 1


def jacob_double(p):
    if not p[1]:
        return 0, 0, 0

    _y = (p[1]**2) % CURVE.P
    _s = (4 * p[0] * _y) % CURVE.P
    _m = (3 * p[0]**2 + CURVE.A * p[2]**4) % CURVE.P

    x = (_m**2 - 2 * _s) % CURVE.P
    y = (_m * (_s - x) - 8 * _y ** 2) % CURVE.P
    z = (2 * p[1] * p[2]) % CURVE.P
    return x, y, z


def jacob_add(p, q):
    if not p[1]:
        return q
    if not q[1]:
        return p

    x1 = (p[0] * q[2] ** 2) % CURVE.P
    x2 = (q[0] * p[2] ** 2) % CURVE.P
    y1 = (p[1] * q[2] ** 3) % CURVE.P
    y2 = (q[1] * p[2] ** 3) % CURVE.P
    if x1 == x2:
        if y1 != y2:
            return 0, 0, 1
        return jacob_double(p)

    _x = x2 - x1
    _y = y2 - y1
    _u = (_x * _x) % CURVE.P
    _v = (_x * _u) % CURVE.P
    _uv = (x1 * _u) % CURVE.P

    x = (_y**2 - _v - 2 * _uv) % CURVE.P
    y = (_y * (_uv - x) - y1 * _v) % CURVE.P
    z = (_x * p[2] * q[2]) % CURVE.P
    return x, y, z


def jacob_mul(p, q):
    if p[1] == 0 or q == 0:
        return 0, 0, 1
    if q == 1:
        return p
    if q < 0 or q >= CURVE.N:
        return jacob_mul(p, q // 2)
    if (q % 2) == 0:
        return jacob_double(jacob_mul(p, q // 2))
    if (q % 2) == 1:
        return jacob_add(jacob_double(jacob_mul(p, q // 2)), p)


def mul(p, q):
    return from_jacob(jacob_mul(to_jacob(p), q))


def generate_k(hashes, privkey, hash_func=hashlib.sha3_256):
    # RFC 6979: https://tools.ietf.org/html/rfc6979

    v = b'\x01' * 32
    k = b'\x00' * 32

    k = hmac.new(k, v + b'\x00' + privkey + hashes, hash_func).digest()
    v = hmac.new(k, v, hash_func).digest()
    k = hmac.new(k, v + b'\x01' + privkey + hashes, hash_func).digest()
    v = hmac.new(k, v, hash_func).digest()

    v = hmac.new(k, v, hash_func).digest()
    k = int_to_big(v)
    return k


def sign(hashes, privkey):
    hashes_numbers = int_from_big(hashes)
    privkey_numbers = int_to_big(privkey)

    k = generate_k(hashes, privkey)
    r, y = mul(CURVE.G, k)
    s = inv(k, CURVE.N) * (hashes_numbers + r * privkey_numbers) % CURVE.N

    v = 27 + ((y % 2) ^ (0 if s * 2 < CURVE.N else 1))
    s = s if s * 2 < CURVE.N else CURVE.N - s
    return [r, s, v - 27]

