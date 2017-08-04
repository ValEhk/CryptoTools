#!/usr/bin/env python3

import sys
import gmpy2
from argparse import ArgumentParser, ArgumentError

from RSA.rsa import *
from RSA.factorizer import Factorizer, Algo
from AES.aes import *
from util.blockcipher import Mode, Padding
from util.convert import hex_to_str

def handle_rsa(args):
    if args.action == "common":
        pk1 = PrivKey(args.n, args.e[0])
        pk2 = PrivKey(args.n, args.e[1])
        return common_modulus(pk1, pk2, args.c[0], args.c[1])
    elif args.action == "eroot":
        plainmpz = gmpy2.iroot(gmpy2.mpz(args.c),args.e)
        return hex_to_str(plainmpz[0])
    elif args.action == "hastad":
        pks, cs = [], []
        for i in range(args.e):
            pks.append(PubKey(args.n[i], args.e))
            cs.append(args.c[i])
        return hastad(pks, cs)
    elif args.action == "wiener":
        pubk = PubKey(args.n, args.e)
        p, q, d = wiener(pubk)
        priv = PrivKey(args.n, d)
        return priv.decrypt(args.c)
    elif args.action == "factorize":
        f = Factorizer(Algo[args.algo])
        pq = f.factorize(args.n)
        r = RSA(pq[0], pq[1], args.e)
        pub, priv = r.gen_keys()
        return priv.decrypt(args.c)
    elif args.action == "decrypt":
        priv = PrivKey(args.n, args.d)
        return priv.decrypt(args.c)
    elif args.action == "decrypt-pq":
        r = RSA(args.p, args.q, args.e)
        pub, priv = r.gen_keys()
        return priv.decrypt(args.c)
    elif args.action == "encrypt":
        pub = PubKey(args.n, args.e)
        return pub.encrypt(args.m.encode())
    elif args.action == "encrypt-pq":
        r = RSA(args.p, args.q, args.e)
        pub, priv = r.gen_keys()
        return pub.encrypt(args.m.encode())

def handle_aes(args):
    aes = AES(args.key.encode(), Mode[args.mode], Padding[args.padding])
    if args.action == "encrypt":
        return aes.encrypt(args.m.encode())
    elif args.action == "decrypt":
        return aes.decrypt(args.c)

# -------------------------------------------------------------------------- #

def parse_int(value):
    return int(value, 0)

# TODO ceasar cipher
# TODO vigenere
# TODO change descr
if __name__ == "__main__":
    descr = ("Crypto-CTF is a small python tool providing a quick and easy ",
        "way to complete the basic cryptography challenges commonly found during CTFs.")
    parser = ArgumentParser(description=''.join(descr))
    parser.add_argument('--version', action='version', version="%(prog)s 1.0")
    subparser = parser.add_subparsers(dest="cmd")

    # RSA args
    rsaparser = subparser.add_parser("rsa", help="RSA cryptosystem")
    pq_argp = ArgumentParser(add_help=False)
    pq_argp.add_argument("-p", type=parse_int, required=True, help="first prime number")
    pq_argp.add_argument("-q", type=parse_int, required=True, help="second prime number")
    n_argp = ArgumentParser(add_help=False)
    n_argp.add_argument("-n", type=parse_int, required=True, help="modulus")
    e_argp = ArgumentParser(add_help=False)
    e_argp.add_argument("-e", type=parse_int, required=True, default=65537, help="public exponent")
    d_argp = ArgumentParser(add_help=False)
    d_argp.add_argument("-d", type=parse_int, required=True, help="private exponent")
    c_argp = ArgumentParser(add_help=False)
    c_argp.add_argument("-c", type=parse_int, required=True, help="ciphertext")
    m_argp = ArgumentParser(add_help=False)
    m_argp.add_argument("-m", required=True, help="plaintext")
    nlist_argp = ArgumentParser(add_help=False)
    nlist_argp.add_argument("-N", type=parse_int, nargs="+", required=True, help="list of moduli")
    e2_argp = ArgumentParser(add_help=False)
    e2_argp.add_argument("-e", type=parse_int, nargs=2, required=True, help="list of public exponents")
    c2_argp = ArgumentParser(add_help=False)
    c2_argp.add_argument("-C", type=parse_int, nargs=2, required=True, help="list of ciphertexts")
    elist_argp = ArgumentParser(add_help=False)
    elist_argp.add_argument("-E", type=parse_int, nargs="+", required=True, help="list of public exponents")
    clist_argp = ArgumentParser(add_help=False)
    clist_argp.add_argument("-C", type=parse_int, nargs="+", required=True, help="list of ciphertexts")

    # RSA parser
    rsasubs = rsaparser.add_subparsers(dest="action")
    rsasubs.add_parser("decrypt", parents=[n_argp, d_argp, c_argp],
            help="decrypt c with private key (n, d)")
    rsasubs.add_parser("decrypt-pq", parents=[pq_argp, e_argp, c_argp],
            help="decrypt c with primes p and q")
    rsasubs.add_parser("encrypt", parents=[n_argp, e_argp, m_argp],
            help="encrypt m with public key (n, e)")
    rsasubs.add_parser("encrypt-pq", parents=[pq_argp, e_argp, m_argp],
            help="encrypt m with primes p and q")
    rsasubs.add_parser("eroot", parents=[e_argp, c_argp],
            help="compute the eth-root of c (big n, small e)")
    factsub = rsasubs.add_parser("factorize", parents=[n_argp, e_argp, c_argp],
            help="factorize n to decrypt c")
    factsub.add_argument("--algo", default="FACTORDB",
            choices=[e.name for e in Algo],
            help="algorithm used to factorize n [FACTORDB]")
    rsasubs.add_parser("wiener", parents=[n_argp, e_argp, c_argp],
            help="Wiener's attack (d small)")
    commonsub = rsasubs.add_parser("common", parents=[n_argp],
            help="common modulus attack (same n, same m)")
    commonsub.add_argument("-e", type=parse_int, nargs=2, required=True,
            help="public exponents")
    commonsub.add_argument("-c", type=parse_int, nargs=2, required=True,
            help="ciphertexts")
    hastadsub = rsasubs.add_parser("hastad", parents=[e_argp],
            help="Hastad's attack (same m sent e times)")
    hastadsub.add_argument("-n", type=parse_int, nargs="+", required=True,
            help="list of moduli")
    hastadsub.add_argument("-c", type=parse_int, nargs="+", required=True,
            help="list of ciphertexts")

    # AES args
    key_argp = ArgumentParser(add_help=False)
    key_argp.add_argument("-k", "--key", required=True, help="secret key (16, 24 or 32 bytes)")
    mode_argp = ArgumentParser(add_help=False)
    mode_argp.add_argument("--mode", default="ECB", choices=[e.name for e in Mode],
            help="blockcipher encryption mode [ECB]")
    pad_argp = ArgumentParser(add_help=False)
    pad_argp.add_argument("--padding", default="PKCS7", choices=[e.name for e in Padding],
            help="Padding method [PKCS7]")

    # AES parser
    aesparser = subparser.add_parser("aes", help="AES-[128|192|224] encryption")
    aessubs = aesparser.add_subparsers(dest="action")
    decsub = aessubs.add_parser("decrypt", parents=[key_argp, mode_argp, pad_argp],
            help="decrypt c with key k")
    decsub.add_argument("-c", required=True, help="ciphertext")
    encsub = aessubs.add_parser("encrypt", parents=[key_argp, mode_argp, pad_argp],
            help="encrypt m with key k")
    encsub.add_argument("-m", required=True, help="plaintext")

    # Parse args
    args = parser.parse_args()
    if args.cmd == "rsa":
        print(handle_rsa(args))
    elif args.cmd == "aes":
        print(handle_aes(args))
    else:
        parser.print_help()


