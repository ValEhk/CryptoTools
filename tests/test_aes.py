#!/usr/bin/env python3

import binascii
from unittest import TestCase
from Crypto.Cipher import AES as pyAES

from AES.aes import *
from AES.aesutil import *
from util.blockcipher import MODE

class TestAESECB(TestCase):
    def test_simple(self):
        plain = "deadbeefdeadbeef"
        key = "Yellow submarine"
        aes = AES(key, MODE.ECB)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain)).decode()
        self.assertEqual(cipher, expected)
        self.assertEqual(aes.decrypt(cipher), plain)

        plain = "Submarine yellow"
        cipher = aes.encrypt(plain)
        expected = binascii.hexlify(aestrue.encrypt(plain)).decode()
        self.assertEqual(cipher, expected)
        self.assertEqual(aes.decrypt(cipher), plain)

        key = "\x00"*16
        plain = "Hello world!!!!!"
        aes = AES(key, MODE.ECB)
        cipher = aes.encrypt(plain)
        aestrue = pyAES.new(key, pyAES.MODE_ECB)
        expected = binascii.hexlify(aestrue.encrypt(plain)).decode()
        self.assertEqual(cipher, expected)
        self.assertEqual(aes.decrypt(cipher), plain)

    def test_multiple(self):
        pass

    def test_padding(self):
        pass

    def test_error(sefl):
        pass

# -------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main()
