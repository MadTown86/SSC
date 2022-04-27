import asyncio

import simplestockchecker_fetchtool
import unittest
from unittest.mock import Mock
from unittest.mock import patch



class FetchCyclerTest_Asyncio(unittest.IsolatedAsyncioTestCase):

    """
    This class tests FetchCycler using unittest.IsolatedAsyncioTestCase and Mock
    """

    @patch('simplestockchecker_fetchtool.FetchUrlRequestShelfSSC')
    @patch('requests.request')
    @patch('simplestockchecker_fetchtool.FetchDataStoreSSC')
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

        FC1T = simplestockchecker_fetchtool.FetchCyclerSSC("MSFT")
        await FC1T.rapid_fetch()


if __name__ == "__main__":
    unittest.main()