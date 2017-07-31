from enum import IntEnum

class Mode(IntEnum):
    ECB = 0
    CBC = 1

class Padding(IntEnum):
    NONE = 0
    ZERO = 1
    ANSI = 2
    PKCS7 = 3
