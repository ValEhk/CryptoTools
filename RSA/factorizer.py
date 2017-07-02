#!/usr/bin/env python

import imp
import math
import warnings
from enum import IntEnum

import gmpy2
import urllib.request as urlreq
from bs4 import BeautifulSoup

from . import fdbparser
from util.error import FactorizationError, UnitWarning


class Algo(IntEnum):
    """Enum of available algorithms."""
    FACTORDB = 0
    SMALL_PRIMES = 1
    FERMAT = 2
    MERSENNE = 3
    WOODALL = 4

# -------------------------------------------------------------------------- #

class Factorizer:
    def __init__(self, algo=Algo.FACTORDB, limit=100000):
        """Wrapper for several integer factorization algorithms.

        Keyword arguments:
        algo -- algorithm used for the factorization (default Algo.FACTORDB)
        limit -- limit in _small_primes and _fermat. This prevents the algorithm
            to run for a long time when factorizing arbitrarily large numbers (default 1000)
        """
        self.algo = algo
        self.limit = limit;
        self.factors = []
        self._fcn = [self._factordb, self._small_primes, self._fermat, \
                self._mersenne, self._woodall]

    def __repr__(self):
        return "Factorizer(%s, %s)" % (self.algo, self.limit)

    def __str__(self):
        return "** Factorizer **\n    algo: %s\n    limit: %s" % (self.algo, self.limit)


    def factorize(self, n):
        """Factorize n and return a list of its factors."""
        self.factors = []
        if n == 1:
            warnings.warn("Are you sure you want to factorize 1?", UnitWarning)
            self.factors = [1]
        elif gmpy2.is_prime(n):
            self.factors = [1, int(n)]
        else:
            self._fcn[self.algo](gmpy2.mpz(n))
            self.factors.sort()
        return self.factors


    def _factordb(self, n):
        """Factorize n by asking factordb.com."""
        self.factors = fdbparser.get_factors(n)


    def _small_primes(self, n):
        """Factorize n by trying the first primes (up to self.limit tests)."""
        if gmpy2.is_prime(n):
            self.factors.append(int(n))
            return
        p = 2
        cpt = 0
        while cpt < self.limit:
            if n % p == 0:
                self.factors.append(int(p))
                self._small_primes(n//p)
                return
            p = gmpy2.next_prime(p)
            cpt += 1
        raise FactorizationError("Factorization is incomplete")


    def _fermat(self, n):
        """Factorize n using Fermat's factorization method (up to self.limit tests).
        Warning: the method will stop as soon as a complete factorisation is found,
        even if this one is trivial.
        """
        if n == 1:
            self.factors.append(1)
            return
        if gmpy2.is_prime(n):
            self.factors.append(int(n))
            return
        cpt = 0
        a = gmpy2.isqrt(n)
        b = a*a - n
        while not gmpy2.is_square(b):
            a += 1
            b = a*a - n
            cpt += 1
            if cpt > self.limit:
                raise FactorizationError("Factorization is incomplete")
        self._fermat(a - gmpy2.isqrt(b))
        self._fermat(a + gmpy2.isqrt(b))

    def _mersenne(self, n):
        """Factorize n by trying the 20 first Mersenne primes."""
        if gmpy2.is_prime(n):
            self.factors.append(n)
            return
        exps = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89,\
                107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423]
        for e in exps:
            p = (2**e) - 1
            if n % p == 0:
                self.factors.append(p)
                self._mersenne(n//p)
                return
        raise FactorizationError("Factorization is incomplete")

    def _woodall(self, n):
        """Factorize n by trying the 20 first Woodall primes."""
        if gmpy2.is_prime(n):
            self.factors.append(n)
            return
        exps = [2, 3, 6, 30, 75, 81, 115, 123, 249, 362,\
                384, 462, 512, 751, 822, 5312, 7755, 9531, 12379, 15822]
        for e in exps:
            p = e*(2**e) - 1
            if n % p == 0:
                self.factors.append(p)
                self._woodall(n/p)
                return
        raise FactorizationError("Factorization is incomplete")
