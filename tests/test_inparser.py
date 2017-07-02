#!/usr/bin/env python3

from unittest import TestCase

from util.inparser import *

class TestHex2Ascii(TestCase):
    def test_a2hstr(self):
        self.assertEqual("Z", hex_to_ascii(0x5a))
        self.assertEqual("Hello world!", hex_to_ascii(0x48656c6c6f20776f726c6421))
        self.assertEqual("1234567890°+=)àç_è-('\"é&", hex_to_ascii(0x31323334353637383930c2b02b3d29c3a0c3a75fc3a82d282722c3a926))

    def test_a2harray(self):
        ha = [0x5a]
        self.assertEqual("Z", hexarray_to_ascii(ha))
        ha = [0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x77, 0x6f, 0x72, 0x6c, 0x64, 0x21]
        self.assertEqual("Hello world!", hexarray_to_ascii(ha))
        ha = [0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0xc2, 0xb0, 0x2b, 0x3d,\
	    0x29, 0xc3, 0xa0, 0xc3, 0xa7, 0x5f, 0xc3, 0xa8, 0x2d, 0x28, 0x27, 0x22, 0xc3, 0xa9, 0x26]
        self.assertEqual("1234567890°+=)àç_è-('\"é&", hexarray_to_ascii(ha))

# -------------------------------------------------------------------------- #

class TestAscii2Hex(TestCase):
    def test_hstr2ar(self):
        self.assertEqual(0x5a, ascii_to_hex("Z"))
        self.assertEqual(0x48656c6c6f20776f726c6421, ascii_to_hex("Hello world!"))
        self.assertEqual(0x31323334353637383930c2b02b3d29c3a0c3a75fc3a82d282722c3a926, ascii_to_hex("1234567890°+=)àç_è-('\"é&"))

    def test_harray2a(self):
        ha = [0x5a]
        self.assertEqual(ha, ascii_to_hexarray("Z"))
        ha = [0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x77, 0x6f, 0x72, 0x6c, 0x64, 0x21]
        self.assertEqual(ha, ascii_to_hexarray("Hello world!"))
        ha = [0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0xc2, 0xb0, 0x2b, 0x3d,\
	    0x29, 0xc3, 0xa0, 0xc3, 0xa7, 0x5f, 0xc3, 0xa8, 0x2d, 0x28, 0x27, 0x22, 0xc3, 0xa9, 0x26]
        self.assertEqual(ha, ascii_to_hexarray("1234567890°+=)àç_è-('\"é&"))
