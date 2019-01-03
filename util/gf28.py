#!/usr/bin/env python3

from util.error import GF28Error

_LOGTABLE = None
_ANTILOGTABLE = None

def _gen_tables():
    """Generate GF(2^8) _LOGTABLE and _ANTILOGTABLE with 3 as generator."""
    global _LOGTABLE, _ANTILOGTABLE
    _LOGTABLE = [0 for i in range(256)]
    _ANTILOGTABLE = [0 for i in range(255)]
    x = 1
    generator = 3
    for i in range(255):
        _LOGTABLE[x] = i
        _ANTILOGTABLE[i] = x
        x = multiply(x, generator)

def add(x, y):
    """Add x and y in GF(2^8)."""
    return x^y

def multiply(x, y):
    """Multiply x and y in GF(2^8)."""
    res = 0
    for _ in range(8):
        if y & 0x1:
            res ^= x
        y = y >> 1
        x = x << 1
        if x & 0x100:
            x ^= 0x11B
    return res


def _matrix_substep(leftop, rightop):
    """Matrix multiplication core."""
    res = 0
    for i, _ in enumerate(leftop):
        res ^= multiply(leftop[i], rightop[i])
    return res

def matrix_multiply(x, y):
    """Multiply matrices x and y in GF(2^8)."""
    if len(x) != len(y[0]) or len(x[0]) != len(y):
        raise GF28Error("Matrices' sizes not matching")
    msize = len(x)
    res = [[0 for j in range(msize)] for i in range(msize)]
    yt = [list(c) for c in zip(*y)]
    for i in range(msize):
        for j in range(msize):
            res[i][j] = _matrix_substep(x[i], yt[j])
    return res

def invert(n):
    """Return the inverse of n in GF(2^8)."""
    if n < 0 or n > 255:
        raise GF28Error("Unsupported value")
    if n == 0:
        return 0

    if not _LOGTABLE or not _ANTILOGTABLE:
        _gen_tables()
    inv_exp = (255 - _LOGTABLE[n]) % 255
    return _ANTILOGTABLE[inv_exp]
