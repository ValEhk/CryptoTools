#!/usr/bin/env python3

from unittest import TestCase

from AES.aes import *
from util.blockcipher import MODE
from util.inparser import hex_to_ascii, ascii_to_hex

class TestSteps(TestCase):
    def test_shift_rows(self):
        state = [[215, 99, 175, 64], [35, 18, 241, 164],
                [38, 110, 38, 18], [80, 143, 54, 229]]
        expected = [[215, 99, 175, 64], [18, 241, 164, 35],
                [38, 18, 38, 110], [229, 80, 143, 54]]
        aesmat = AES_Matrix(state)
        aesmat.shift_rows()
        self.assertEqual(aesmat.state, expected)

    def test_mix_columns(self):
        state = [[215, 99, 175, 64], [18, 241, 164, 35],
                [38, 18, 38, 110], [229, 80, 143, 54]]
        expected = [[64, 140, 27, 189], [124, 252, 25, 130],
                [189, 70, 205, 229], [135, 230, 109, 225]]
        aesmat = AES_Matrix(state)
        aesmat.mix_columns()
        self.assertEqual(aesmat.state, expected)
        state = [[11, 231, 231, 4], [1, 202, 79, 97],
                [45, 243, 19, 121], [93, 142, 84, 51]]
        expected = [[101, 237, 67, 225], [35, 232, 24, 126],
                [183, 89, 114, 194], [139, 12, 198, 114]] 
        aesmat = AES_Matrix(state)
        aesmat.mix_columns()
        self.assertEqual(aesmat.state, expected)


    def test_sub_bytes(self):
        state = [[13, 0, 27, 114], [50, 57, 43, 29],
                [35, 69, 35, 57], [108, 115, 36, 42]]
        expected = [[215, 99, 175, 64], [35, 18, 241, 164],
                [38, 110, 38, 18], [80, 143, 54, 229]]
        aesmat = AES_Matrix(state)
        aesmat.sub_bytes()
        self.assertEqual(aesmat.state, expected)

# -------------------------------------------------------------------------- #

# class TestAES128(TestCase):
#     def test_ecb_simple(self):
#         key = "deadbeefdeadbeef"
#         plain = "Yellow submarine"
#         aes = AES(key, MODE.ECB)
#         cipher = aes.encrypt(plain)
#         self.assertEqual(cipher, "8b21bdc14d0b6faf5cfe16e56d043d36")
#         self.assertEqual(aes.decrypt(cipher), plain)
#         plain = "Submarine yellow"
#         cipher = aes.encrypt(plain)
#         self.assertEqual(cipher, "03570ff2f7901421c5ced79515f6ffb8")
#         self.assertEqual(aes.decrypt(cipher), plain)
#         key = "\x00"*16
#         plain = "Hello world!!!!!"
#         aes = AES(key, MODE.ECB)
#         cipher = aes.encrypt(plain)
#         self.assertEqual(cipher, "d13533881e4de1b0c60c761d0231936c")
#         self.assertEqual(aes.decrypt(cipher), plain)

#     def test_ecb_padding(self):
#         pass

#     def test_error(sefl):
#         pass

# -------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main()
