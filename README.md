# CryptoTools
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CryptoTools is a small python tool providing a quick and easy way to complete the basic cryptography challenges commonly found during CTFs.
It can also be used to simply encrypt/decrypt messages, although it is likely not as good as the "official" encryption packages.

Currently available are:
* string rotation/Ceasar cipher;
* xor on strings;
* Vigenere cipher;
* prime factorization;
* RSA basic encryption/decryption;
* common RSA attacks such as Wiener, Hastad or common modulus;
* AES-128, AES-192, AES-224 (ECB or CBC) with multiple padding choice;


Usage
-----
    usage: cryptotools.py [-h] [--version] {factorize, rsa,aes,rot,xor,vigenere} ...

    positional arguments:
    {factorize, rsa,aes,rot,xor,vigenere}
        factorize           prime factorization
        rsa                 RSA cryptosystem
        aes                 AES-[128|192|224] encryption
        rot                 Ceasar cipher / string rotation
        xor                 xor string with the given value/range
        vigenere            Vigenere cipher

    optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit

Additional help can be found by using the option `-help` or `-h` with a specific subcommand.


Required packages
-----------------
- `argparse`
- `gmpy2`
- `urllib`, `bs4` and `parsimonious` for the factorization with [factordb](http://factordb.com/)


License
-------
The project is distributed under the MIT License. See [LICENSE](https://github.com/ValEhk/RSActf/blob/master/LICENSE) for more details.
