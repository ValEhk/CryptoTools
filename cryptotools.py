#!/usr/bin/env python3

import sys

from argparse import ArgumentParser, ArgumentError

from AES.parser import handle_aes
from RSA.parser import handle_rsa

# TODO ceasar cipher
# TODO vigenere
if __name__ == "__main__":
    descr = ("Crypto-CTF is a small python tool providing a quick and easy ",
        "way to complete the basic cryptography challenges commonly found during CTFs.")
    parser = ArgumentParser(description=''.join(descr))
    parser.add_argument('--version', action='version', version="%(prog)s 1.0")
    subparser = parser.add_subparsers(dest="cmd")

    # RSA
    rsaparser = subparser.add_parser("rsa", help="RSA cryptosystem")
    rsasubs = rsaparser.add_subparsers(dest="action")
    primes_help = ("encrypt/decrypt m from primes p and q instead of ",
        "directly using the private or the public key")
    rsaparser.add_argument("-p", "--primes", action="store_true", help="".join(primes_help))
    rsaparser.add_argument("-n", "--nocipher", action="store_true",
            help="stop after RSA keys have been generated and return p, q and d")
    rsasubs.add_parser("common", help="common modulus attack (same n, same m)")
    rsasubs.add_parser("decrypt", help="decrypt c with private key (n, d)")
    rsasubs.add_parser("encrypt", help="encrypt m with public key (n, e)")
    rsasubs.add_parser("eroot", help="compute the eth-root of c (big n, small e)")
    rsasubs.add_parser("factorize", help="factorize n to decrypt c")
    rsasubs.add_parser("hastad", help="Hastad's attack (same m sent e times)")
    rsasubs.add_parser("wiener", help="Wiener's attack (d small)")

    # AES
    aesparser = subparser.add_parser("aes", help="AES-[128|192|224] encryption")
    aessubs = aesparser.add_subparsers(dest="action")
    aessubs.add_parser("decrypt", help="decrypt c with private key (n, d)")
    aessubs.add_parser("encrypt", help="encrypt m with public key (n, e)")

    # Parse command line
    if len(sys.argv[1:])==0:
        parser.print_usage()
        parser.exit()

    args = parser.parse_args()
    if args.cmd == "rsa":
        out = handle_rsa(args)
    elif args.cmd == "aes":
        out = handle_aes(args)
    print(out)


