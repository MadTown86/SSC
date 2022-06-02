import unittest
from unittest.mock import patch

import sscpackage.storessc
from sscpackage import storessc
from sscpackage.storessc import StoreSSC
from simplestockchecker_parsetool import GradeSSC


class Test_StoreSSC(unittest.TestCase):
    def test_chksetup(self):
        S1 = storessc.StoreSSC()
        self.assertTrue(S1.db_chksetup())
    @patch('mysql.connector.connect')
    @patch('json.dumps')
    def test_logentry(self, mock_parse, mock_methodvar):
        mocknest_parse = mock_parse(side_effect=lambda: unittest.mock.MagicMock())
        mocknest_parsemethod = unittest.mock.MagicMock(return_value="dumpmock")
        type(mocknest_parse).dumps = unittest.mock.MagicMock(return_value=mocknest_parsemethod)



        mvarreturn = unittest.mock.MagicMock()
        mmvar = mock_methodvar(return_value=mvarreturn)
        mmvar.execute = unittest.mock.MagicMock()
        mmvar.commit = unittest.mock.MagicMock()
        type(mmvar).execute = unittest.mock.MagicMock()

        STest = storessc.StoreSSC()
        STest.log_entry()

if __name__ == '__main__':
    unittest.main()
