def multinv(a, b):
    """Get multiplicative inverse when given m, and n from m mod n"""
    r = [a, b]
    x = [1, 0]
    y = [0, 1]
    while r[1] > 0:
        z = r[1]
        (q, r[1]) = divmod(r[0], r[1])
        r[0] = z
        z = x[0]
        x[0] = x[1]
        x[1] = z - x[0] * q
        z = y[0]
        y[0] = y[1]
        y[1] = z - y[0] * q
    return x[0]

def egcd(a, b):
    """Get solutions for x and y for ax + by = gcd(a, b)"""
    return (multinv(a, b) % b, multinv(b, a))

def gcd(a, b):
    """Get the greatest common divisor of a and b"""
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
    
def lcm(a, b):
    """Get the least common multiple of a and b"""
    return abs(a * b) // gcd(a, b)

def decrypt(e, m, k):
    """Converts ciphertext to plaintext provided that modulus is 256"""
    return (e - k) * multinv(m, 256) % 256

def lineardecipher(bstr, m, k):
    """Decrypts a linear-ciphered bytestring given m and k"""
    return bytes( [ decrypt(b, m, k) for b in bstr ] )

import unittest

"""Tests"""

class MyTest(unittest.TestCase):
    def test_gcd(self):
        self.assertEqual(gcd(5, 6), 1)
        self.assertEqual(gcd(9, 6), 3)
        self.assertEqual(gcd(10, 5), 5)

    def test_lcm(self):
        self.assertEqual(lcm(5, 6), 30)
        self.assertEqual(lcm(10, 15), 30)
        self.assertEqual(lcm(123, 422), 51906)

    def test_egcd(self):
        self.assertEqual(egcd(15, 26), (7, -4))
        self.assertEqual(egcd(110, 51), (-19, 41))
        self.assertEqual(egcd(51, 56), (11, -10))

    def test_multinv(self):
        self.assertEqual(multinv(15, 26), 7)
        self.assertEqual(multinv(110, 51), -19)
        self.assertEqual(multinv(51, 56), 11)

    def test_decrypt(self):
        self.assertEqual(decrypt(61, 5, 11), 10)
        self.assertEqual(decrypt(80, 5, 11), 65)
        self.assertEqual(decrypt(149, 5, 11), 130)

    def test_lineardecypher(self):
        self.assertEqual(lineardecipher(b"s\x04''6\xab\xaa\x18\x04EE\xf0", 5, 11), b'Hello Sierra')
        self.assertEqual(lineardecipher(b'xO\xab^6E"J\xb0', 5, 11), b'It works!')
        self.assertEqual(lineardecipher(b'\xaf\x18,\x04\xabO6\xabOTE1\xabO\x13\x18J\xab\x181', 5, 11), b'Time to turn this in')
        
unittest.main()
