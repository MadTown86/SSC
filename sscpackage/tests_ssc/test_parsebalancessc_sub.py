import unittest
from unittest.mock import patch
import sscpackage.parsebalancessc
import sscpackage.fetchshelfssc_mod
import sscpackage.dictpullssc
import sscpackage.fetchssc
import sscpackage.parsebalancessc_sub


class TestParseMock_Sub(unittest.TestCase):
    test_passin = {"balanceSheetStatement": ["test_failticker"]}

    @patch("sscpackage.dictpullssc.DictPullSSC.dictpullssc", unittest.mock.MagicMock(return_value=test_passin))
    @patch('sscpackage.fetchssc.FetchSSC')
    @patch('sscpackage.fetchshelfssc_mod.FetchShelfSSC')
    def test_parsebalance_tickefailflag(self, mock_fetchshelf, mock_fetchssc):
        def sideeffect2(arg):
            return arg

        test_fetchnamepassin = "TEST__TEST__TEST__TEST"
        passin_empty = {}

        PSB = sscpackage.parsebalancessc_sub.ParseBalance_Sub()

        PSB.parsebalance(test_fetchnamepassin, passin_empty)

        assert mock_fetchssc.called_with()


if __name__ == '__main__':
    unittest.main()
