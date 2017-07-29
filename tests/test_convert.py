#!/usr/bin/env python3

from unittest import TestCase

from util.convert import *

class TestHex2Str(TestCase):
    def test_a2hstr(self):
        self.assertEqual(b"Z", hex_to_str(0x5a))
        self.assertEqual(b"Hello world!",
                hex_to_str(0x48656c6c6f20776f726c6421))
        bstr = b"1234567890\xc2\xb0+=)\xc3\xa0\xc3\xa7_\xc3\xa8-('\"\xc3\xa9&"
        hexval = 0x31323334353637383930c2b02b3d29c3a0c3a75fc3a82d282722c3a926
        self.assertEqual(bstr, hex_to_str(hexval))

    def test_a2harray(self):
        ha = [0x5a]
        self.assertEqual(b"Z", hexarray_to_str(ha))
        ha = [0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x20,
                0x77, 0x6f, 0x72, 0x6c, 0x64, 0x21]
        self.assertEqual(b"Hello world!", hexarray_to_str(ha))
        ha = [0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30,
                0xc2, 0xb0, 0x2b, 0x3d, 0x29, 0xc3, 0xa0, 0xc3, 0xa7, 0x5f,
                0xc3, 0xa8, 0x2d, 0x28, 0x27, 0x22, 0xc3, 0xa9, 0x26]
        bstr = b"1234567890\xc2\xb0+=)\xc3\xa0\xc3\xa7_\xc3\xa8-('\"\xc3\xa9&"
        self.assertEqual(bstr, hexarray_to_str(ha))

# -------------------------------------------------------------------------- #

class TestStr2Hex(TestCase):
    def test_hstr2ar(self):
        self.assertEqual(0x5a, str_to_hex(b"Z"))
        self.assertEqual(0x48656c6c6f20776f726c6421,
                str_to_hex(b"Hello world!"))
        bstr = b"1234567890\xc2\xb0+=)\xc3\xa0\xc3\xa7_\xc3\xa8-('\"\xc3\xa9&"
        hexpect = 0x31323334353637383930c2b02b3d29c3a0c3a75fc3a82d282722c3a926
        self.assertEqual(hexpect, str_to_hex(bstr))

    def test_harray2a(self):
        ha = [0x5a]
        self.assertEqual(ha, str_to_hexarray(b"Z"))
        ha = [0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x77,
                0x6f, 0x72, 0x6c, 0x64, 0x21]
        self.assertEqual(ha, str_to_hexarray(b"Hello world!"))
        ha = [0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30,
                0xc2, 0xb0, 0x2b, 0x3d, 0x29, 0xc3, 0xa0, 0xc3, 0xa7, 0x5f,
                0xc3, 0xa8, 0x2d, 0x28, 0x27, 0x22, 0xc3, 0xa9, 0x26]
        bstr = b"1234567890\xc2\xb0+=)\xc3\xa0\xc3\xa7_\xc3\xa8-('\"\xc3\xa9&"
        self.assertEqual(ha, str_to_hexarray(bstr))
