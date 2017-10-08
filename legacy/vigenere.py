#!/usr/bin/env python3

import string

_alphabet_lower = string.ascii_lowercase
_alphabet_upper = string.ascii_uppercase
_alphabet = string.ascii_letters

def _get_shifted_char(txtchar, keychar, right=True):
    """Shift 'txtchar' [char] by 'keychar' [char] position in the alphabet.
    Shift is performed left or right depending on 'right' [bool] (default True).
    """
    if txtchar not in _alphabet:
        return txtchar
    if txtchar in _alphabet_lower:
        charset = _alphabet_lower
        keychar = keychar.lower()
    else:
        charset = _alphabet_upper
        keychar = keychar.upper()

    if right:
        idx = charset.index(txtchar) + charset.index(keychar)
    else:
        idx = charset.index(txtchar) - charset.index(keychar)
    return charset[idx % 26]


def encrypt(plain, key):
    """Encrypt 'plain' [string] with 'key' [string]."""
    cipher = []
    for i in range(len(plain)):
        enc_char = _get_shifted_char(plain[i], key[i % len(key)])
        cipher.append(enc_char)
    return ''.join(cipher)

def decrypt(cipher, key):
    """Decrypt 'cipher' [string] with 'key' [string]."""
    plain = []
    for i in range(len(cipher)):
        dec_char = _get_shifted_char(cipher[i], key[i % len(key)], False)
        plain.append(dec_char)
    return ''.join(plain)
