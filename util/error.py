#!/usr/bin/env python3

class FactorizationError(Exception):
    """Generic factorization error."""
    def __init__(self, value):
        super().__init__(value)
        self.value = value
    def __str__(self):
        return self.value

class FactordbError(FactorizationError):
    """FactorDB error."""
    pass

class UnitWarning(UserWarning):
    """Factorization of 1."""
    pass

class FactorizationWarning(UserWarning):
    """Unknown, incomplete or trivial factorization."""
    pass

# -------------------------------------------------------------------------- #

class RSAError(Exception):
    """Generic RSA error."""
    def __init__(self, value):
        super().__init__(value)
        self.value = value
    def __str__(self):
        return self.value

class WienerError(RSAError):
    """Wiener's attack error."""
    pass
class HastadError(RSAError):
    """Hastad's attack error."""
    pass
class CommonModError(RSAError):
    """Common modulus attack error."""
    pass

# -------------------------------------------------------------------------- #

class GF28Error(Exception):
    """Generic GF(2^8) operations error."""
    def __init__(self, value):
        super().__init__(value)
        self.value = value
    def __str__(self):
        return self.value

# -------------------------------------------------------------------------- #

class AESError(Exception):
    """Generic AES error."""
    def __init__(self, value):
        super().__init__(value)
        self.value = value
    def __str__(self):
        return self.value

# -------------------------------------------------------------------------- #

class PaddingError(Exception):
    """Invalid PKCS7 or ANSI X.923 padding detected."""
    def __init__(self, value):
        super().__init__(value)
        self.value = value
    def __str__(self):
        return self.value

# -------------------------------------------------------------------------- #

class PadOracleError(Exception):
    """Generic padding oracle attack error."""
    def __init__(self, value):
        super().__init__(value)
        self.value = value
    def __str__(self):
        return self.value
