#!/usr/bin/env python3

import string

_alphabet_lower = string.ascii_lowercase
_alphabet_upper = string.ascii_uppercase
_alphabet = string.ascii_letters

def rot(plain, shift=13):
    """Rotate 'plain' [string] by 'shift' (default 13)."""
    shifted = _alphabet_lower[shift:] + _alphabet_lower[:shift] + \
            _alphabet_upper[shift:] + _alphabet_upper[:shift]
    table = str.maketrans(_alphabet, shifted)
    return plain.translate(table)
