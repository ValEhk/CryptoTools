#!/usr/bin/env python3

def xorvalue(instr, value):
    """Xor each element of 'input' [bytes] with 'value' [int]."""
    res = []
    for c in instr:
        res.append(c^value)
    return bytes(res)

def xorstrings(str1, str2):
    """Xor 'str1' [bytes] with 'str2' [bytes]."""
    res = []
    for i in range(min(len(str1), len(str2))):
        res.append(str1[i] ^ str2[i])
    return bytes(res)
