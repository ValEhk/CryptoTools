#!/usr/bin/env python3

import warnings
import sys
import gmpy2

from argparse import ArgumentParser, ArgumentError

from util.console import *
from RSA.rsa import *
from RSA.factorizer import Factorizer, Algo


algo_def = Algo.FACTORDB.name
algo_list = ' / '.join([e.name.lower() for e in Algo]).replace(
        algo_def.lower(), algo_def)

def handle_rsa(parser, args):
    # params = parse_file(args.files[0])
    # common modulus
    if args.common:
        # TODO
        print_title("RSA - Common Modulus")
        params = {}
        if len(args.files) != 2:
            parser.error("2 files expected with '--common'")
        params2 = inparser.parse_file(args.files[1])
        pub1 = PubKey(params['n'], params['e'])
        pub2 = PubKey(params2['n'], params2['e'])
        plain = common_modulus(pub1, pub2, params['c'], params2['c'])
        return hex_to_str(plain)

    # e-root of c
    if args.eroot:
        print_title("RSA - eth-root")
        params = {"e":"65537", "c":""}
        types = {"e":"int", "c":"int"}
        defaults = {"e": 65537}
        get_parameters(params, types, defaults)
        plain = gmpy2.iroot(gmpy2.mpz(params['c']),params['e'])
        return hex_to_str(plain[0])

    # Hastad's attack
    elif args.hastad:
        # TODO
        print_title("RSA - Hastad")
        pks = [PubKey(params['n'], params['e'])]
        cs = [params['c']]
        for f in args.files[1:]:
            d = parse_file(f)
            pks.append(d['n'], d['e'])
            cs.append(d['c'])
        plain = hastad(pks, cs)
        return hex_to_str(plain)

    # Wiener's attack
    if args.wiener:
        print_title("RSA - Wiener")
        params = {"e":"65537", "n":""}
        types = {"e":"int", "n":"int"}
        defaults = {"e": 65537}
        if not args.nocipher:
            params["c"] = ""
            types["c"] = "int"
        get_parameters(params, types, defaults)
        pubk = PubKey(params['n'], params['e'])
        p, q, d = wiener(pubk)
        if not args.nocipher:
            privk = PrivKey(params["n"], d)
            plain = priv.decrypt(params["c"])
            return hex_to_str(plain)
        return [p, q, d]

    # Factorize n
    if args.factorize:
        print_title("RSA - Factorize")
        types = {"n":"int", "algo":"ustr"}
        defaults = {"algo":algo_def}
        while True:
            params = {"algo":algo_list}
            try:
                get_parameters(params, types, defaults)
                f = Factorizer(Algo[params["algo"]])
                break
            except KeyError:
                print("None, try again!")
        params = {"n":""}
        if not args.nocipher:
            params["c"], params["e"] = "", "65537"
            types["c"], types["e"] = "int", "int"
            defaults["e"] = 65537
        get_parameters(params, types, defaults)
        pq = f.factorize(params["n"])
        if not args.nocipher:
            r = RSA(pq[0], pq[1], params["e"])
            pub, priv = r.gen_keys()
            plain = priv.decrypt(params["c"])
            return plain
        return [pq[0], pq[1]]

    # Decrypt
    if args.decrypt:
        print_title("RSA - Decrypt")
        # Decrypt with primes p and q
        if args.primes:
            params = {"p":"", "q":"", "e":"", "c":""}
            types = {"p":"int", "q":"int", "e":"int", "c":"int"}
            defaults = {"e": 65537}
            get_parameters(params, types, defaults)
            r = RSA(params["p"], params["q"], params["e"])
            pub, priv = r.gen_keys()
        # Decrypt with private key (n, d)
        else:
            params = {"d":"", "n":"", "c":""}
            types = {"d":"int", "n":"int", "c":"int"}
            get_parameters(params, types)
            priv = PrivKey(params["n"], params["d"])
        plain = priv.decrypt(params["c"])
        return plain

    # Encrypt
    if args.encrypt:
        print_title("RSA - Encrypt")
        # Encrypt with primes p and q
        if args.primes:
            params = {"p":"", "q":"", "e":"", "m":""}
            types = {"p":"int", "q":"int", "e":"int", "m":"str"}
            defaults = {"e": 65537}
            get_parameters(params, types, defaults)
            r = RSA(params["p"], params["q"], params["e"])
            pub, priv = r.gen_keys()
        # Encrypt with public key (n, e)
        else:
            params = {"e":"", "n":"", "m":""}
            types = {"e":"int", "n":"int", "m":"str"}
            defaults = {"e": 65537}
            get_parameters(params, types, defaults)
            pub = PubKey(params["n"], params["e"])
        return pub.encrypt(params["m"])

# -------------------------------------------------------------------------- #

def handle_aes(parser, args):
    pass

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
    algo_default = "FACTORDB"
    rsaparser.add_argument("--nocipher", action="store_true",
            help="TODO")
    rsaparser.add_argument("--primes", action="store_true",
            help="TODO")
    exgr.add_argument("--common",action="store_true",
            help="common modulus attack (same n, same m)")
    exgr.add_argument("--decrypt",action="store_true",
            help="decrypt c with private key (n, d)")
    exgr.add_argument("--encrypt",action="store_true",
            help="encrypt m with public key (n, e)")
    exgr.add_argument("--eroot",action="store_true",
            help="compute the eth-root of c (big n, small e)")
    exgr.add_argument("--factorize",action="store_true",
            help="factorize n to decrypt c")
    exgr.add_argument("--hastad", action="store_true",
            help="Hastad's attack (same m sent e times)")
    exgr.add_argument("--wiener",action="store_true",
            help="Wiener's attack (d small)")

    # AES
    aesparser = subparser.add_parser("aes", help="AES")
    exga = aesparser.add_mutually_exclusive_group()
    exga.add_argument("--decrypt",action="store_true",
            help="decrypt c with private key (n, d)")
    exga.add_argument("--encrypt",action="store_true",
            help="encrypt m with public key (n, e)")
    # aesparser.add_argument("files", metavar="FILE", nargs="+", help="input file (refer to README.md for more details)")


    # TODO ceasar cipher
    # TODO vigenere
# TODO choose right handle
    args = parser.parse_args()
    out = handle_rsa(rsaparser, args)
    print(out)
