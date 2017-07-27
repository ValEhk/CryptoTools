#!/usr/bin/env python
import itertools
import binascii

from util.blockcipher import MODE
from util.inparser import ascii_to_hexarray
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

    def _get_subkey(self, expanded_key, round):
        offset = 16*round
        subkey = [expanded_key[offset+i:offset+16:4] for i in range(self.rows)]
        return subkey

    # TODO complete func
    def add_roundkey(self, expanded_key, round):
        rkey = self._get_subkey(expanded_key, round)
        for r in range(self.rows):
            for c in range(self.cols):
                self.state[r][c] ^= rkey[r][c]

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
    def inv_shift_rows(self):
        for r in range(1, self.rows):
            tmp = self.state[r][self.cols-r:]
            self.state[r][r:] = self.state[r][:self.cols-r]
            self.state[r][:r] = tmp

# -------------------------------------------------------------------------- #
# TODO check + eveythin sur aes

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

# TODO mettre ca + sbox a part
def _initialize_rcon():
    global _rcon
    _rcon = [0 for i in range(255)]
    value = 0x8d
    for i in range(0, 255):
        _rcon[i] = value
        value = gf28.multiply(value, 2)

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
        matrix = AES_Matrix(ascii_to_matrix(plain))
        expkey = self._expand_key()
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


    # TODO update rows/cols
    def decrypt(self, cipher):
        matrix = AES_Matrix(hex_to_matrix(cipher))
        expkey = self._expand_key()
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

    # TODO update rows/cols
    def _expand_key(self):
        expkey = ascii_to_hexarray(self.key)
        idx_rcon = 1
        while len(expkey) < self._explen:
            tmp = expkey[-4:]
            tmp = tmp[1:] + tmp[:1]
            for i in range(4):
                tmp[i] = _sbox[tmp[i]]
            tmp[0] ^= _rcon[idx_rcon]
            idx_rcon += 1
            for _ in range(4):
                tmp = xor_lists(tmp, expkey[-16:-12])
                expkey.extend(tmp)
        return expkey

