#!/usr/bin/env python3

from unittest import TestCase

from AES import gf28
from util.error import GF28Error

class TestGF28(TestCase):
    def test_multiply(self):
        self.assertEqual(gf28.multiply(0, 13), 0)
        self.assertEqual(gf28.multiply(1, 5), 5)
        self.assertEqual(gf28.multiply(11, 10), 78)
        self.assertEqual(gf28.multiply(241, 3), 8)
        self.assertEqual(gf28.multiply(125, 424), 24)

    def test_matrix_multiply(self):
        """More tests for matrix_multiply are in tests/test_aes.py:
        AES_Matrix.mix_columns since the mix_columns() function is just a
        wrapper for the matrix_multiply function.
        """
        mat1 = [[0,1], [1,0]]
        self.assertEqual(gf28.matrix_multiply(mat1, mat1), [[1,0], [0,1]])
        with self.assertRaises(GF28Error):
            gf28.matrix_multiply([[0,0], [0,0]], [[0,1,2], [2,1,0]])
            gf28.matrix_multiply([[0,0], [0,0], [3,4]], [[0,1], [2,1], [5,0]])

    def test_invert(self):
        self.assertEqual(gf28.invert(0), 0)
        self.assertEqual(gf28.invert(1), 1)
        self.assertEqual(gf28.invert(20), 153)
        self.assertEqual(gf28.invert(233), 78)
        self.assertEqual(gf28.invert(113), 183)
        with self.assertRaises(GF28Error):
            gf28.invert(-12)
            gf28.invert(300)

    def test_mixed(self):
        self.assertEqual(gf28.multiply(gf28.invert(43), 43), 1)
        self.assertEqual(gf28.multiply(gf28.invert(78), 78), 1)
        self.assertEqual(gf28.multiply(gf28.invert(154), 154), 1)
