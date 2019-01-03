#!/usr/bin/env python3

import binascii
from unittest import TestCase

from dlp.dlp import discrete_log

class TestDLP(TestCase):
    def test_simple(self):
        g = 2862392356922936880157505726961027620297475166595443090826668842052108260396755078180089295033677131286733784955854335672518017968622162153227778875458650593
        h = 6289736695712027841545587266292164172813699099085672937550442102159309081155467550411414088175729823598108452032137447608687929628597035278365152781494883808
        n = 7863166752583943287208453249445887802885958578827520225154826621191353388988908983484279021978114049838254701703424499688950361788140197906625796305008451719
        expected = 5984395521967467346233654974364351165422250974773836380349996370549071399526484130546437803585190342858690941215911884205493540794098544612334027224908987632
        self.assertEqual(discrete_log(g, h, n), expected)

# -------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main()