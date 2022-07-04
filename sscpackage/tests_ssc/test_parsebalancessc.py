import unittest
import parsebalancessc
import shelfpeekssc
import shelve


class MyTestCase(unittest.TestCase):

    def test_parsebalancesssc(self):
        PBSSC_test = parsebalancessc.ParseBalance()
        SPEEK_SSC = shelfpeekssc.FetchPeekSSC()
        namevar = "test__test2__test3__test4"
        pbalancepath = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parsebalanceshelf'
        testval1 = str(('2021-06-30', '2020-06-30', '2019-06-30', '2018-06-30'))

        if not SPEEK_SSC.fetchpeek(path=pbalancepath, keysearch=namevar):
            with open(r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\test_parse_balance.json', 'r') as fd:
                PBSSC_test.parsebalance(namevar, fd.read())
        else:
            pass

        resval1 = ''
        with shelve.open(pbalancepath) as sv:
            resval1 += str(sv[namevar]['Date'])
            sv.close()

        self.assertEqual(testval1, resval1)


if __name__ == '__main__':
    unittest.main()
