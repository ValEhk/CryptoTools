#!/usr/bin/env python

class FactorizationError(Exception):
    """General factorization error"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

class FactordbError(FactorizationError):
    pass

class UnitWarning(UserWarning):
    """Factorization of 1"""
    pass

class FactorizationWarning(UserWarning):
    """Unknown, incomplete or trivial factorization"""
    pass

# -------------------------------------------------------------------------- #

class RSAError(Exception):
    """General RSA Error"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

class WienerError(RSAError):
    pass
class HastadError(RSAError):
    pass
class CommonModError(RSAError):
    pass

# -------------------------------------------------------------------------- #

class FormatError(Exception):
    """Error raised when the input file is not correctly formatted"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

# -------------------------------------------------------------------------- #

class GF28Error(Exception):
    """General error occuring when computing values in GF(2^8)"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value