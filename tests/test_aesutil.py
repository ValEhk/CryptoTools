#!/usr/bin/env python3

import binascii
from unittest import TestCase

from AES.aesutil import *
from util.blockcipher import MODE
from util.convert import hex_to_ascii, ascii_to_hex

class TestSteps(TestCase):
    def test_key_sched(self):
        key = "YELLOW SUBMARINE"
        expected = [89, 69, 76, 76, 79, 87, 32, 83, 85, 66, 77, 65, 82, 73,
                78, 69, 99, 106, 34, 76, 44, 61, 2, 31, 121, 127, 79, 94, 43,
                54, 1, 27, 100, 22, 141, 189, 72, 43, 143, 162, 49, 84, 192,
                252, 26, 98, 193, 231, 202, 110, 25, 31, 130, 69, 150, 189,
                179, 17, 86, 65, 169, 115, 151, 166, 77, 230, 61, 204, 207,
                163, 171, 113, 124, 178, 253, 48, 213, 193, 106, 150, 37, 228,
                173, 207, 234, 71, 6, 190, 150, 245, 251, 142, 67, 52, 145,
                24, 29, 101, 0, 213, 247, 34, 6, 107, 97, 215, 253, 229, 34,
                227, 108, 253, 76, 53, 84, 70, 187, 23, 82, 45, 218, 192, 175,
                200, 248, 35, 195, 53, 234, 27, 194, 7, 81, 12, 144, 42, 139,
                204, 63, 226, 115, 239, 252, 215, 46, 171, 204, 136, 127, 167,
                92, 162, 244, 107, 99, 64, 135, 132, 159, 151, 71, 112, 68,
                159, 56, 215, 24, 61, 204, 188, 123, 125, 75, 56, 228, 234]
        self.assertEqual(expected, expand_key(key))

        key = "OneTwoThreeFour!"
        expected = [79, 110, 101, 84, 119, 111, 84, 104, 114, 101, 101, 70,
                111, 117, 114, 33, 211, 46, 152, 252, 164, 65, 204, 148, 214,
                36, 169, 210, 185, 81, 219, 243, 0, 151, 149, 170, 164, 214,
                89, 62, 114, 242, 240, 236, 203, 163, 43, 31, 14, 102, 85,
                181, 170, 176, 12, 139, 216, 66, 252, 103, 19, 225, 215, 120,
                254, 104, 233, 200, 84, 216, 229, 67, 140, 154, 25, 36, 159,
                123, 206, 92, 207, 227, 163, 19, 155, 59, 70, 80, 23, 161, 95,
                116, 136, 218, 145, 40, 184, 98, 151, 215, 35, 89, 209, 135,
                52, 248, 142, 243, 188, 34, 31, 219, 107, 162, 46, 178, 72,
                251, 255, 53, 124, 3, 113, 198, 192, 33, 110, 29, 22, 61, 138,
                8, 94, 198, 117, 61, 34, 197, 4, 251, 226, 228, 106, 230, 100,
                63, 4, 144, 58, 249, 113, 173, 24, 60, 117, 86, 250, 216, 31,
                176, 51, 255, 227, 189, 9, 6, 146, 16, 17, 58, 231, 70, 235,
                226, 248, 246]
        self.assertEqual(expected, expand_key(key))

    def test_shift_rows(self):
        state = [[215, 99, 175, 64], [35, 18, 241, 164],
                [38, 110, 38, 18], [80, 143, 54, 229]]
        expected = [[215, 99, 175, 64], [18, 241, 164, 35],
                [38, 18, 38, 110], [229, 80, 143, 54]]
        aesmat = AES_Matrix(state)
        aesmat.shift_rows()
        self.assertEqual(aesmat.state, expected)
        aesmat.inv_shift_rows()
        self.assertEqual(aesmat.state, state)

    def test_mix_columns(self):
        state = [[215, 99, 175, 64], [18, 241, 164, 35],
                [38, 18, 38, 110], [229, 80, 143, 54]]
        expected = [[64, 140, 27, 189], [124, 252, 25, 130],
                [189, 70, 205, 229], [135, 230, 109, 225]]
        aesmat = AES_Matrix(state)
        aesmat.mix_columns()
        self.assertEqual(aesmat.state, expected)
        aesmat.inv_mix_columns()
        self.assertEqual(aesmat.state, state)

        state = [[11, 231, 231, 4], [1, 202, 79, 97],
                [45, 243, 19, 121], [93, 142, 84, 51]]
        expected = [[101, 237, 67, 225], [35, 232, 24, 126],
                [183, 89, 114, 194], [139, 12, 198, 114]]
        aesmat = AES_Matrix(state)
        aesmat.mix_columns()
        self.assertEqual(aesmat.state, expected)
        aesmat.inv_mix_columns()
        self.assertEqual(aesmat.state, state)


    def test_sub_bytes(self):
        state = [[13, 0, 27, 114], [50, 57, 43, 29],
                [35, 69, 35, 57], [108, 115, 36, 42]]
        expected = [[215, 99, 175, 64], [35, 18, 241, 164],
                [38, 110, 38, 18], [80, 143, 54, 229]]
        aesmat = AES_Matrix(state)
        aesmat.sub_bytes()
        self.assertEqual(aesmat.state, expected)
        aesmat.inv_sub_bytes()
        self.assertEqual(aesmat.state, state)

# -------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main()
