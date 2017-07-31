#!/usr/bin/env python3

from enum import IntEnum

from .error import FormatError

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

# -------------------------------------------------------------------------- #

def print_title(title):
    print(" "*3 + title + " "*3)
    print("*"*(len(title) + 6))

# -------------------------------------------------------------------------- #

def convert(value, type):
    if type == "int":
        return int(value, 0)
    elif type == "ustr":
        return value.upper()
    return value.encode()

def get_parameters(params, types, defaults=None):
    for key,value in params.items():
        nval = ""
        while not nval:
            if not value:
                inputstr = "{}: ".format(key)
            else:
                inputstr = "{} [{}]: ".format(key, value)
            nval = input(inputstr)
            if not nval:
                if defaults:
                    nval = defaults[key]
                else:
                    print("Nope, try again!")
            else:
                try:
                    nval = convert(nval, types[key])
                except ValueError:
                    nval = ""
                    print("At least you tried...")
                    continue
        params[key] = nval
