import unittest
from unittest.mock import patch
import sscpackage.parsebalancessc
import sscpackage.fetchshelfssc_mod
import sscpackage.dictpullssc
import sscpackage.fetchssc
import sscpackage.parsebalancessc_sub


class TestParseMock_Sub(unittest.TestCase):


    @patch("dictpullssc.DictPullSSC")
    @patch('fetchssc.FetchSSC')
    @patch('fetchshelfssc_mod.FetchShelfSSC')
    def test_parsebalance_tickefailflag(self, Mock_FetchShelfSSC, Mock_FetchSSC, Mock_DictPullSSC):
        test_passin = {"balanceSheetStatement": ["test_failticker"]}

        type(Mock_FetchShelfSSC()).fetchstore = unittest.mock.MagicMock()
        type(Mock_FetchSSC()).ticker_fail = unittest.mock.MagicMock()
        type(Mock_DictPullSSC()).dictpullssc(return_value=test_passin)

        test_fetchnamepassin = "TEST__TEST__TEST__TEST"
        passin_empty = {}

        PSB = sscpackage.parsebalancessc_sub.ParseBalance_Sub()

        PSB.parsebalance(test_fetchnamepassin, passin_empty)


        Mock_FetchSSC.calls()

        Mock_FetchSSC.assert_called_with(test_fetchnamepassin)


if __name__ == '__main__':
    unittest.main()
