#!/usr/bin/env python

from util.blockcipher import MODE
from . import gf28

# -------------------------------------------------------------------------- #

class AES_Matrix:
    def __init__(self, init):
        self.mat = init
        self.cols = 4
        self.rows = 4

    def add_roundkey(expanded_key, round):
        rkey = ""
        for r in range(self.rows):
            for c in range(self.cols):
                self.mat[r][c] ^= rkey[r][c]

    def sub_bytes():
        for r in range(self.rows):
            for c in range(self.cols):
                self.mat[r][c] = _sbox[self.mat[r][c]]
    def inv_sub_bytes():
        for r in range(self.rows):
            for c in range(self.cols):
                self.mat[r][c] = _invsbox[self.mat[r][c]]

    def mix_columns():
        self.mat = gf28.matrix_multiply(self.mat, _mds)
    def inv_mix_columns():
        self.mat = gf28.matrix_multiply(self.mat, _invmds)

    def shift_rows():
        for r in range(1, self.rows):
            tmp = self.mat[r][:r]
            self.mat[r][:self.cols-r] = self.mat[r][r:]
            self.mat[r][self.cols-r:] = tmp
    def invshift_rows():
        for r in range(1, self.rows):
            tmp = self.mat[r][self.cols-r:]
            self.mat[r][r:] = self.mat[r][:self.cols-r]
            self.mat[r][:r] = tmp

# -------------------------------------------------------------------------- #

def xor_lists(l1, l2):
#     TODO itertools? + moce dans util
    res = []
    for i in range(len(l1)):
        res.append(l1[i] ^ l2[i])
    return res

def _initialize_sbox():
    _sbox = [0 for i in range(256)]
    for i in range(256):
        n = gf28.invert(i)
        svalue = 0
        for j in range(5):
            svalue ^= n
            n = ((n << 1) | (n >> 7)) & 0xff
        _sbox[i] = svalue ^ 0x63
        _invsbox[svalue ^ 0x63] = i

# TODO
def _initialize_rcon():
    pass

_sbox = None
_invsbox = None
_rcon = None
_mds = [[2,3,1,1], [1,2,3,1], [1,1,2,3], [3,1,1,2]]
_invmds = [[14,11,13,9], [9,14,11,13], [13,9,14,11], [11,13,9,14]]

class AES:
    def __init__(self, key, mode, iv):
        if not _sbox or not _rcon:
            _initialize_rcon()
            _initialize_sbox()
        self.key = key
        self._rounds = 10
        self._explen = 176

    # TODO update rows/cols
    def encrypt(self, plain):
        state = AES_Matrix(plain)
        expkey = self._expand_key()
        state.add_roundkey(expkey, 0)
        for i in range(1, self._rounds-1):
            state.sub_bytes()
            state.shift_rows()
            state.mix_columns()
            state.add_roundkey(expkey, i)
        state.sub_bytes()
        state.shift_rows()
        state.add_roundkey(expkey, self._rounds)
        return state.mat


    # TODO update rows/cols
    def decrypt(self, cipher):
        state = AES_Matrix(cipher)
        expkey = self._expand_key()
        state.add_roundkey(expkey, self._rounds)
        state.shift_rows()
        state.sub_bytes()
        for i in range(self._rounds-1, 0, -1):
            state.add_roundkey(expkey, i)
            state.inv_mix_columns()
            state.inv_shift_rows()
            state.inv_sub_bytes()
        state.add_roundkey(expkey, 0)
        return state.mat

    # TODO update rows/cols
    def _expand_key(self):
        expykey = self.key[:]
        idx_rcon = 1
        while len(expkey) < self.explen:
            tmp = expkey[-4:]
            tmp = tmp[1:] + tmp[:1]
            for i in range(4):
                t[i] = _sbox[t[i]]
            t[0] ^= rcon[idx_rcon]
            idx_rcon += 1
            for _ in range(4):
                tmp = xor_lists(tmp, expkey[-16:-12])
                expkey.extend(tmp)
        return expkey

