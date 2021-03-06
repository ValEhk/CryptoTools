#!/usr/bin/env python3

import gmpy2

from util.error import RSAError, WienerError, HastadError, CommonModError
from util.convert import hex_to_str, str_to_hex

class RSA:
    """RSA encryption (cf. https://en.wikipedia.org/wiki/RSA_(cryptosystem)).

    Keyword arguments:
    p [int] -- first prime used to generate RSA keys
    q [int] -- second prime used to generate RSA keys
    e [int] -- public exponent (default 65537)
    """
    def __init__(self, p, q, e=65537):
        self.p = gmpy2.mpz(p)
        if not gmpy2.is_prime(self.p):
            raise RSAError("'p' is not prime")
        self.q = gmpy2.mpz(q)
        if not gmpy2.is_prime(self.q):
            raise RSAError("'q' is not prime")
        self.e = e
        self.privkey = None
        self.pubkey = None

    def __repr__(self):
        return "RSA({:d}, {:d}, {:d})".format(self.p, self.q, self.e)

    def __str__(self):
        return "RSA\n  p: {:d}\n  q: {:d}\n  e: {:d}".format(self.p, self.q, self.e)


    def gen_keys(self):
        """Generate private and public keys."""
        if not (self.pubkey and self.privkey):
            phi = gmpy2.lcm(self.p-1, self.q-1)
            if gmpy2.gcd(phi, self.e) != 1:
                raise RSAError("Unable to generate keys: phi and e are not coprimes")
            d = int(gmpy2.invert(self.e, phi))
        n = self.p * self.q
        self.pubkey = PubKey(n, self.e)
        self.privkey = PrivKey(n, d)
        return self.pubkey, self.privkey

# -------------------------------------------------------------------------- #

class PubKey():
    """RSA public key

    Keyword arguments:
    n [int] -- modulus
    e [int] -- public exponent
    """
    def __init__(self, n, e):
        self.n = n
        self.e = e

    def __repr__(self):
        return "PubKey({:d}, {:d})".format(self.n, self.e)

    def encrypt(self, plainstr):
        """Encrypt 'plainstr' [bytes] and return the corresponding ciphertext [int]."""
        plain = str_to_hex(plainstr)
        cipher = pow(plain, self.e, self.n)
        return cipher

# -------------------------------------------------------------------------- #

class PrivKey():
    """RSA private key

    Keyword arguments:
    n [int] -- modulus
    d [int] -- private exponent
    """
    def __init__(self, n, d):
        self.n = n
        self.d = d

    def __repr__(self):
        return "PrivKey({:d}, {:d})".format(self.n, self.d)

    def decrypt(self, cipher):
        """Decrypt 'cipher' [int] and return the corresponding plaintext [bytes]."""
        plain = pow(cipher, self.d, self.n)
        return hex_to_str(plain)

# -------------------------------------------------------------------------- #

def wiener(pk):
    """Wiener's attack (d small)

    Keyword arguments:
    pk [PubKey] -- public key
    Output:
    p [int] -- first prime factor of n
    q [int] -- second prime factor of n
    d [int] -- private exponent
    """
    cf = _continued_frac(pk.e, pk.n)
    for c in _cvgs(cf):
        k, d = c.numerator, c.denominator
        if k == 0 or (pk.e*d - 1)%k != 0:
            continue
        phi = (pk.e*d - 1) // k
        b = pk.n - phi + 1
        delta = b*b - 4*pk.n
        if delta >= 0:
            root = gmpy2.isqrt(delta)
            if root*root == delta and not (b+root) & 1:
                p, q = (b+root)//2, (b-root)//2
                return p, q, d
    raise WienerError("Unable to crack RSA with Wiener's attack")

def _continued_frac(num, den):
    """Compute continued fraction of num/den."""
    res = []
    while den:
        q = num // den
        res.append(q)
        num, den = den, num - den*q
    return res

def _convergent(coeffs):
    """Compute the convergent of 'coeffs'."""
    f = gmpy2.mpq(0, 1)
    for x in reversed(coeffs):
        try:
            f = 1 / (f + x)
        except ZeroDivisionError:
            return f
    return 1/f

def _cvgs(coeffs):
    """Compute all intermediate convergents of 'coeffs'."""
    i = 0
    while i < len(coeffs):
        yield _convergent(coeffs[:i+1])
        i += 1

# -------------------------------------------------------------------------- #

def hastad(pks, cs):
    """Hastad's attack (same 'm' sent 'e' times)

    Keyword arguments:
    pks [List<PubKey>] -- list of public keys
    cs [List<int>] -- list of ciphertexts
    Output:
    m [bytes] -- plaintext
    """
    _check(pks, cs)
    prod = 1
    me = 0
    for pk in pks:
        prod *= pk.n
    for pk, c in zip(pks, cs):
        p = prod//pk.n
        me += c * gmpy2.invert(p, pk.n) * p
    return hex_to_str(gmpy2.iroot(me % prod, pks[0].e)[0])

def _check(pks, cs):
    """Check if Hastad's attack is possible with the given values."""
    if len(pks) != len(cs):
        raise HastadError("Number of ciphertexts not equal to number of public keys")
    if len(pks) < pks[0].e:
        raise HastadError("Less than 'e' public keys")
    for i in range(1, len(pks)):
        if pks[i-1].e != pks[i].e:
            raise HastadError("Different value for 'e'")
    return 0

# -------------------------------------------------------------------------- #

def common_modulus(pk1, pk2, c1, c2):
    """Common modulus attack (same 'm', same'n')

    Keyword arguments:
    pk1, pk2 [PubKey] -- public keys
    c1, c2 [int] -- ciphertexts
    Output:
    m [bytes] -- plaintext
    """
    if pk1.n != pk2.n:
        raise CommonModError("Different modulus 'n1' and 'n2'")
    if gmpy2.gcd(pk1.e, pk2.e) != 1:
        raise RSAError("gcd(e1, e2) not equal to 1")
    u = gmpy2.invert(pk1.e, pk2.e)
    v = (1 - u*pk1.e)//pk2.e
    inv_c2 = gmpy2.invert(c2, pk2.n)
    m1 = pow(c1, u, pk1.n)
    m2 = pow(inv_c2, -v, pk2.n)
    return hex_to_str(m1*m2 % pk1.n)
