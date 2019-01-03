#!/usr/bin/env python3

import gmpy2
import math

from util.error import DLPError
from factorizer.factorizer import Factorizer

def discrete_log(g, h, n):
    """Find x such as h=g^x mod n using Pohlig-Hellman algorithm
    (cf. https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm)
    """
    phi_n = n-1
    pi, ei = get_factors(phi_n)
    lenpi = len(pi)
    gi = [0 for i in range(lenpi)]
    hi = [0 for i in range(lenpi)]
    xi = [0 for i in range(lenpi)]
    # Compute intermediate values
    for i in range(lenpi):
        exp = phi_n//pow(pi[i], ei[i])
        gi[i] = pow(g, exp, n)
        hi[i] = pow(h, exp, n)
        xi[i] = compute_x(gi[i], hi[i], pi[i], ei[i], n)
    for i, xis in enumerate(xi):
        if hi[i] != pow(gi[i], xis, n):
            raise DLPError("Incorrect intermediate values found")

    # Compute x using the chinese remainder theorem
    return chinese(xi, pi, ei, phi_n) % phi_n

# -------------------------------------------------------------------------- #

def get_factors(n):
    """Get prime factorizatio of 'n'

    Output:
    pi [List<int>] -- list of prime factors
    ei [List<int>] -- exponent of each prime factors
    """
    f = Factorizer()
    factors = f.factorize(n)
    lenfac = len(factors)
    pi, ei = [], []
    i = 0
    while i < lenfac:
        current = factors[i]
        count = 0
        while i < lenfac and current == factors[i]:
            count += 1
            i += 1
        pi.append(current)
        ei.append(count)
    return pi, ei


def chinese(xi, pi, ei, n):
    """Chinese Remainder Theorem (cf. https://en.wikipedia.org/wiki/Chinese_remainder_theorem)."""
    res = 0
    for i in range(len(pi)):
        frac = n//pow(pi[i], ei[i])
        inv = gmpy2.invert(frac, pow(pi[i], ei[i]))
        res += ((xi[i]*inv*frac) % n)
    return res

def baby_giant(g, h, n, upper):
    """Baby-Giant step algoritm (cf. https://en.wikipedia.org/wiki/Baby-step_giant-step)."""
    m = int(math.ceil(math.sqrt(upper)))
    tabl = {pow(g,j+1,n):j for j in range(m)}
    ginv = gmpy2.invert(g,n)
    y = h
    for i in range(upper):
        if y in tabl:
            return i*m + tabl[y]+1
        y = (y * pow(ginv, m, n)) % n
    raise DLPError("No solution found")

def compute_x(g, h, p, e, n):
    """Compute intermediate x such as h=g^x in the group <g> (cf. Pohlig-Hellman algorithm)."""
    mod = pow(p, e)
    ghat = pow(g, pow(p, e-1), n)
    ginv = gmpy2.invert(g, n)
    x = 0
    tmp = 1
    for i in range(e):
        exp_hhat = pow(p, e-1-i)
        hhat = pow(h*tmp, exp_hhat, n)
        xi = baby_giant(ghat, hhat, n, p)
        x += xi*pow(p,i)
        exp_tmp = pow(p, i)*xi
        tmp *= pow(ginv, exp_tmp, n)
    return x % mod
