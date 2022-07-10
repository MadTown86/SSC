import unittest
import shelve
import parseincomessc
import shelfpeekssc


class MyTestCase(unittest.TestCase):
    def test_parseincomessc(self):
        PISSC_test = parseincomessc.ParseIncome()
        SPEEK_SSC = shelfpeekssc.FetchPeekSSC()
        namevar = "test__test2__test3__test4"
        pincomepath = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parseincomeshelf'
        testval1 = str(('2021-06-30', '2020-06-30', '2019-06-30', '2018-06-30'))

        if not SPEEK_SSC.fetchpeek(path=pincomepath, keysearch=namevar):
            with open(r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\test_parse_income.json', 'r') as fd:
                PISSC_test.parseincome(namevar, fd.read())
                fd.close()
        else:
            pass

        resval1 = ''
        with shelve.open(pincomepath) as sv:
            resval1 += str(sv[namevar]['Date'])
            sv.close()

        self.assertEqual(testval1, resval1)


if __name__ == '__main__':
    unittest.main()
