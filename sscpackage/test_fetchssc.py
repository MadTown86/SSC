import unittest
import sscpackage.fetchssc
from unittest.mock import patch
from unittest.mock import MagicMock
from unittest.mock import AsyncMock
import asyncio


class Test_FetchCyclerTest_Asyncio(unittest.IsolatedAsyncioTestCase):

    """
    This class tests FetchCycler using unittest.IsolatedAsyncioTestCase and Mock
    """

    @patch('sscpackage.fetchurlssc.FetchUrlSSC')
    @patch('requests.request')
    @patch('sscpackage.fetchshelfssc_mod.FetchShelfSSC')
    async def test_fetchcycler(self, MockFetchStore, mock_request, MockFetchUrl):
        # Mock requests.request setup
        mockrequest = mock_request()
        stcode = unittest.mock.PropertyMock(return_value=200)
        jsonmock = unittest.mock.PropertyMock(return_value='{"JSONDICT": {"URL": "value1", "qd": "value2"}}')
        type(mockrequest).status_code = stcode
        type(mockrequest).text = jsonmock

        # FetchUrlShelfRequest Setup mock
        mockfetchvar = MockFetchUrl()
        fetchshelf = unittest.mock.MagicMock(return_value={"url_income": {"url": "url1", "qs": "qs1", "headers": "headers1"},
                                                           "url_balance": {"url": "url2", "qs": "qs2", "headers": "headers2"},
                                                           "url_ar": {"url": "url3", "qs": "qs_ar3", "headers": "headers_ar3"},
                                                           "url_val": {"url": "url_val4", "qs": "qs_val4", "headers": "headers4"},
                                                           "url_sectordata": {"url": "url_sectordata", "qs": "qs_sector", "headers": "headers"}})

        type(mockfetchvar).pullfetchshelf = fetchshelf

        mockfetchstorevar = MockFetchStore()
        mockfetchstorecall = unittest.mock.MagicMock(return_value="stored data")
        type(mockfetchstorevar).fetchstore = mockfetchstorecall

        FC1T = sscpackage.fetchssc.FetchSSC("MSFT")
        await FC1T.rapid_fetch()


if __name__ == '__main__':
    unittest.main()
