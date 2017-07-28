#!/usr/bin/env python3

import itertools
import binascii

from AES.aesutil import *
from util.blockcipher import MODE
from util.inparser import ascii_to_hexarray

# TODO comments

# -------------------------------------------------------------------------- #
# TODO check + eveythin sur aes

# TODO move ça dans util.convert.py
def matrix_to_ascii(mat):
    return binascii.unhexlify(matrix_to_hex(mat)).decode("ISO-8859-1")

def hex_to_matrix(hexstr):
    hexarray = [int("0x"+hexstr[i:i+2], 16) for i in range(0, len(hexstr), 2)]
    mat = []
    for i in range(4):
        mat.append(hexarray[i::4])
    return mat

def ascii_to_matrix(str):
    """Convert ascii string into  a 4x4 matrix"""
    hexarray = ascii_to_hexarray(str)
    return [[hexarray[k] for k in range(i, 16, 4)] for i in range(4)]

def matrix_to_hex(mat):
    """Convert a  matrix into an hex string"""
    res = []
    mapt = map(list, zip(*mat))
    for c in itertools.chain(*mapt):
        res.append("{:02x}".format(c))
    return ''.join(res)

class AES:
    def __init__(self, key, mode, iv=None):
        self.key = key
        self._rounds = 10

    def encrypt(self, plain):
        matrix = AES_Matrix(ascii_to_matrix(plain))
        expkey = expand_key(self.key)
        matrix.add_roundkey(expkey, 0)
        for i in range(1, self._rounds):
            matrix.sub_bytes()
            matrix.shift_rows()
            matrix.mix_columns()
            matrix.add_roundkey(expkey, i)
        matrix.sub_bytes()
        matrix.shift_rows()
        matrix.add_roundkey(expkey, self._rounds)
        return matrix_to_hex(matrix.state)

    def decrypt(self, cipher):
        matrix = AES_Matrix(hex_to_matrix(cipher))
        expkey = expand_key(self.key)
        matrix.add_roundkey(expkey, self._rounds)
        matrix.inv_shift_rows()
        matrix.inv_sub_bytes()
        for i in range(self._rounds-1, 0, -1):
            matrix.add_roundkey(expkey, i)
            matrix.inv_mix_columns()
            matrix.inv_shift_rows()
            matrix.inv_sub_bytes()
        matrix.add_roundkey(expkey, 0)
        return matrix_to_ascii(matrix.state)

