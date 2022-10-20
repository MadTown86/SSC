import os
import unittest
from unittest.mock import patch
import sscpackage


def miniprinter(header, obj):
    res = ''
    end = '\n'
    for val in obj:
        res += header + " :::: " + str(val) + end
    return res + end


class Test_StoreSSC(unittest.TestCase):

    @patch('sscpackage.storessc.mysql.connector')
    def test_chksetup(self, mock_connector):
        """
        This tests to make sure a table exists before commits are mde
        :return: True / creates table / throws error if no server exists in which to create a table
        """

        S1 = sscpackage.storessc.StoreSSC()
        called_withblock = """
                CREATE DATABASE IF NOT EXISTS sscdb;
                USE sscdb;
                CREATE TABLE IF NOT EXISTS logentry (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    ticker VARCHAR(5),
                    logTime DATETIME DEFAULT CURRENT_TIMESTAMP,
                    grade VARCHAR(2),
                    parsecombo JSON,
                    points INT,
                    basepoints INT
                );"""

        for value in mock_connector.method_calls:
            print(value)

        for value in mock_connector.connect.method_calls:
            print(value)

        for value in mock_connector.cursor.method_calls:
            print(value)

        self.assertTrue(S1.db_chksetup())

    @patch('sscpackage.storessc.mysql.connector')
    @patch('sscpackage.storessc.json')
    def test_logentry(self, mock_json, mock_methodvar):
        """
        :param mock_parse:
        :param mock_json:
        :param mock_methodvar:
        :return:
        """
        ticker_entry = unittest.mock.MagicMock()
        grade_ssc = unittest.mock.MagicMock()
        points = unittest.mock.MagicMock()
        basepoints = unittest.mock.MagicMock()
        parsecombo = unittest.mock.MagicMock()

        SC = sscpackage.storessc.StoreSSC()
        SC.log_entry(parsecombo, grade_ssc, ticker_entry, points, basepoints)

        mock_json.dumps.assert_called()
        mock_methodvar.connect.assert_called()
        connect_calls = [unittest.mock.call.connect(host='localhost', user=str(os.getenv("DB_USER")),
                                                    password=str(os.getenv("DB_PASS")), database='sscdb')]

        for item in mock_methodvar.method_calls:
            print(item)
        self.assertEqual(connect_calls, mock_methodvar.method_calls)

        # TODO: need to update storetool and test_storetool
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

        mock_connector.connect.return_value.__enter__.return_value.cursor.return_value. \
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
