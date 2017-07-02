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

    # TODO complete tests
    def test_matrix_multiply(self):
        pass

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
