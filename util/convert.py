#!/usr/bin/env python3

import binascii
import itertools

def hex_to_str(hexv):
    """Convert hex value into byte string."""
    return binascii.unhexlify("{:02x}".format(hexv))

def hexarray_to_str(hexa):
    """Convert hex array into byte string."""
    str = ''.join(["{:02x}".format(h) for h in hexa] )
    return binascii.unhexlify(str)

# -------------------------------------------------------------------------- #

def hstr_to_ascii(hstr):
    """Convert hex byte string into ascii string."""
    return binascii.unhexlify(hstr)

# -------------------------------------------------------------------------- #

def ascii_to_hstr(str):
    """Convert ascii string into hex byte string."""
    return binascii.hexlify(str)

# -------------------------------------------------------------------------- #

def str_to_hex(str):
    """Convert byte string into hex value."""
    return int(binascii.hexlify(str), 16)


def str_to_hexarray(str):
    """Convert byte string into hex array."""
    hex = binascii.hexlify(str)
    return [int(hex[i:i+2], 16) for i in range(0, len(hex), 2)]

def str_to_matrix(str):
    """Convert byte string into a 4x4 column-major order matrix."""
    hexarray = str_to_hexarray(str)
    return [[hexarray[k] for k in range(i, 16, 4)] for i in range(4)]

# -------------------------------------------------------------------------- #

def matrix_to_str(mat):
    """Convert a 4x4 column-major order matrix into byte string."""
    barr = [mat[i%4][i//4] for i in range(16)]
    return bytes(barr)
