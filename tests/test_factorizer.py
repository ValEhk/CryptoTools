#!/usr/bin/env python3

from unittest import TestCase

from factorizer.factorizer import *
from util.error import UnitWarning, FactorizationError, FactordbError

class TestGen(TestCase):
    def setUp(self):
        self.f = Factorizer()

    def test_one(self):
        with self.assertWarns(UnitWarning):
            self.f.factorize(1)

    def test_prime(self):
        self.assertEqual(self.f.factorize(11), [1, 11])
        self.assertEqual(self.f.factorize(12334567643456787654589), [1, 12334567643456787654589])
        self.assertEqual(self.f.factorize(1554394760620636982437498555986798873241611344431896131572608284673300517), \
                [1, 1554394760620636982437498555986798873241611344431896131572608284673300517])

# -------------------------------------------------------------------------- #

class TestFactordb(TestCase):
    def setUp(self):
        self.f = Factorizer(Algo.FACTORDB)

    def test_power(self):
        self.assertEqual(self.f.factorize(25), [5, 5])
        self.assertEqual(self.f.factorize(11250), [2, 3, 3, 5, 5, 5, 5])

    def test_arbit(self):
        self.assertEqual(self.f.factorize(2787), [3, 929])
        self.assertEqual(self.f.factorize(777772727772272727), [3, 11, 9371,  2515085960789])
        self.assertEqual(self.f.factorize(572647860209), [857, 883, 756739])
        self.assertEqual(self.f.factorize(2406937264475073), [3, 11, 29,  2515085960789])
        self.assertEqual(self.f.factorize(40054869679012345679012345679012345679012345679012345679012345679012345679012345679012345679),\
                [8534419, 3019395743473, 1554394760620636982437498555986798873241611344431896131572608284673300517])

    def test_error(self):
        with self.assertRaises(FactordbError):
            self.f.factorize(-12)
            self.f.factorize(0)

# -------------------------------------------------------------------------- #

class TestSmallPrimes(TestCase):
    def setUp(self):
        self.f = Factorizer(Algo.SMALL_PRIMES, 100)

    def test_arbit(self):
        self.assertEqual(self.f.factorize(2787), [3, 929])
        self.assertEqual(self.f.factorize(2809), [53, 53])

    def test_recurs(self):
        self.assertEqual(self.f.factorize(2406937264475073), [3, 11, 29,  2515085960789])
        self.assertEqual(self.f.factorize(10210200), [2, 2, 2, 3, 5, 5, 7, 11, 13, 17])

    def test_limit(self):
        self.f.limit = 4
        with self.assertRaises(FactorizationError):
            self.f.factorize(121)
        self.assertEqual(self.f.factorize(119), [7, 17])
        self.f.limit = 10
        self.assertEqual(self.f.factorize(121), [11, 11])
        self.assertEqual(self.f.factorize(119), [7, 17])

# -------------------------------------------------------------------------- #

class TestFermat(TestCase):
    def setUp(self):
        self.f = Factorizer(Algo.FERMAT, 100)

    def test_arbit(self):
        self.assertEqual(self.f.factorize(2809), [53, 53])
        self.assertEqual(self.f.factorize(756731), [857, 883])

    def test_recurs(self):
        self.assertEqual(self.f.factorize(35717), [11, 17, 191])
        self.assertEqual(self.f.factorize(572647860209), [857, 883, 756739])

    def test_limit(self):
        self.assertEqual(self.f.factorize(187), [11, 17])
        with self.assertRaises(FactorizationError):
            self.f.factorize(2787)
        self.f.limit = 1000
        self.assertEqual(self.f.factorize(121), [11, 11])
        self.assertEqual(self.f.factorize(2787), [3, 929])

    def test_sexyrsa(self):
        n = 1209143407476550975641959824312993703149920344437422193042293131572745298662696284279928622412441255652391493241414170537319784298367821654726781089600780498369402167443363862621886943970468819656731959468058528787895569936536904387979815183897568006750131879851263753496120098205966442010445601534305483783759226510120860633770814540166419495817666312474484061885435295870436055727722073738662516644186716532891328742452198364825809508602208516407566578212780807
        p = 1099610570827941329700237866432657027914359798062896153406865588143725813368448278118977438921370935678732434831141304899886705498243884638860011461262640420256594271701812607875254999146529955445651530660964259381322198377196122393
        q = 1099610570827941329700237866432657027914359798062896153406865588143725813368448278118977438921370935678732434831141304899886705498243884638860011461262640420256594271701812607875254999146529955445651530660964259381322198377196122399
        self.assertEqual(self.f.factorize(n), [p, q])

# -------------------------------------------------------------------------- #

class TestMersenne(TestCase):
    def setUp(self):
        self.f = Factorizer(Algo.MERSENNE)

    def test_arbit(self):
        self.assertEqual(self.f.factorize(155), [5, 31])
        self.assertEqual(self.f.factorize(315), [3, 3, 5, 7])
        n = ((2**2203)-1)*((2**2281)-1)
        expected = [(2**2203)-1, (2**2281)-1]
        self.assertEqual(self.f.factorize(n), expected)

    def test_warning(self):
        with self.assertRaises(FactorizationError):
            self.f.factorize(28)
        with self.assertRaises(FactorizationError):
            self.f.factorize(3844)

# -------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main()
