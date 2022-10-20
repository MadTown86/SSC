import unittest
import unittest.mock
from unittest.mock import patch
import parsessc

import dotenv
import os
dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')

class MyTestCase(unittest.TestCase):
    storpath = ROOT_VAR_SSC + "test_fetchlog.txt"

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

        ticker_fail = "MSFT__url_balance"

        P = parsessc.ParseStart()
        P.ssc_parselogstart(ticker_fail)
        MockFetchS.assert_called()
        print(MockFetchS.call_count)
        MockFetchL.assert_called()
        print(MockFetchL.call_count)
        MockParseBal.assert_called()
        print(MockParseBal.call_count)
        MockParseInc.assert_called()
        print(MockParseInc.call_count)
        MockParseAr.assert_called()
        print(MockParseAr.call_count)
        MockParseVal.assert_called()
        print(MockParseVal.call_count)
        MockParseSec.assert_called()
        print(MockParseSec.call_count)
        MockParseInd.assert_called()
        print(MockParseInd.call_count)


if __name__ == '__main__':
    unittest.main()
