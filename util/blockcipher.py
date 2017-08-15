from enum import IntEnum

class Mode(IntEnum):
    """Encryption mode."""
    ECB = 0
    CBC = 1

class Padding(IntEnum):
    """Padding scheme."""
    NONE = 0
    ZERO = 1
    ANSI = 2
    PKCS7 = 3
