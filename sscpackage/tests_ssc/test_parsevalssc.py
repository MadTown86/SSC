import unittest
import parsevalssc
import json


class MyTestCase(unittest.TestCase):
    def test_parseval(self):
        PSVAL = parsevalssc.ParseVal()
        test_datapathparsevalssc = r'C:\SSC\SimpleStockchecker_Rev1\sscpackage\storage\test_parse_val.json'
        test_dataparsevalresult1 = r'C:\SSC\SimpleStockchecker_Rev1\sscpackage\storage\test_parsevaltestresult.json'
        test_parsevaluniquename = "Testticker__Testkey__Testidssc__Testtimestampidval"

        with open(test_datapathparsevalssc, 'r') as pvssctest:
            parsevaldata = json.loads(pvssctest.read())
            pvssctest.close()

        PSVAL.parseval(test_parsevaluniquename, parsevaldata)

        with open(test_dataparsevalresult1, 'r') as pvsscrestst:
            parseresultdata = json.loads(pvsscrestst.read())
            pvsscrestst.close()

        parsevalresultshelf = PSVAL.fetchparseval(test_parsevaluniquename)

        self.assertEqual(parsevalresultshelf, parseresultdata)  # add assertion here


if __name__ == '__main__':
    unittest.main()
