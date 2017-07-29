#!/usr/bin/env python3

from enum import IntEnum

from .error import FormatError

class FORMAT(IntEnum):
    HEX = 0
    DEC = 1
    STR = 2

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
