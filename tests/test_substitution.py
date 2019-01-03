#!/usr/bin/env python3

from unittest import TestCase

from substitution.ceasar import rot
from substitution.xor import xorvalue
from substitution.vigenere import encrypt, decrypt

class TestCeasar(TestCase):
    def test_letters(self):
        plain = "deadbeef"
        self.assertEqual(plain, rot(plain, 0))
        self.assertEqual(plain, rot(plain, 26))
        self.assertEqual(plain, rot(rot(plain, 13), 13))
        plain = "HelloWorld"
        self.assertEqual(plain, rot(rot(plain, 13), 13))
        self.assertEqual(plain, rot(rot(plain, 10), 16))
        self.assertEqual(plain, rot(rot(plain, 20), 6))

    def test_ascii(self):
        plain = "deadb33f--*123457**"
        self.assertEqual(plain, rot(plain, 0))
        self.assertEqual(plain, rot(plain, 26))
        self.assertEqual(plain, rot(rot(plain, 13), 13))
        plain = "Hello World!"
        self.assertEqual(plain, rot(rot(plain, 13), 13))
        self.assertEqual(plain, rot(rot(plain, 10), 16))
        self.assertEqual(plain, rot(rot(plain, 20), 6))

# -------------------------------------------------------------------------- #

class TestXor(TestCase):
    def test_xor(self):
        plain = b"deadbeef"
        self.assertEqual(plain, xorvalue(plain, 0))
        self.assertEqual(plain, xorvalue(xorvalue(plain, 25), 25))
        self.assertEqual(plain, xorvalue(xorvalue(plain, 99), 99))
        plain = b"Hello World!"
        self.assertEqual(plain, xorvalue(plain, 0))
        self.assertEqual(plain, xorvalue(xorvalue(plain, 16), 16))
        self.assertEqual(plain, xorvalue(xorvalue(plain, 200), 200))


# -------------------------------------------------------------------------- #

class TestVigenere(TestCase):
    def test_basic(self):
        plain = "Hello World!"
        self.assertEqual(plain, encrypt(plain, "A"))
        self.assertEqual(plain, encrypt(plain, "aaaaaa"))
        plain = "deadbeef"
        self.assertEqual(rot(plain, 3), encrypt(plain, "dd"))

    def test_mixed(self):
        plain = "Hello World!"
        self.assertEqual(decrypt(encrypt(plain, "AZERTY"), "azerty"), plain)
        self.assertEqual(encrypt(encrypt(plain, "bZbzbZ"), "ZbZbzb"), plain)

# -------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main()
