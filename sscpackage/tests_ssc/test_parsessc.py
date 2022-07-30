import unittest
import unittest.mock
from unittest.mock import patch

import parsessc


class MyTestCase(unittest.TestCase):
    storpath = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\test_fetchlog.txt'
    def setUp(self):

        with open(self.storpath, 'w') as sfile:
            sfile.truncate()
            sfile.close()

        primedata_testlogfetch = ''
        with open(self.storpath, 'w') as sfile:
            primedata_testlogfetch += "MSFT__url_income__2510381479104__x1jU288DK5DRjWf, " \
                                     "MSFT__url_balance__2510381479104__x1jU288DK5DRjWf, " \
                                     "MSFT__url_ar__2510381479104__x1jU288DK5DRjWf, " \
                                     "MSFT__url_val__2510381479104__x1jU288DK5DRjWf, " \
                                     "MSFT__url_sectordata__2510381479104__x1jU288DK5DRjWf,"
            sfile.write(primedata_testlogfetch)
            sfile.close()

    @patch("parsearssc.ParseAr")
    @patch("parsebalancessc.ParseBalance")
    @patch("parseincomessc.ParseIncome")
    @patch("parsevalssc.ParseVal")
    @patch("parseindssc.ParseIndustry")
    @patch("parsesectorssc.ParseSector")
    @patch("fetchlogssc.FetchLogSSC")
    @patch("fetchshelfssc_mod.FetchShelfSSC")
    def test_parsessc(self, MockFetchS, MockFetchL, MockParseSec, MockParseInd, MockParseVal, MockParseInc,
                      MockParseBal, MockParseAr):
        with open(self.storpath, 'r') as datassc:
            primedatatestlogfetchmock = datassc.read().split(", ")

        type(MockFetchS()).fetchdbpull = unittest.mock.MagicMock(return_value=unittest.mock.MagicMock())
        type(MockFetchL()).ssc_logfetch = unittest.mock.MagicMock(return_value=primedatatestlogfetchmock)
        type(MockParseSec()).parsesector = unittest.mock.MagicMock(return_value="Sector")
        type(MockParseInd()).parseindustry = unittest.mock.MagicMock(return_value="Industry")
        type(MockParseVal()).parseval = unittest.mock.MagicMock(return_value="ParseVal")
        type(MockParseInc()).parseincome = unittest.mock.MagicMock(return_value="ParseInc")
        type(MockParseBal()).parsebalance = unittest.mock.MagicMock(return_value="ParseBal")
        type(MockParseAr()).parsear = unittest.mock.MagicMock(return_value="ParseAr")

        P = parsessc.ParseStart()
        P.ssc_parselogstart()
        MockFetchS.assert_called()
        MockFetchL.assert_called()
        MockParseBal.assert_called()
        MockParseInc.assert_called()
        MockParseAr.assert_called()
        MockParseVal.assert_called()
        MockParseSec.assert_called()
        MockParseInd.assert_called()


if __name__ == '__main__':
    unittest.main()
