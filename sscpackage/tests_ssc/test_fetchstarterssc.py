import unittest
from unittest.mock import patch
import sscpackage.fetchstarterssc


class Test_FetchStarterFinal(unittest.IsolatedAsyncioTestCase):

    @patch('sscpackage.fetchssc.FetchSSC')
    async def test_fetchstarter(self, MockFetchCycler):

        mock_fetchcyclerclassvar = MockFetchCycler()
        mock_returntest = unittest.mock.AsyncMock(auto_spec=sscpackage.fetchssc.FetchSSC())
        mock_fetchcyclervar = unittest.mock.AsyncMock(return_value=mock_returntest)

        type(mock_fetchcyclerclassvar).rapid_fetch = mock_fetchcyclervar
        test_tickerlist = "MSFT, AMD, NVDA, TSLA, ORCL, AAPL, NVDA, GME, GE, FORD"
        FSF1 = sscpackage.fetchstarterssc.FetchStarterSSC(test_tickerlist)
        await FSF1.fetch_cycle()
        self.assertEqual(2, len(MockFetchCycler.mock_calls), "Missmatch")


if __name__ == '__main__':
    unittest.main()
