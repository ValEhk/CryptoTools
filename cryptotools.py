#!/usr/bin/env python3

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import gmpy2

import substitution.vigenere as vig
from substitution.ceasar import rot
from substitution.xor import xorvalue
from factorizer.factorizer import Factorizer, Algo
from asymmetric.rsa import RSA, PrivKey, PubKey, wiener, hastad, common_modulus
from symmetric.aes import AES
from symmetric.padoracle import padding_oracle
from dlp.dlp import discrete_log
from util.blockcipher import Mode, Padding
from util.convert import hex_to_str

def handle_factorize(args):
    f = Factorizer(Algo[args.algo], args.limit)
    return f.factorize(args.n)

def handle_rsa(args):
    if args.action == "common":
        pk1 = PrivKey(args.n, args.e[0])
        pk2 = PrivKey(args.n, args.e[1])
        return common_modulus(pk1, pk2, args.c[0], args.c[1])
    elif args.action == "eroot":
        plainmpz = gmpy2.iroot(gmpy2.mpz(args.c), args.e)
        return hex_to_str(plainmpz[0])
    elif args.action == "hastad":
        pks, cs = [], []
        for i in range(args.e):
            pks.append(PubKey(args.n[i], args.e))
            cs.append(args.c[i])
        return hastad(pks, cs)
    elif args.action == "wiener":
        pubk = PubKey(args.n, args.e)
        _, _, d = wiener(pubk)
        priv = PrivKey(args.n, d)
        return priv.decrypt(args.c)
    elif args.action == "crack":
        f = Factorizer(Algo[args.algo], args.limit)
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
    if args.action == "oracle":
        host = {}
        host["hostname"] = args.host
        host["port"] = args.port
        host["error"] = args.error.encode()
        return padding_oracle(args.c.encode(), host)
    if args.iv:
        args.iv = args.iv.encode()
    aes = AES(args.key.encode(), Mode[args.mode], Padding[args.padding], args.iv)
    if args.action == "encrypt":
        return aes.encrypt(args.m.encode())
    elif args.action == "decrypt":
        return aes.decrypt(args.c)

def handle_rot(args):
    if args.all:
        for i in range(26):
            print(rot(args.input, i))
    else:
        print(rot(args.input, args.key))

def handle_xor(args):
    if args.range:
        for i in range(args.range[0], args.range[1]):
            print(xorvalue(args.input.encode(), i))
    else:
        print(xorvalue(args.input.encode(), args.key))

def handle_vigenere(args):
    if args.action == "encrypt":
        return vig.encrypt(args.input, args.key)
    elif args.action == "decrypt":
        return vig.decrypt(args.input, args.key)

def handle_dlp(args):
    return discrete_log(args.g, args.h, args.n)

# -------------------------------------------------------------------------- #

def parse_int(value):
    return int(value, 0)

if __name__ == "__main__":
    descr = ("CryptoTools is a small python tool providing a quick and easy ",
             "way to complete the basic cryptography challenges commonly found during CTFs.",
             "\n\nCurrently available are:",
             "\n    * string rotation/Ceasar cipher;",
             "\n    * xor on strings;",
             "\n    * Vigenere cipher;",
             "\n    * prime factorization;",
             "\n    * RSA basic encryption/decryption;",
             "\n    * common RSA attacks such as Wiener, Hastad or common modulus;",
             "\n    * AES-128, AES-192, AES-224 (ECB or CBC) with multiple padding choice;",
             "\n    * CBC padding oracle attack.",
             "\n    * resolution of the discrete logarithm problem based on Pohlig-Hellman algorithm.")
    parser = ArgumentParser(description=''.join(descr), formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('--version', action='version', version="%(prog)s 1.0")
    subparser = parser.add_subparsers(dest="cmd")

    # Factorize parser
    factoparser = subparser.add_parser("factorize", help="prime factorization")
    factoparser.add_argument("--algo", default="FACTORDB",
                             choices=[e.name for e in Algo],
                             help="algorithm used to factorize n (default FACTORDB)")
    factoparser.add_argument("--limit", default=10000, type=parse_int,
                             help="maximum number of tries (SMALL_PRIMES and FERMAT only) (default 10000)")
    factoparser.add_argument("n", type=parse_int, help="number to factorize [int]")

    # RSA args
    rsaparser = subparser.add_parser("rsa", help="RSA cryptosystem")
    pq_argp = ArgumentParser(add_help=False)
    pq_argp.add_argument("-p", type=parse_int, required=True, help="first prime number [int]")
    pq_argp.add_argument("-q", type=parse_int, required=True, help="second prime number [int]")
    n_argp = ArgumentParser(add_help=False)
    n_argp.add_argument("-n", type=parse_int, required=True, help="modulus [int]")
    e_argp = ArgumentParser(add_help=False)
    e_argp.add_argument("-e", type=parse_int, required=True, default=65537, help="public exponent [int]")
    d_argp = ArgumentParser(add_help=False)
    d_argp.add_argument("-d", type=parse_int, required=True, help="private exponent [int]")
    c_argp = ArgumentParser(add_help=False)
    c_argp.add_argument("-c", type=parse_int, required=True, help="ciphertext [int]")
    m_argp = ArgumentParser(add_help=False)
    m_argp.add_argument("-m", required=True, help="plaintext [string]")
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
    factsub = rsasubs.add_parser("crack", parents=[n_argp, e_argp, c_argp],
                                 help="try to factorize n to decrypt c")
    factsub.add_argument("--algo", default="FACTORDB",
                         choices=[e.name for e in Algo],
                         help="algorithm used to factorize n (default FACTORDB)")
    factsub.add_argument("--limit", default=10000, type=parse_int,
                         help="maximum number of tries (SMALL_PRIMES and FERMAT only) (default 10000)")
    rsasubs.add_parser("wiener", parents=[n_argp, e_argp, c_argp],
                       help="Wiener's attack (d small)")
    commonsub = rsasubs.add_parser("common", parents=[n_argp],
                                   help="common modulus attack (same n, same m)")
    commonsub.add_argument("-e", type=parse_int, nargs=2, required=True,
                           help="two public exponents [int]")
    commonsub.add_argument("-c", type=parse_int, nargs=2, required=True,
                           help="two ciphertexts [int]")
    hastadsub = rsasubs.add_parser("hastad", parents=[e_argp],
                                   help="Hastad's attack (same m sent e times)")
    hastadsub.add_argument("-n", type=parse_int, nargs="+", required=True,
                           help="list of moduli [List<int>]")
    hastadsub.add_argument("-c", type=parse_int, nargs="+", required=True,
                           help="list of ciphertexts [List<int>]")

    # AES args
    key_argp = ArgumentParser(add_help=False)
    key_argp.add_argument("-k", "--key", required=True, help="secret key [string] (16, 24 or 32 bytes)")
    mode_argp = ArgumentParser(add_help=False)
    mode_argp.add_argument("--mode", default="ECB", choices=[e.name for e in Mode],
                           help="blockcipher encryption mode (default ECB)")
    pad_argp = ArgumentParser(add_help=False)
    pad_argp.add_argument("--padding", default="PKCS7", choices=[e.name for e in Padding],
                          help="Padding method (default PKCS7)")
    iv_argp = ArgumentParser(add_help=False)
    iv_argp.add_argument("--iv", default=None, help="CBC initialization vector [string] (16 bytes)")
    # AES parser
    aesparser = subparser.add_parser("aes", help="AES-[128|192|224] encryption")
    aessubs = aesparser.add_subparsers(dest="action")
    decsub = aessubs.add_parser("decrypt", parents=[key_argp, mode_argp, pad_argp, iv_argp],
                                help="decrypt c with key k")
    decsub.add_argument("-c", required=True, help="ciphertext [hex string]")
    encsub = aessubs.add_parser("encrypt", parents=[key_argp, mode_argp, pad_argp, iv_argp],
                                help="encrypt m with key k")
    encsub.add_argument("-m", required=True, help="plaintext [string]")
    oraclesub = aessubs.add_parser("oracle", help="Decrypt 'c' using CBC padding oracle attack")
    oraclesub.add_argument("-c", required=True, help="ciphertext [hex string]")
    oraclesub.add_argument("--host", required=True, help="Hostname/IP adress [string]")
    oraclesub.add_argument("-p", "--port", required=True, type=parse_int, help="port [int]")
    oraclesub.add_argument("--error", default="Error",
                           help="text received on error [string] (default 'Error')")

    # Rot parser
    rotparser = subparser.add_parser("rot", help="Ceasar cipher / string rotation")
    rotexcl = rotparser.add_mutually_exclusive_group()
    rotexcl.add_argument("-k", "--key", type=parse_int, default=13,
                         help="shift [int] (default 13)")
    rotexcl.add_argument("--all", action="store_true", help="print all 26 rotations")
    rotparser.add_argument("input", help="text to be rotated [string]")

    # Xor parser
    xorparser = subparser.add_parser("xor", help="xor string with the given value/range")
    xorexcl = xorparser.add_mutually_exclusive_group(required=True)
    xorexcl.add_argument("-k", "--key", type=parse_int, help="xor value [int]")
    xorexcl.add_argument("--range", nargs=2, type=parse_int, metavar=('MIN', 'MAX'),
                         help="range of xor values [min, max[")
    xorparser.add_argument("input", help="text to be xored [string]")

    # Vigenere parser
    vin_argp = ArgumentParser(add_help=False)
    vin_argp.add_argument("input", help="input text [string]")
    vkey_argp = ArgumentParser(add_help=False)
    vkey_argp.add_argument("-k", "--key", required=True, help="key [string]")
    vigparser = subparser.add_parser("vigenere", help="Vigenere cipher")
    vigsubs = vigparser.add_subparsers(dest="action")
    vdecsub = vigsubs.add_parser("decrypt", parents=[vin_argp, vkey_argp],
                                 help="Decrypt 'input' with key k")
    vencsub = vigsubs.add_parser("encrypt", parents=[vin_argp, vkey_argp],
                                 help="Encrypt 'input' with key k")

    # DLP parser
    dlpparser = subparser.add_parser("dlp", help="discrete logarithm problem")
    dlpparser.add_argument("g", type=parse_int, help="h=g^x mod n [int]")
    dlpparser.add_argument("h", type=parse_int, help="h=g^x mod n [int]")
    dlpparser.add_argument("n", type=parse_int, help="modulo [int]")

    # Parse args
    args_parser = parser.parse_args()
    if args_parser.cmd == "factorize":
        print(handle_factorize(args_parser))
    elif args_parser.cmd == "rsa":
        print(handle_rsa(args_parser))
    elif args_parser.cmd == "aes":
        print(handle_aes(args_parser))
    elif args_parser.cmd == "rot":
        handle_rot(args_parser)
    elif args_parser.cmd == "xor":
        handle_xor(args_parser)
    elif args_parser.cmd == "vigenere":
        print(handle_vigenere(args_parser))
    elif args_parser.cmd == "dlp":
        print(handle_dlp(args_parser))
    else:
        parser.print_help()
