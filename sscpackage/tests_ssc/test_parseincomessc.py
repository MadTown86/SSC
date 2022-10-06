import shelve
import unittest

import parseincomessc
import shelverssc
import dotenv
import os
dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')

class MyTestCase(unittest.TestCase):
    def test_parseincomessc(self):
        PISSC_test = parseincomessc.ParseIncome()
        SPEEK_SSC = shelverssc.ShelverSSC()
        namevar = "test__test2__test3__test4"
        pincomepath = ROOT_VAR_SSC + 'parseincomeshelf'
        testval1 = str(('2021-06-30', '2020-06-30', '2019-06-30', '2018-06-30'))

        if not SPEEK_SSC.fetchpeek(path=pincomepath, keysearch=namevar):
            with open(ROOT_VAR_SSC + 'test_parse_income.json', 'r') as fd:
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
