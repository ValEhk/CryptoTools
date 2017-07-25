#!/usr/bin/env python

from util.blockcipher import MODE
from . import gf28

# TODO comments
_sbox = None
_invsbox = None
_rcon = None
_mds = [[2,3,1,1], [1,2,3,1], [1,1,2,3], [3,1,1,2]]
_invmds = [[14,11,13,9], [9,14,11,13], [13,9,14,11], [11,13,9,14]]

# -------------------------------------------------------------------------- #

class AES_Matrix:
    def __init__(self, init):
        if not _sbox:
            _initialize_sbox()
        self.state = init
        self.cols = 4
        self.rows = 4

    # TODO complete func
    def add_roundkey(self, expanded_key, round):
        for r in range(self.rows):
            rkey = expanded_key[round:round+16:4]
            for c in range(self.cols):
                self.state[r][c] ^= rkey[c]

    def sub_bytes(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.state[r][c] = _sbox[self.state[r][c]]
    def inv_sub_bytes(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.state[r][c] = _invsbox[self.state[r][c]]

    def mix_columns(self):
        self.state = gf28.matrix_multiply(_mds, self.state)
    def inv_mix_columns(self):
        self.state = gf28.matrix_multiply(_invmds, self.state )

    def shift_rows(self):
        for r in range(1, self.rows):
            tmp = self.state[r][:r]
            self.state[r][:self.cols-r] = self.state[r][r:]
            self.state[r][self.cols-r:] = tmp
    def invshift_rows(self):
        for r in range(1, self.rows):
            tmp = self.state[r][self.cols-r:]
            self.state[r][r:] = self.state[r][:self.cols-r]
            self.state[r][:r] = tmp

# -------------------------------------------------------------------------- #

# TODO move up
def xor_lists(l1, l2):
#     TODO itertools? + move dans util
    res = []
    for i in range(len(l1)):
        res.append(l1[i] ^ l2[i])
    return res

def _initialize_sbox():
    global _sbox, _invsbox
    _sbox = [0 for i in range(256)]
    _invsbox = [0 for i in range(256)]
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

class AES:
    def __init__(self, key, mode, iv=None):
        if not _sbox or not _rcon:
            _initialize_rcon()
            _initialize_sbox()
        self.key = key
        self._rounds = 10
        self._explen = 176

    # TODO update rows/cols
    def encrypt(self, plain):
        state = AES_Matrix(plain)
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

