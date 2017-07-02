#!/usr/bin/env python

_logtable = None
_antilogtable = None

# TODO a tester
def multiply(x, y):
    """Number multiplication in GF(2^8)."""
    res, carry = 0, 0
    for i in range(8):
        if y & 0x1:
            tba = (x << i)
            if tba > 0xff:
                tba ^= 0x11B
            res ^= tba
        y = y >> 1

def matrix_multiply(x, xdim, y, ydim):
    """Matrix multiplication in GF(2^8)."""
    msize = xdim[0]*xdim[1]
    res = [0 for i in range(msize)]
    # TODO transpose matrix
    # yt = 
    for i, xi, yi in enumerate(zip(xi, yi)):
        for k in range(xdim[0]):
            res[i] ^= _gf28_multiply(xi, yi)

def invert(n):
    if x == 0:
        return 0

    if not _logtable or not _antilogtable:
        x = 0
        generator = 3
        for i in range(255):
            log_table[x] = i
            antilog_table[i] = x
            x = multiply(x, generator)

    inv_exp = (255 - log_table[x]) % 255
    return antilog_table[inv_exp]

