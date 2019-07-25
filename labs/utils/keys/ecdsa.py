
import hashlib
import hmac

from labs.utils.keys.const import SECP256K1
from labs.utils import (
    int_to_big,
    int_from_big,
    pad32
)


CURVE = SECP256K1()


def ec_inv(p: int, q: int):
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
    k = ec_inv(p[2], CURVE.P)
    return (p[0] * k**2) % CURVE.P, (p[1] * k**3) % CURVE.P


def to_jacob(p):
    return p[0], p[1], 1


def ec_double(p):
    if not p[1]:
        return 0, 0, 0

    _y = (p[1]**2) % CURVE.P
    _s = (4 * p[0] * _y) % CURVE.P
    _m = (3 * p[0]**2 + CURVE.A * p[2]**4) % CURVE.P

    x = (_m**2 - 2 * _s) % CURVE.P
    y = (_m * (_s - x) - 8 * _y ** 2) % CURVE.P
    z = (2 * p[1] * p[2]) % CURVE.P
    return x, y, z


def ec_add(p, q):
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
        return ec_double(p)

    _x = x2 - x1
    _y = y2 - y1
    _u = (_x * _x) % CURVE.P
    _v = (_x * _u) % CURVE.P
    _uv = (x1 * _u) % CURVE.P

    x = (_y**2 - _v - 2 * _uv) % CURVE.P
    y = (_y * (_uv - x) - y1 * _v) % CURVE.P
    z = (_x * p[2] * q[2]) % CURVE.P
    return x, y, z


def ec_mul(p, q):
    if p[1] == 0 or q == 0:
        return 0, 0, 1
    if q == 1:
        return p
    if q < 0 or q >= CURVE.N:
        return ec_mul(p, q // 2)
    if (q % 2) == 0:
        return ec_double(ec_mul(p, q // 2))
    elif (q % 2) == 1:
        return ec_add(ec_double(ec_mul(p, q // 2)), p)


def mul(p, q):
    return from_jacob(ec_mul(to_jacob(p), q))


def generate_k(hashes, privkey, hash_func=hashlib.sha3_256):
    # RFC6979::section#3.2: https://tools.ietf.org/html/rfc6979

    v = b'\x01' * 32
    k = b'\x00' * 32

    k = hmac.new(k, v + b'\x00' + privkey + hashes, hash_func).digest()
    v = hmac.new(k, v, hash_func).digest()
    k = hmac.new(k, v + b'\x01' + privkey + hashes, hash_func).digest()
    v = hmac.new(k, v, hash_func).digest()

    v = hmac.new(k, v, hash_func).digest()
    k = int_from_big(v)
    return k


def sign(hashes: bytes, privkey: bytes):
    # X9.62
    hashes_numbers = int_from_big(hashes)
    privkey_numbers = int_from_big(privkey)

    k = generate_k(hashes, privkey)
    r, y = mul(CURVE.G, k)
    s = ec_inv(k, CURVE.N) * (hashes_numbers + r * privkey_numbers) % CURVE.N

    v = 33 + ((y % 2) ^ (0 if s * 2 < CURVE.N else 1))
    s = s if s * 2 < CURVE.N else CURVE.N - s
    return [r, s, v - 33]


def recover(hashes: bytes, sig_vrs):
    r, s, v = sig_vrs
    v = v + 33
    # todo range exception
    x = r
    a = (x * x * x + CURVE.A * x + CURVE.B) % CURVE.P
    b = pow(a, (CURVE.P + 1) // 4, CURVE.P)

    y = b if (b - (v % 2)) % 2 == 0 else CURVE.P - b
    e = int_from_big(hashes)

    mg = ec_mul((CURVE.Gx, CURVE.Gy, 1), (CURVE.N - e) % CURVE.N)
    xy = ec_mul((x, y, 1), s)
    _xy = ec_add(mg, xy)
    Q = ec_mul(_xy, ec_inv(r, CURVE.N))

    p, q = from_jacob(Q)
    return b''.join((pad32(int_to_big(p)), pad32(int_to_big(q))))


def verifies(hashes: bytes, sig_rs, pubkey):
    r, s = sig_rs
    public_p = tuple(int_from_big(p) for p in pubkey)

    w = ec_inv(s, CURVE.N)
    e = int_from_big(hashes)

    p, q = e * w % CURVE.N, r * w % CURVE.N
    a = mul(CURVE.G, p)
    b = mul(public_p, q)
    v = ec_add(to_jacob(a), to_jacob(b))
    x, _ = from_jacob(v)
    is_verified_r = r == x == r % CURVE.N
    is_verified_s = s == s % CURVE.N
    if is_verified_r and is_verified_s:
        return True
    else:
        return False


def encode_signature(sig_vrs):
    r, s, v = sig_vrs
    r_bytes = pad32(int_to_big(r))
    s_bytes = pad32(int_to_big(s))
    v_bytes = int_to_big(v)
    return b''.join((r_bytes, s_bytes, v_bytes))


def decode_signature(sig_vrs):
    sig = sig_vrs[:32], sig_vrs[32:64], sig_vrs[-1:]
    decode_sig = [
        int_from_big(point)
        for point
        in sig
    ]
    return decode_sig

