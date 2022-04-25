import asyncio

import simplestockchecker_fetchtool
import unittest
from unittest.mock import Mock
from unittest.mock import patch



class Tester1(unittest.IsolatedAsyncioTestCase):

    # @patch('simplestockchecker_fetchtool.FetchUrlRequestShelfSSC')
    @patch('requests.request')
    # @patch('simplestockchecker_fetchtool.FetchDataStoreSSC')
    async def test_fetchcycler(self, mock_request): #MockFetchStore, mock_request, MockFetchUrl
        m = mock_request()
        stcode = unittest.mock.PropertyMock(return_value=200)
        jsonmock = unittest.mock.PropertyMock(return_value={"JSONDICT": {"URL": "value1", "qd": "value2"}})
        type(m).status_code = stcode
        type(m).text = jsonmock

        #mock_request.return_value = Mock(status_code=200, response={"data_get": {"id": "test"}})
        #MFURLSHELF = MockFetchUrl()
        #MFS = MockFetchStore()
        #MFS.fetchstore.return_value = "Data Stored"
        #MFURLSHELF.pullfetchshelf.return_value = {"url_income": {"url": "url1", "qs": "qs1", "headers": "headers1"},
                                                  #"url_balance": {"url": "url2", "qs": "qs2", "headers": "headers2"},
                                                  #"url_ar": {"url": "url3", "qs": "qs_ar3", "headers": "headers_ar3"},
                                                  #"url_val": {"url": "url_val4", "qs": "qs_val4", "headers": "headers4"},
                                                  #"url_sectordata": {"url": "url_sectordata", "qs": "qs_sector", "headers": "headers"}}

        FC1T = simplestockchecker_fetchtool.FetchCyclerSSC("MSFT")
        loop = asyncio.get_event_loop()
        await FC1T.rapid_fetch({"TESTDICT": "MOCKERY"})
        #print(MFURLSHELF.pullfetchshelf())
        #await FC1T.rapid_fetch(MFURLSHELF.pullfetchshelf())
        #mock_request.assert_called()
        #mock_request.assert_called_with("GET", "url_sectordata", "qs_sector", "headers")
        #MFURLSHELF.assert_called()


if __name__ == "__main__":
    unittest.main()