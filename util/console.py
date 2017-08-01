#!/usr/bin/env python3

from enum import IntEnum

from .error import FormatError
from RSA.factorizer import Factorizer, Algo

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
    print("*"*(len(title) + 6))
    print(" "*3 + title + " "*3)
    print("*"*(len(title) + 6))

def print_subtitle(title):
    print("\n"+title)
    print("-"*len(title))

# -------------------------------------------------------------------------- #

def convert(value, type):
    if type == "int":
        return int(value, 0)
    elif type == "ustr":
        return value.upper()
    elif type == "falgo":
        try:
            return Algo[value.upper()]
        except KeyError:
            print("Oh dear, we are in trouble!")
            return ""
    return value.encode()

def get_parameters(params):
    for key,value in params.items():
        nval = ""
        while nval == "":
            if not value[0]:
                inputstr = "{}: ".format(key)
            else:
                inputstr = "{} [{}]: ".format(key, value[0])
            nval = input(inputstr)
            if not nval:
                nval = value[2]
            try:
                nval = convert(nval, value[1])
            except (ValueError, TypeError):
                nval = ""
                print("At least you tried...")
                continue
        params[key] = nval
