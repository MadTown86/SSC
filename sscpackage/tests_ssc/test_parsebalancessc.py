import shelve
import unittest
import parsebalancessc
import shelverssc

import dotenv
import os
dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')

class MyTestCase(unittest.TestCase):
    # TODO: Update test_parsebalancessc so it actually tests the damn thing
    def test_parsebalancesssc(self):
        PBSSC_test = parsebalancessc.ParseBalance()
        namevar = "test__test2__test3__test4"
        SPEEK_SSC = shelverssc.ShelverSSC(namevar)
        pbalancepath = ROOT_VAR_SSC + 'parsebalanceshelf'
        testval1 = str(('2021-06-30', '2020-06-30', '2019-06-30', '2018-06-30'))

        if not SPEEK_SSC.fetchpeek(path=pbalancepath, keysearch=namevar):
            with open(ROOT_VAR_SSC + 'test_parse_balance.json', 'r') as fd:
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
