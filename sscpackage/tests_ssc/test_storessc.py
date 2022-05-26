import unittest
from unittest.mock import patch
from sscpackage import storessc


class Test_StoreSSC(unittest.TestCase):
    def test_chksetup(self):
        S1 = storessc.StoreSSC()
        self.assertTrue(S1.db_chksetup())
    @patch.dict('insert_db_table')
    def test_logentry(self):



if __name__ == '__main__':
    unittest.main()
