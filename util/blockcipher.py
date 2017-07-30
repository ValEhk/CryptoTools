from enum import IntEnum

class MODE(IntEnum):
    ECB = 0
    CBC = 1

class PADDING(IntEnum):
    NONE = 0
    ZERO = 1
    ANSI = 2
    PKCS7 = 3
