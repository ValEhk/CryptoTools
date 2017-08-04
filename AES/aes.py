#!/usr/bin/env python3

from AES.aesutil import *
from util.blockcipher import Mode, Padding
from util.convert import *
from util.error import AESError, PaddingError

# TODO comments
# TODO check + eveythin sur aes
_nbrounds = {16: 10, 24:12, 32:14}

class AES:
    def __init__(self, key, mode, padding=Padding.PKCS7, iv=None):
        self.key = key
        self.keylen = len(key)
        try:
            self._rounds = _nbrounds[self.keylen]
        except KeyError:
            raise AESError("Invalid key length (must be 16, 24 or 32 bytes)")
        self.mode = mode
        self.iv = iv
        self.padding = padding

    def encrypt(self, plain):
        parts = []
        plain = self._pad(plain)
        for offset in range(0, len(plain), 16):
            parts.append(self._encrypt_core(plain[offset:offset+16], self.key))
        return "".join(parts)

    def _encrypt_core(self, plain, key):
        matrix = AES_Matrix(str_to_matrix(plain))
        expkey = expand_key(key)
        matrix.add_roundkey(expkey, 0)
        for i in range(1, self._rounds):
            matrix.sub_bytes()
            matrix.shift_rows()
            matrix.mix_columns()
            matrix.add_roundkey(expkey, i)
        matrix.sub_bytes()
        matrix.shift_rows()
        matrix.add_roundkey(expkey, self._rounds)
        return matrix_to_str(matrix.state).hex()

    def decrypt(self, cipher):
        parts = []
        cipher = bytes.fromhex(cipher)
        for offset in range(0, len(cipher), 16):
            parts.append(self._decrypt_core(cipher[offset:offset+16], self.key))
        return self._unpad(b"".join(parts))

    def _decrypt_core(self, cipher, key):
        matrix = AES_Matrix(str_to_matrix(cipher))
        expkey = expand_key(key)
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

    def _pad(self, text):
        padlen = 16 - len(text)%16
        if self.padding == Padding.ZERO:
            text += b"\x00"*padlen
        elif self.padding == Padding.ANSI:
            if padlen == 0:
                text += bytes(15) + b"\x10"
            else:
                text += bytes(padlen - 1) + bytes([padlen])
        elif self.padding == Padding.PKCS7:
            if padlen == 0:
                text += b"\x10"*16
            else:
                text += bytes([padlen])*padlen
        elif self.padding == Padding.NONE:
            return text
        else:
            raise AESError("Unknown padding scheme")
        return text

    def _unpad(self, text):
        if self.padding == Padding.ZERO:
            while text[-1] == 0:
                text = text[:-1]
        elif self.padding == Padding.ANSI or self.padding == Padding.PKCS7:
            check = text[-text[-1]:-1]
            for n in check:
                if n != check[0]:
                    raise PaddingError("Invalid padding")
            text = text[:-text[-1]]
        elif self.padding == Padding.NONE:
            return text
        else:
            raise AESError("Unknown padding scheme")
        return text

