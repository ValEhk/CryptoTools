#!/usr/bin/env python3

import binascii
import itertools

def hex_to_str(hexv):
    """Convert hex value into bytes string"""
    return binascii.unhexlify("{:x}".format(hexv))

def hexarray_to_str(hexa):
    """Convert hex array into bytes string"""
    str = ''.join(["{:02x}".format(h) for h in hexa] )
    return binascii.unhexlify(str)

# -------------------------------------------------------------------------- #

def str_to_hex(str):
    """Convert byte string into hex value"""
    return int(binascii.hexlify(str), 16)

def str_to_hexarray(str):
    """Convert byte string into hex array"""
    hex = binascii.hexlify(str)
    return [int(hex[i:i+2], 16) for i in range(0, len(hex), 2)]

def str_to_matrix(str):
    """Convert byte string into  a 4x4 column-major order matrix"""
    hexarray = str_to_hexarray(str)
    return [[hexarray[k] for k in range(i, 16, 4)] for i in range(4)]

# -------------------------------------------------------------------------- #
# TODO change that
def matrix_to_str(mat):
    return binascii.unhexlify(matrix_to_hexstr(mat))

def str_to_matrix(bstr):
    hexstr = bstr.hex()
    hexarray = [int(hexstr[i:i+2], 16) for i in range(0, len(hexstr), 2)]
    mat = []
    for i in range(4):
        mat.append(hexarray[i::4])
    return mat


def matrix_to_hexstr(mat):
    """Convert a  matrix into an hex string"""
    res = []
    mapt = map(list, zip(*mat))
    for c in itertools.chain(*mapt):
        res.append("{:02x}".format(c))
    return ''.join(res).encode()
