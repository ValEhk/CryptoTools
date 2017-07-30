#!/usr/bin/env python3

import binascii
from unittest import TestCase
from Crypto.Cipher import AES as pyAES

from AES.aes import *
from AES.aesutil import *
from util.blockcipher import MODE, PADDING

class TestAES128_ECB(TestCase):
    def test_simple(self):
        plain = b"deadbeefdeadbeef"
        key = b"Yellow submarine"
        aes = AES(key, MODE.ECB, PADDING.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        plain = b"Submarine yellow"
        cipher = aes.encrypt(plain)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"\x00"*16
        plain = b"Hello world!!!!!"
        aes = AES(key, MODE.ECB, PADDING.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    def test_multiple(self):
        key = b"\x00"*16
        plain = b"Hello world!!!!  !!!!dlrow olleH"
        aes = AES(key, MODE.ECB, PADDING.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"Yellow submarine"
        plain = b"deadbeefdeadbeef"*10
        aes = AES(key, MODE.ECB, PADDING.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    # def test_padding(self):
    #     pass

# -------------------------------------------------------------------------- #

class TestAES192_ECB(TestCase):
    def test_simple(self):
        plain = b"deadbeefdeadbeef"
        key = b"Yellow submarineazertyui"
        aes = AES(key, MODE.ECB, PADDING.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        plain = b"Submarine yellow"
        cipher = aes.encrypt(plain)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"\x00"*24
        plain = b"Hello world!!!!!"
        aes = AES(key, MODE.ECB, PADDING.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    def test_multiple(self):
        key = b"\x00"*24
        plain = b"Hello world!!!!  !!!!dlrow olleH"
        aes = AES(key, MODE.ECB, PADDING.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"Yellow submarine01234567"
        plain = b"deadbeefdeadbeef"*10
        aes = AES(key, MODE.ECB, PADDING.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    # def test_padding(self):
    #     pass

# -------------------------------------------------------------------------- #

class TestAES256_ECB(TestCase):
    def test_simple(self):
        plain = b"deadbeefdeadbeef"
        key = b"Yellow submarineYellow submarine"
        aes = AES(key, MODE.ECB, PADDING.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        plain = b"Submarine yellow"
        cipher = aes.encrypt(plain)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"\x00"*32
        plain = b"Hello world!!!!!"
        aes = AES(key, MODE.ECB, PADDING.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    def test_multiple(self):
        key = b"\x00"*32
        plain = b"Hello world!!!!  !!!!dlrow olleH"
        aes = AES(key, MODE.ECB, PADDING.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

        key = b"Yellow submarineYellow submarine"
        plain = b"deadbeefdeadbeef"*10
        aes = AES(key, MODE.ECB, PADDING.NONE)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain))
        self.assertEqual(cipher.hex(), expected.decode())
        self.assertEqual(aes.decrypt(cipher), plain)

    # def test_padding(self):
    #     pass

# -------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main()
