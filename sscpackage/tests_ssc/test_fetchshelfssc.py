import shelve
import unittest
from unittest.mock import Mock
from unittest.mock import patch


import sscpackage
from sscpackage.fetchshelfssc_mod import FetchShelfSSC


class Test_FetchShelfSSC(unittest.TestCase):
    @patch('shelve.open')
    def test_fetchshelfsscmock(self, ShelveMock):
        MockShelveVar = ShelveMock(spec_set=shelve.open) # MagicMock Class Instance, takes the place for 'shelve'
        starterdict_mock = {}
        with patch.dict(starterdict_mock, {"TEST1": "VAlTEST1"}, clear=True) as fetchpatchedshelf:
            print(fetchpatchedshelf)
            mock_shelvemethod = unittest.mock.MagicMock(return_value=fetchpatchedshelf)
            MockShelveVar.open = mock_shelvemethod
            FS1 = FetchShelfSSC()
            fetchstorenamefromFS1 = FS1.fetchstore()
        self.assertEqual("MSFT__url_income__DEFAULTID__DEFTSID", fetchstorenamefromFS1, "First")
        self.assertTrue(ShelveMock.called)
        ShelveMock.assert_called_with(r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\fetchfiledb')

    @patch('shelve.open')
    def test_fetchdbpullssc(self, MockShelve):
        mockershelvemethod = unittest.mock.MagicMock()
        MockerShelve = MockShelve(return_value=mockershelvemethod)


        FS1 = sscpackage.fetchshelfssc_mod.FetchShelfSSC()
        FS1.fetchdbpull()

        MockShelve.assert_called_with(r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\fetchfiledb')

if __name__ == '__main__':
    unittest.main()
