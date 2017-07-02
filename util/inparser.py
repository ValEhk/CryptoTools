#!/usr/bin/env python3

import binascii
from enum import IntEnum

from .error import FormatError

class FORMAT(IntEnum):
    HEX = 0
    DEC = 1
    STR = 2

# -------------------------------------------------------------------------- #

def hex_to_ascii(hex):
    """Convert hex value into ascii string"""
    return binascii.unhexlify("{:x}".format(hex)).decode()

def hexarray_to_ascii(hex):
    """Convert hex array into ascii string"""
    str = ''.join(["{:02x}".format(h) for h in hex] )
    return binascii.unhexlify(str).decode()

def ascii_to_hex(str):
    """Convert ascii string into hex value"""
    return int(binascii.hexlify(str.encode()), 16)

def ascii_to_hexarray(str):
    """Convert ascii string into hex array"""
    hex = binascii.hexlify(str.encode())
    return [int(hex[i:i+2], 16) for i in range(0, len(hex), 2)]

# -------------------------------------------------------------------------- #

def parse_file(filename):
    dic = {}
    with open(filename, "r") as f:
        for l in f.readlines():
            spl = l.split("=")
            key = spl[0].strip()
            try:
                value = int(spl[-1].strip(), 0)
            except ValueError:
                raise FormatError("Incorrect value for %s" % key)
            if key in dic:
                raise FormatError("Multiple definition of %s" % key)
            dic[key] = value
    return dic
