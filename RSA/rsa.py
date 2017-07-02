#!/usr/bin/env python

import sys

import gmpy2

from util.error import RSAError, WienerError

class RSA:
    def __init__(self, p, q, e=65537):
        """RSA encryption (cf. https://en.wikipedia.org/wiki/RSA_(cryptosystem)).

        Keyword arguments:
        p -- first prime used to generate RSA keys
        q -- second prime used to generate RSA keys
        e -- public exponent (default 65537)
        """
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
        return "RSA(%d, %d, %e)" % (self.p, self.q, self.e)

    def __str__(self):
        return "-- RSA --\n    p: %d\n    q: %d\n    e: %d" % (self.p, self.q, self.d)


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

    def _mod_inv(self, a, m):
        """Compute modular inverse of a mod m using extended Euclidean algorithm."""
        x0, x1, y0, y1 = 1, 0, 0, 1
        mtmp = m
        while mtmp != 0:
            q, a, mtmp =  a // mtmp, mtmp, a % mtmp
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        return  (x0 + m) % m

# -------------------------------------------------------------------------- #

class PubKey():
    def __init__(self, n, e):
        """RSA public key."""
        self.n = n
        self.e = e

    def __repr__(self):
        return "PubKey(%d, %d)" % (self.n, self.e)

    def encrypt(self, plain):
        """Encrypt plain with self."""
        cipher = pow(plain, self.e, self.n)
        return cipher

# -------------------------------------------------------------------------- #

class PrivKey():
    def __init__(self, n, d):
        """RSA private key."""
        self.n = n
        self.d = d

    def __repr__(self):
        return "PrivKey(%d, %d)" % (self.n, self.d)

    def decrypt(self, cipher):
        """Decrypt cipher with self."""
        plain = pow(cipher, self.d, self.n)
        return plain

# -------------------------------------------------------------------------- #

def wiener(pk):
    """Wiener's attack (d small)

    Keyword arguments:
    pk -- public key
    Output:
    p -- first factor of n (prime)
    q -- second factor of n (prime)
    d -- private exponent
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
    """Compute all intermediate convergents."""
    i = 0
    while i < len(coeffs):
        yield _convergent(coeffs[:i+1])
        i += 1

# -------------------------------------------------------------------------- #

def hastad(pks, cs):
    """Hastad's attack (same 'm' sent 'e' times)

    Keyword arguments:
    pks -- list of public keys
    cs -- list of ciphertexts (int)
    Output:
    m -- plaintext (int)
    """
    _check(pks, cs)
    prod = 1
    me = 0
    for pk in pks:
        prod *= pk.n
    for pk,c in zip(pks, cs):
        p = prod//pk.n
        me += c * gmpy2.invert(p, pk.n) * p
    return gmpy2.iroot(me % prod, pks[0].e)[0]

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
    pk1, pk2 -- public keys
    c1, c2 -- ciphertexts (int)
    Output:
    m -- plaintext (int)
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
    return m1*m2 % pk1.n
