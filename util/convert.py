#!/usr/bin/env python3

import binascii

def hex_to_str(hexv):
    """Convert hex value into byte string."""
    hstr = "{:02x}".format(hexv)
    if len(hstr) % 2 == 1:
        hstr = "0"+hstr
    return binascii.unhexlify(hstr)

def hexarray_to_str(hexa):
    """Convert hex array into byte string."""
    hstr = ''.join(["{:02x}".format(h) for h in hexa])
    return binascii.unhexlify(hstr)

# -------------------------------------------------------------------------- #

def hstr_to_ascii(hstr):
    """Convert hex byte string into ascii string."""
    return binascii.unhexlify(hstr)

# -------------------------------------------------------------------------- #

def ascii_to_hstr(astr):
    """Convert ascii string into hex byte string."""
    return binascii.hexlify(astr)

# -------------------------------------------------------------------------- #

def str_to_hex(bstr):
    """Convert byte string into hex value."""
    return int(binascii.hexlify(bstr), 16)

def str_to_hexarray(bstr):
    """Convert byte string into hex array."""
    hstr = binascii.hexlify(bstr)
    return [int(hstr[i:i+2], 16) for i in range(0, len(hstr), 2)]

def str_to_matrix(bstr):
    """Convert byte string into a 4x4 column-major order matrix."""
    hexarray = str_to_hexarray(bstr)
    return [[hexarray[k] for k in range(i, 16, 4)] for i in range(4)]

# -------------------------------------------------------------------------- #

def matrix_to_str(mat):
    """Convert a 4x4 column-major order matrix into byte string."""
    barr = [mat[i%4][i//4] for i in range(16)]
    return bytes(barr)
