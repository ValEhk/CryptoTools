#!/usr/bin/env python3

import string

_alphabet_lower = string.ascii_lowercase
_alphabet_upper = string.ascii_uppercase
_alphabet = string.ascii_letters

def rot(input, shift=13):
    """Rotate 'input' [string] by 'shift' [int] (default 13)."""
    shifted = _alphabet_lower[shift:] + _alphabet_lower[:shift] + \
            _alphabet_upper[shift:] + _alphabet_upper[:shift]
    table = str.maketrans(_alphabet, shifted)
    return input.translate(table)

def xor(input, value):
    """Xor each element of 'input' [bytes] with 'value' [int]."""
    res = []
    for c in input:
        res.append(c^value)
    return bytes(res)

