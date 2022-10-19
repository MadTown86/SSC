import unittest
from unittest.mock import patch
import sscpackage.parsebalancessc
import sscpackage.fetchshelfssc_mod
import sscpackage.dictpullssc
import sscpackage.fetchssc
import sscpackage.parsebalancessc_sub
import test_helperfuncs_ssc as hpr


class TestParseMock_Sub(unittest.TestCase):
    test_passin = {"balanceSheetStatement": ["test_failticker"]}
    DoubleD_TheDilenschnazzle = unittest.mock.MagicMock(return_value=test_passin)
    mockfetchfailpassin = unittest.mock.MagicMock()

    @patch("dictpullssc.DictPullSSC.dictpullssc", DoubleD_TheDilenschnazzle)
    @patch("fetchssc.FetchSSC.ticker_fail", mockfetchfailpassin)
    @patch("fetchssc.FetchSSC")
    @patch("fetchshelfssc_mod.FetchShelfSSC")
    def test_parsebalance_tickefailflag(self, Mock_FetchShelfSSC, Mock_FetchSSC):

        type(Mock_FetchShelfSSC()).fetchstore = unittest.mock.MagicMock()

        test_fetchnamepassin = "TEST__TEST__TEST__TEST"
        passin_empty = {}

        PSB = sscpackage.parsebalancessc_sub.ParseBalance_Sub()

        PSB.parsebalance(test_fetchnamepassin, passin_empty)

        hpr.testmock_print(Mock_FetchShelfSSC, "MOCKFETCHSHELFSSC")
        hpr.testmock_print(Mock_FetchSSC, "MOCKfetch")
        hpr.testmock_print(TestParseMock_Sub.mockfetchfailpassin, "FETCH FAIL")
        hpr.testmock_print(
            TestParseMock_Sub.DoubleD_TheDilenschnazzle, "DOUBLE DEEEEEE"
        )

        print(test_fetchnamepassin)
        Mock_FetchSSC.return_value.ticker_fail.assert_called_with(
            fetchname="TEST__TEST__TEST__TEST"
        )




if __name__ == "__main__":
    unittest.main()
