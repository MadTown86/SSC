import unittest
import parsevalssc
import json
import shelve


class MyTestCase(unittest.TestCase):
    def test_parseval(self):
        PSVAL = parsevalssc.ParseVal()
        test_datapathparsevalssc = r'C:\SSC\SimpleStockchecker_Rev1\sscpackage\storage\test_parse_val.json'
        test_dataparsevalresult1 = r'C:\SSC\SimpleStockchecker_Rev1\sscpackage\storage\test_parsevaltestresult.json'
        test_parsevaluniquename = "Testticker1__Testkey1__Testidssc1__Testtimestampidval1"

        with shelve.open(PSVAL.setpathssc_parsesscval) as shelfclear:
            for key in shelfclear.keys():
                del shelfclear[key]
            shelfclear.close()

        with open(test_datapathparsevalssc, 'r') as pvssctest:
            parsevaldata = pvssctest.read()
            pvssctest.close()

        PSVAL.parseval(uniquename=test_parsevaluniquename, pval_rawdata=parsevaldata)

        with open(test_dataparsevalresult1, 'r') as pvsscrestst:
            parseresultdata = json.loads(pvsscrestst.read())
            pvsscrestst.close()

        parsevalresultshelf = PSVAL.fetchparseval(test_parsevaluniquename)
        print("IN TEST PARSE", parsevalresultshelf)

        self.assertEqual(parsevalresultshelf, parseresultdata)  # add assertion here

    def test_fetchparseval(self):
        test_parsevaluniquename = "Testticker1__Testkey1__Testidssc1__Testtimestampidval1"
        PPS = parsevalssc.ParseVal()
        if PPS.fetchparseval(test_parsevaluniquename) != 0:
            testres = True
        else:
            testres = False
        self.assertTrue(testres)

        with shelve.open(PPS.setpathssc_parsesscval) as pvssc:
            if test_parsevaluniquename in pvssc.keys():
                del pvssc[test_parsevaluniquename]
                pvssc.close()
            else:
                pvssc.close()

        self.assertEqual(0, PPS.fetchparseval(test_parsevaluniquename))

if __name__ == '__main__':
    unittest.main()
