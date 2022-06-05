import unittest
from unittest.mock import patch
import os

import sscpackage.storessc

def miniprinter(header, obj):
    res = ''
    end = '\n'
    for val in obj:
        res += header + " :::: " + str(val) + end
    return res + end


class Test_StoreSSC(unittest.TestCase):
    def test_chksetup(self):
        """
        This tests to make sure a table exists before commits are mde
        :return: True / creates table / throws error if no server exists in which to create a table
        """
        S1 = sscpackage.storessc.StoreSSC()
        self.assertTrue(S1.db_chksetup())

    @patch('sscpackage.storessc.mysql.connector')
    @patch('sscpackage.storessc.json')
    @patch('sscpackage.storessc.sscp.GradeSSC')
    def test_logentry(self, mock_parse, mock_json, mock_methodvar):
        """
        :param mock_parse:
        :param mock_json:
        :param mock_methodvar:
        :return:
        """
        SC = sscpackage.storessc.StoreSSC()
        SC.log_entry()

        mock_json.dumps.assert_called()
        mock_methodvar.connect.assert_called()
        connect_calls = [unittest.mock.call.connect(host='localhost', user=str(os.getenv("DB_USER")),
                        password=str(os.getenv("DB_PASS")), database='sscdb')]
        self.assertEqual(connect_calls, mock_methodvar.method_calls)

        assert mock_parse is sscpackage.storessc.sscp.GradeSSC
        assert mock_json is sscpackage.storessc.json
        assert mock_methodvar is sscpackage.storessc.mysql.connector


    @patch('sscpackage.storessc.mysql.connector')
    @patch('sscpackage.storessc.mysql.connector.cursor')
    def test_showdb(self, mock_cursor, mock_connector):
        """

        :param mock_cursor:
        :param mock_connector:
        :return:
        """

        SC1 = sscpackage.storessc.StoreSSC()
        SC1.show_db()

        mock_connector.connect.return_value.__enter__.return_value.cursor.return_value.\
            __enter__.return_value.execute.assert_called_with('SELECT * FROM logentry')
    @patch('sscpackage.storessc.mysql.connector')
    @patch('sscpackage.storessc.pd')
    def test_export_excel(self, mock_pd, mock_connector_xls):
        """

        :param mock_connector_xls:
        :return:
        """
        connect_calls_xls = [unittest.mock.call.connect(host='localhost', user=str(os.getenv("DB_USER")),
                                                    password=str(os.getenv("DB_PASS")), database='sscdb')]

        SC2 = sscpackage.storessc.StoreSSC()
        SC2.export_excel()

        mock_pd.read_sql.return_value.to_excel.assert_called_with('SSC.xlsx', sheet_name='DATA', index=False)
        self.assertEqual(connect_calls_xls, mock_connector_xls.method_calls)

if __name__ == '__main__':
    unittest.main()
