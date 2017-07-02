#!/usr/bin/env python3

from util.error import GF28Error

_logtable = None
_antilogtable = None

def _gen_tables():
    global _logtable, _antilogtable
    _logtable = [0 for i in range(256)]
    _antilogtable = [0 for i in range(255)]
    x = 1
    generator = 3
    for i in range(255):
        _logtable[x] = i
        _antilogtable[i] = x
        x = multiply(x, generator)

def add(x, y):
    return x^y

def multiply(x, y):
    """Number multiplication in GF(2^8)."""
    res, carry = 0, 0
    for i in range(8):
        if y & 0x1:
            res ^= x
        y = y >> 1
        x = x << 1
        if x & 0x100:
            x ^= 0x11B
    return res

def matrix_multiply(x, y):
    """Matrix multiplication in GF(2^8)."""
    if len(x) != len(y[0]) or len(x[0]) != len(y):
        raise GF28Error("Matrices' sizes are not matching")
    msize = xdim[0]*xdim[1]
    res = [0 for i in range(msize)]
    # TODO transpose matrix
    # yt = 
    for i, xi, yi in enumerate(zip(xi, yi)):
        for k in range(xdim[0]):
            res[i] ^= multiply(xi, yi)

def invert(n):
    if n < 0 or n > 255:
        raise GF28Error("Unsupported value")
    if n == 0:
        return 0

    if not _logtable or not _antilogtable:
        _gen_tables()
    inv_exp = (255 - _logtable[n]) % 255
    return _antilogtable[inv_exp]

