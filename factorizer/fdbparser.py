import re

import urllib.request as urlreq
from bs4 import BeautifulSoup
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

from util.error import FactorizationError, FactordbError

# Status returned by factordb.com
fdb_status = { "C": "Composite, no factors knwon",
        "CF": "Composite, factors known",
        "FF": "Composite, fully factored",
        "P": "Definitely prime",
        "Prp": "Probably prime",
        "U": "Unknown"}

_fdb_url = "http://factordb.com/"

_fdb_grammar = Grammar("""
        expr    = (power mult) / mult / power / factor
        parent  = "(" expr ")"
        pval    = parent / factor
        power   = pval "^" factor
        mval    = parent / power / factor
        mult    = mval "*" expr
        factor  = int junk*
        int     = ~"[0-9]+"
        junk    = ~"<[0-9]+>"
        """)

class FDBParser(NodeVisitor):
    """Parse the result obtained by factordb.com to extract all factors."""
    def __init__(self, text):
        self.factors = []
        self._tmp = []
        ast = _fdb_grammar.parse(text)
        res = self.visit(ast)
        self.factors = [int(v) for v in res]
    def visit_power(self, n, vc):
        nvc = []
        for i in range(int(vc[2][0])):
            nvc.extend(vc[0])
        return nvc
    def visit_mult(self, n, vc):
        vc[0].extend(vc[2])
        return vc[0]
    def visit_int(self, n, vc):
        return [n.text]
    def visit_factor(self, n, vc):
        return vc[0]
    def visit_digit(self, n, vc):
        return [n.text]
    def visit_parent(self, n, vc):
        return vc[1]
    def visit_mval(self, n, vc):
        return vc[0]
    def visit_pval(self, n, vc):
        return vc[0]
    def visit_expr(self, n, vc):
        return vc[0]
    def generic_visit(self, n, vc):
        pass

def get_factors(n):
    try:
        url = _fdb_url + "index.php?query=" + str(n)
        res = urlreq.urlopen(url)
    except IOError as err:
        # Handle Internet connectivity issues
        raise FactordbError("Unable to access %s" % url)
    if res.getcode() != 200:
        # Handle specific connectivity to factordb.com issues
        raise FactordbError("HTTP request returns with status code %d" % res.getcode())
    soup = BeautifulSoup(res.read(), "html.parser")
    if soup.find(text=re.compile("^Error:*")):
        # Handle unsupported values by factordb.com
        raise FactordbError("Value %d unsupported by factordb.com" % n)
    tr = soup.find_all("tr")[3]
    status = tr.contents[0].get_text().replace('*', '').strip()
    if status in ["FF", "CF"]:
        ftxt = _handle_number(tr)
        if status == "CF":
            raise FactorizationError("Factorization is incomplete")
        return FDBParser(ftxt).factors
    elif status in ["P", "Prp"]:
        return [1, n]
    else:
        raise FactorizationError("No factorization found")

def _handle_number(txt):
    """Handle number in returned by factordb.com.
    Large prime numbers of the form 111...11 are handled by accessing
    the 'href' link in the <a> tag.
    """
    ftxt = str(txt)
    ftxt = txt.contents[4].get_text().partition(" = ")[-1]
    ftxt = ftxt.replace(u" \u00b7 ", "*")
    td = txt.find_all("td")[-1]
    for a in td.find_all("a")[1:]:
        if "..." in a.get_text():
            # Handle large number
            url = _fdb_url + a.get("href").replace("?id=", "?showid=")
            res = urlreq.urlopen(url)
            soup = BeautifulSoup(res.read(), "html.parser")
            n = soup.find_all("td")[-1].get_text()
            n = n.replace("\n", "")
            ftxt = ftxt.replace(a.get_text(), n)
    return ftxt
