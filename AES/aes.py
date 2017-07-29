#!/usr/bin/env python3

from AES.aesutil import *
from util.blockcipher import MODE
from util.convert import *

# TODO comments
# TODO check + eveythin sur aes

class AES:
    def __init__(self, key, mode, iv=None):
        self.key = key
        self.mode = mode
        self.iv = iv
        self._rounds = 10

    def encrypt(self, plain):
        matrix = AES_Matrix(str_to_matrix(plain))
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
        return matrix_to_hexstr(matrix.state)

    def decrypt(self, cipher):
        matrix = AES_Matrix(hexstr_to_matrix(cipher))
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
        return matrix_to_str(matrix.state)

