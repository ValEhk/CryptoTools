#!/usr/bin/env python3

from unittest import TestCase

from legacy.substitute import rot, xor

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
        self.assertEqual(plain, xor(plain, 0))
        self.assertEqual(plain, xor(xor(plain, 25), 25))
        self.assertEqual(plain, xor(xor(plain, 99), 99))
        plain = b"Hello World!"
        self.assertEqual(plain, xor(plain, 0))
        self.assertEqual(plain, xor(xor(plain, 16), 16))
        self.assertEqual(plain, xor(xor(plain, 200), 200))


# -------------------------------------------------------------------------- #

# class TestVigenere(TestCase):

# -------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main()
