#!/usr/bin/env python3

import gmpy2

from RSA.rsa import *
from RSA.factorizer import Factorizer, Algo
from util.console import *

_algo_def = Algo.FACTORDB.name
_algo_list = ' / '.join([e.name.lower() for e in Algo]).replace(_algo_def.lower(), _algo_def)
_DEFAULT_ALGO = (_algo_list, "falgo", _algo_def)
_DEFAULT_E = ("65537", "int", "65537")
_DEFAULT_INT = ("", "int", None)
_DEFAULT_STR = ("", "str", None)

def handle_rsa(args):
    if args.action == "common":
        retval = _common(args)
    elif args.action == "eroot":
        retval = _eroot(args)
    elif args.action == "hastad":
        retval = _hastad(args)
    elif args.action == "wiener":
        retval = _wiener(args)
    elif args.action == "factorize":
        retval = _factorize(args)
    elif args.action == "decrypt":
        retval = _decrypt(args)
    elif args.action == "encrypt":
        retval = _encrypt(args)
    return retval

# -------------------------------------------------------------------------- #

def _encrypt(args):
    print_title("RSA - Encrypt")
    # Encrypt with primes p and q
    if args.primes:
        params = {"p":_DEFAULT_INT, "q":_DEFAULT_INT, "e":_DEFAULT_E, "m":_DEFAULT_STR}
        get_parameters(params)
        r = RSA(params["p"], params["q"], params["e"])
        pub, priv = r.gen_keys()
    # Encrypt with public key (n, e)
    else:
        params = {"e":_DEFAULT_E, "n":_DEFAULT_INT, "m":_DEFAULT_STR}
        get_parameters(params)
        pub = PubKey(params["n"], params["e"])
    return pub.encrypt(params["m"])

# -------------------------------------------------------------------------- #

def _decrypt(args):
        print_title("RSA - Decrypt")
        # Decrypt with primes p and q
        if args.primes:
            params = {"p":_DEFAULT_INT, "q":_DEFAULT_INT, "e":_DEFAULT_E, "c":_DEFAULT_INT}
            get_parameters(params)
            r = RSA(params["p"], params["q"], params["e"])
            pub, priv = r.gen_keys()
        # Decrypt with private key (n, d)
        else:
            params = {"d":_DEFAULT_INT, "n":_DEFAULT_INT, "c":_DEFAULT_INT}
            get_parameters(params)
            priv = PrivKey(params["n"], params["d"])
        plain = priv.decrypt(params["c"])
        return plain

# -------------------------------------------------------------------------- #

def _common(args):
        print_title("RSA - Common Modulus")
        params = {"n":_DEFAULT_INT}
        get_parameters(params)
        n = params["n"]
        pks, cs = [], []
        for i in range(e):
            print_subtitle("Values #{}".format(i+1))
            params = {"e":_DEFAULT_E, "c":_DEFAULT_INT}
            get_parameters(params)
            pks.append(n, PubKey(params["e"]))
            cs.append(params["c"])
        plain = common_modulus(pks[0], pks[1], cs[0], [1])
        return hex_to_str(plain)

# -------------------------------------------------------------------------- #

def _hastad(args):
        print_title("RSA - Hastad")
        params = {"e":_DEFAULT_E}
        get_parameters(params)
        e = params["e"]
        pks, cs = [], []
        for i in range(e):
            print_subtitle("Values #{}".format(i+1))
            params = {"n":_DEFAULT_INT, "c":_DEFAULT_INT}
            get_parameters(params)
            pks.append(PubKey(params["n"], e))
            cs.append(params["c"])
        plain = hastad(pks, cs)
        return hex_to_str(plain)

# -------------------------------------------------------------------------- #

def _factorize(args):
        print_title("RSA - Factorize")
        params = {"n":_DEFAULT_INT, "algo":_DEFAULT_ALGO}
        if not args.nocipher:
            params["c"], params["e"] = _DEFAULT_INT, _DEFAULT_E
        get_parameters(params)
        f = Factorizer(params["algo"])
        pq = f.factorize(params["n"])
        r = RSA(pq[0], pq[1], params["e"])
        pub, priv = r.gen_keys()
        if not args.nocipher:
            plain = priv.decrypt(params["c"])
            return plain
        return [pq[0], pq[1], priv.d]

# -------------------------------------------------------------------------- #

def _wiener(args):
        print_title("RSA - Wiener")
        params = {"e":_DEFAULT_E, "n":_DEFAULT_INT}
        if not args.nocipher:
            params["c"] = _DEFAULT_INT
        get_parameters(params)
        pubk = PubKey(params['n'], params['e'])
        p, q, d = wiener(pubk)
        if not args.nocipher:
            privk = PrivKey(params["n"], d)
            plain = priv.decrypt(params["c"])
            return hex_to_str(plain)
        return [p, q, d]

# -------------------------------------------------------------------------- #

def _eroot(args):
        print_title("RSA - eth-root")
        params = {"e":_DEFAULT_E, "c":_DEFAULT_INT}
        get_parameters(params)
        plain = gmpy2.iroot(gmpy2.mpz(params['c']),params['e'])
        return hex_to_str(plain[0])

