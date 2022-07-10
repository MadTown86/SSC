import unittest
import parsearssc
import shelve

import parsessc


class MyTestCase(unittest.TestCase):
    def test_parsear(self):
        test_parseardatapath = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\test_parse_ar.json'
        test_parsearuniquename = "TESTticker__TESTkey__TESTidssc__TESTtimestampidar"
        PARSSC = parsearssc.ParseAr()
        with open(test_parseardatapath) as testdoc:
            test_value = PARSSC.parsear(test_parsearuniquename, testdoc.read())
            print(test_value)
            testdoc.close()

        with shelve.open(PARSSC.setpathssc_parsesscar) as parshelv:
            keylist = [key for key in parshelv.keys()]
            if test_parsearuniquename in keylist:
                testvalone = True
                del parshelv[test_parsearuniquename]
            else:
                testvalone = False

        self.assertTrue(testvalone)
        del PARSSC

    def test_fetchparsear(self):

        PARSSC = parsearssc.ParseAr()
        with shelve.open(PARSSC.setpathssc_parsesscar) as parshelv:
            for key in parshelv.keys():
                del parshelv[key]
            parshelv.close()

        test_parseardatapath = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\test_parse_ar.json'
        test_parsearuniquename = "TESTticker__TESTkey__TESTidssc__TESTtimestampidar"
        test_parsetimestampid = "TESTtimestampidar"

        testvalone = PARSSC.fetch_parsear(test_parsetimestampid)

        self.assertEqual(testvalone, None)

        with open(test_parseardatapath) as fd:
            PARSSC.parsear(test_parsearuniquename, fd.read())
            fd.close()

        testvaluetwoar = PARSSC.fetch_parsear(test_parsetimestampid)[0]['action']
        correctvaluetwoar = "main"
        self.assertEqual(testvaluetwoar, correctvaluetwoar)




if __name__ == '__main__':
    unittest.main()
