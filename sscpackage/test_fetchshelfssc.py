import shelve

import unittest
from unittest.mock import Mock
from unittest.mock import patch
from sscpackage.fetchshelfssc_mod import FetchShelfSSC


class Test_FetchShelfSSC(unittest.TestCase):
    @patch('shelve.open')
    def test_fetchshelfsscmock(self, ShelveMock):
        MockShelveVar = ShelveMock(spec_set=shelve.open) # MagicMock Class Instance, takes the place for 'shelve'
        starterdict_mock = {}
        mock_shelvemethod = unittest.mock.MagicMock(return_value=starterdict_mock)
        MockShelveVar.open = mock_shelvemethod
        with patch.dict(starterdict_mock, {}, clear=True) as fetchpatchedshelf:
            FS1 = FetchShelfSSC()
            fetchstorenamefromFS1 = FS1.fetchstore()
        self.assertEqual("MSFT__url_income__DEFAULTID", fetchstorenamefromFS1, "First")
        self.assertTrue(ShelveMock.called)
        ShelveMock.assert_called_with("fetchfiledb")







if __name__ == '__main__':
    unittest.main()
