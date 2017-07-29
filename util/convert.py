#!/usr/bin/env python3

import binascii
import itertools

def hex_to_ascii(hexv):
    """Convert hex value into ascii string"""
    return binascii.unhexlify("{:x}".format(hexv)).decode()

def hexarray_to_ascii(hexa):
    """Convert hex array into ascii string"""
    str = ''.join(["{:02x}".format(h) for h in hexa] )
    return binascii.unhexlify(str).decode()

# -------------------------------------------------------------------------- #

def ascii_to_hex(str):
    """Convert ascii string into hex value"""
    return int(binascii.hexlify(str.encode()), 16)

def ascii_to_hexarray(str):
    """Convert ascii string into hex array"""
    hex = binascii.hexlify(str.encode())
    return [int(hex[i:i+2], 16) for i in range(0, len(hex), 2)]

def ascii_to_matrix(str):
    """Convert ascii string into  a 4x4 column-major order matrix"""
    hexarray = ascii_to_hexarray(str)
    return [[hexarray[k] for k in range(i, 16, 4)] for i in range(4)]

# -------------------------------------------------------------------------- #
# TODO move ça dans util.convert.py
def matrix_to_ascii(mat):
    return binascii.unhexlify(matrix_to_hexstring(mat)).decode("ISO-8859-1")

def hex_to_matrix(hexstr):
    hexarray = [int("0x"+hexstr[i:i+2], 16) for i in range(0, len(hexstr), 2)]
    mat = []
    for i in range(4):
        mat.append(hexarray[i::4])
    return mat


def matrix_to_hexstring(mat):
    """Convert a  matrix into an hex string"""
    res = []
    mapt = map(list, zip(*mat))
    for c in itertools.chain(*mapt):
        res.append("{:02x}".format(c))
    return ''.join(res)
