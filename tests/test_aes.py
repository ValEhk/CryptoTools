#!/usr/bin/env python3

import binascii
from unittest import TestCase
from Crypto.Cipher import AES as pyAES

from symmetric.aes import AES
from util.blockcipher import Mode, Padding

class TestAES128_ECB(TestCase):
    def test_simple(self):
        plain = b"deadbeefdeadbeef"
        key = b"Yellow submarine"
        aes = AES(key, Mode.ECB, Padding.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        plain = b"Submarine yellow"
        cipher = aes.encrypt(plain)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"\x00"*16
        plain = b"Hello world!!!!!"
        aes = AES(key, Mode.ECB, Padding.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    def test_multiple(self):
        key = b"\x00"*16
        plain = b"Hello world!!!!  !!!!dlrow olleH"
        aes = AES(key, Mode.ECB, Padding.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"Yellow submarine"
        plain = b"deadbeefdeadbeef"*10
        aes = AES(key, Mode.ECB, Padding.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

# -------------------------------------------------------------------------- #

class TestAES192_ECB(TestCase):
    def test_simple(self):
        plain = b"deadbeefdeadbeef"
        key = b"Yellow submarineazertyui"
        aes = AES(key, Mode.ECB, Padding.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        plain = b"Submarine yellow"
        cipher = aes.encrypt(plain)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"\x00"*24
        plain = b"Hello world!!!!!"
        aes = AES(key, Mode.ECB, Padding.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    def test_multiple(self):
        key = b"\x00"*24
        plain = b"Hello world!!!!  !!!!dlrow olleH"
        aes = AES(key, Mode.ECB, Padding.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"Yellow submarine01234567"
        plain = b"deadbeefdeadbeef"*10
        aes = AES(key, Mode.ECB, Padding.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

# -------------------------------------------------------------------------- #

class TestAES256_ECB(TestCase):
    def test_simple(self):
        plain = b"deadbeefdeadbeef"
        key = b"Yellow submarineYellow submarine"
        aes = AES(key, Mode.ECB, Padding.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        plain = b"Submarine yellow"
        cipher = aes.encrypt(plain)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"\x00"*32
        plain = b"Hello world!!!!!"
        aes = AES(key, Mode.ECB, Padding.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    def test_multiple(self):
        key = b"\x00"*32
        plain = b"Hello world!!!!  !!!!dlrow olleH"
        aes = AES(key, Mode.ECB, Padding.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"Yellow submarineYellow submarine"
        plain = b"deadbeefdeadbeef"*10
        aes = AES(key, Mode.ECB, Padding.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

class TestAES128_CBC(TestCase):
    def test_simple(self):
        iv = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        plain = b"deadbeefdeadbeef"
        key = b"Yellow submarine"
        aes = AES(key, Mode.CBC, Padding.NONE, iv)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        plain = b"Submarine yellow"
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"\x00"*16
        plain = b"Hello world!!!!!"
        aes = AES(key, Mode.CBC, Padding.NONE, iv)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    def test_multiple(self):
        iv = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        key = b"\x00"*16
        plain = b"Hello world!!!!  !!!!dlrow olleH"
        aes = AES(key, Mode.CBC, Padding.NONE, iv)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"Yellow submarine"
        plain = b"deadbeefdeadbeef"*10
        aes = AES(key, Mode.CBC, Padding.NONE, iv)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

# -------------------------------------------------------------------------- #

class TestAES192_CBC(TestCase):
    def test_simple(self):
        iv = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        plain = b"deadbeefdeadbeef"
        key = b"Yellow submarineazertyui"
        aes = AES(key, Mode.CBC, Padding.NONE, iv)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        plain = b"Submarine yellow"
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"\x00"*24
        plain = b"Hello world!!!!!"
        aes = AES(key, Mode.CBC, Padding.NONE, iv)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    def test_multiple(self):
        iv = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        key = b"\x00"*24
        plain = b"Hello world!!!!  !!!!dlrow olleH"
        aes = AES(key, Mode.CBC, Padding.NONE, iv)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"Yellow submarine01234567"
        plain = b"deadbeefdeadbeef"*10
        aes = AES(key, Mode.CBC, Padding.NONE, iv)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

# -------------------------------------------------------------------------- #

class TestAES256_CBC(TestCase):
    def test_zero(self):
        iv = b"\xca"*16
        plain = b"deadbeef"
        key = b"Yellow submarine"
        aes = AES(key, Mode.CBC, Padding.ZERO, iv)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain + bytes(8)))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    def test_ansi(self):
        iv = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        plain = b"deadbeef"
        key = b"Yellow submarine"
        aes = AES(key, Mode.CBC, Padding.ANSI, iv)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain + bytes(7) + b"\x08"))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    def test_pkcs(self):
        iv = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        plain = b"deadbeef"
        key = b"Yellow submarine"
        aes = AES(key, Mode.CBC, Padding.PKCS7, iv)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_CBC, iv)
        expected = binascii.hexlify(aestrue.encrypt(plain + b"\x08"*8))
        self.assertEqual(cipher, expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

# -------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main()
