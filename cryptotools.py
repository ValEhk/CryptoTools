#!/usr/bin/env python

import warnings
import sys
import gmpy2

from argparse import ArgumentParser, ArgumentError

from util.inparser import *
from RSA.rsa import *
from RSA.factorizer import Factorizer, Algo

def handle_rsa(parser, args):
    dic = parse_file(args.files[0])

    # common modulus
    if args.common:
        if len(args.files) != 2:
            parser.error("2 files expected with '--common'")
        dic2 = inparser.parse_file(args.files[1])
        pub1 = PubKey(dic['n'], dic['e'])
        pub2 = PubKey(dic2['n'], dic2['e'])
        plain = common_modulus(pub1, pub2, dic['c'], dic2['c'])
        return hex_to_ascii(plain)

    # e-root of c
    if args.eroot:
        plain = gmpy2.iroot(gmpy2.mpz(dic['c']), dic['e'])
        return hex_to_ascii(plain)

    # Hastad's attack
    elif args.hastad:
        pks = [PubKey(dic['n'], dic['e'])]
        cs = [dic['c']]
        for f in args.files[1:]:
            d = parse_file(f)
            pks.append(d['n'], d['e'])
            cs.append(d['c'])
        plain = hastad(pks, cs)
        return hex_to_ascii(plain)

    # Wiener's attack
    if args.wiener:
        pubk = PubKey(dic['n'], dic['e'])
        p, q, d = wiener(pubk)
        out = [p, q, d]
        if "c" in dic:
            privk = PrivKey(dic[n], dic[d])
            plain = priv.decrypt(dic["c"])
            out = hex_to_ascii(plain)
        return out

    # Factorize n
    if args.factorize:
        f = Factorizer(Algo[args.algo])
        pq = f.factorize(dic['n'])
        r = RSA(pq[0], pq[1], dic["e"])
        pub, priv = r.gen_keys()
        plain = priv.decrypt(dic["c"])
        return hex_to_ascii(plain)

    # Decrypt
    if args.decrypt:
        # Decrypt with private key (n, d)
        if "n" in dic:
            priv = PrivKey(dic["n"], dic["d"])
        # Decrypt with primes p and q
        else:
            r = RSA(dic["p"], dic["q"], dic["e"])
            pub, priv = r.gen_keys()
        plain = priv.decrypt(dic["c"])
        return hex_to_ascii(plain)

    # Encrypt (default)
    plain = ascii_to_hex(dic["m"])
    # Encrypt with public key (n, e)
    if "n" in dic:
        pub = PubKey(dic["n"], dic["e"])
    # Encrypt with primes p and q
    else:
        r = RSA(dic["p"], dic["q"], dic["e"])
        pub, priv = r.gen_keys()
    return pub.encrypt(dic[c])

# -------------------------------------------------------------------------- #

def handle_aes(parser, args):
    dic = parse_file(args.files[0])

# -------------------------------------------------------------------------- #

if __name__ == "__main__":

    descr = ("Crypto-CTF is a small python tool providing a quick and easy ",
        "way to complete the basic cryptography challenges commonly found during CTFs.")
    parser = ArgumentParser(description=''.join(descr))
    parser.add_argument('--version', action='version', version="%(prog)s 1.0")
    subparser = parser.add_subparsers()

    # RSA
    rsaparser = subparser.add_parser("rsa", help="RSA")
    exgr = rsaparser.add_mutually_exclusive_group()
    algo_choices = ', '.join([e.name for e in Algo])
    algo_default = algo_choices.split(",")[0]
    rsaparser.add_argument("--algo", default="FACTORDB",
            help="factorization method used with '--factorize'. \
                    Possible values are {} (Default {})" .format(algo_choices, algo_default))
    exgr.add_argument("--common",action="store_true",
            help="common modulus attack (same n, same m)")
    exgr.add_argument("--decrypt",action="store_true",
            help="decrypt c with private key (n, d)")
    exgr.add_argument("--eroot",action="store_true",
            help="compute the eth-root of c (big n, small e)")
    exgr.add_argument("--factorize",action="store_true",
            help="factorize n to decrypt c")
    exgr.add_argument("--hastad", action="store_true",
            help="Hastad's attack (same m sent e times)")
    exgr.add_argument("--wiener",action="store_true",
            help="Wieners attack (d small)")
    rsaparser.add_argument("files", metavar="FILE", nargs="+", help="input file (refer to README.md for more details)")

    # AES
    aesparser = subparser.add_parser("aes", help="AES")
    aesparser.add_argument("files", metavar="FILE", nargs="+", help="input file (refer to README.md for more details)")


# TODO choose right handle
# TODO encrypt is default
    args = parser.parse_args()
    out = handle_rsa(rsaparser, args)
    print(out)
