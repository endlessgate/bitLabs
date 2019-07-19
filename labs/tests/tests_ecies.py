
from labs.net.ecies.crypto import generate_random, make_shared_secret, kdf


def tests_kdf():
    my_test_pub = b'\x04#\xbf\x1a\x84\xb73\xab`\xa3\x91\xed\xee\x82+n\xb9\xd5\xc9A\xa1\x9c\xfd\xe8r\x1cwy\xdc\xefG\xe0\xea\xbc\xa2\xc0D}\x06b)X\xe7\\\xda\xaa\xc36\xd0\x16\xef\x83\xa3\x02\x17\xf6\x93\xc0F\x81\x0f;\xc9NV'
    my_test_pub2 = b'\x04+\xd0n\x0eR\x81\xb5e\x7f\x8c\xcc\xff\xde\xb6\x0b\x14W\xcd\x01}\\\x9b\xd2G\x8cs\xd1\xf2\x0c]\x1e\xdd\xe8\xea\xbc!\xd5\xd4\xd2<\x1f\x87\x89\x91!=\xd7TB\x00SG\xac%\xcb \xf0p\xf0\x13}\x1dm\xcd'
    # -- generate random number R --
    r = generate_random()
    r2 = generate_random()

    # -- shared secret S --
    material = make_shared_secret(r, my_test_pub2)
    material2 = make_shared_secret(r2, my_test_pub)

    key = kdf(material)
    key2 = kdf(material2)
    print(key, len(key))
    print(key2, len(key2))


tests_kdf()


