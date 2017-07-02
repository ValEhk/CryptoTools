# Crypto-CTF
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Crypto-CTF is a small python tool providing a quick and easy way to complete the basic cryptography challenges commonly found during CTFs.  
It can also be used to simply encrypt/decrypt messages, although it is likely not as good as the "official" encryption packages.

_Currently, only RSA is available. Stay tuned for more._


Usage
-----
    usage: crypto-ctf.py [-h] [--version] {rsa} ... FILE [FILE ...]

    Crypto-CTF is a small python tool providing a quick and easy way to complete
    the basic cryptography challenges commonly found during CTFs.

    positional arguments:
    {rsa}       encryption method used
    FILE        input file (refer to README.md for more details)

    optional arguments:
    -h, --help  show this help message and exit
    --version   show program's version number and exit


Input file
----------
The input file must be made of lines respecting the following syntax:

> _id_ **=** _number_
    
with _id_ being one of the following: m, c, n, d, e, p or q.  
The _number_ value can be expressed either in decimal or in hexadecimal. Blank lines are not allowed and will result in a crash.

Depending on what you want to do, you don't have to put the same identifiers in the input file.  
If some identifiers are missing, the program will stop with a `KeyError`. If more identifiers than required are provided, the programm will probably do something that will depend on the order of the given identifiers.


Required packages
-----------------
- `argparse`
- `gmpy2`  

Additionally, other packages might be required depending on what you want to do:
- `sympy` if you want to use the _sympy_ built_in factorization function
- `urllib`, `bs4` and `parsimonious` if you use [factordb](http://factordb.com/)


License
-------
The project is distributed under the MIT License. See [LICENSE](https://github.com/ValEhk/RSActf/blob/master/LICENSE) for more details.
