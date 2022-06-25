import unittest
from unittest.mock import patch
import simp_tablefuncs
import os

import sscpackage.tests_ssc.simp_tablefuncs

testarg_create = {'testname': 'varchar(50)', 'testname2': 'json'}


class TestSimpTableFuncs(unittest.TestCase):

    def test_createtable(self):
        testarg_create = {'testname':'varchar(50)', 'testname2':'json'}
        STF = simp_tablefuncs.Simp_TableFuncs()
        test_str = STF.create_table('test', True, **testarg_create)
        print(test_str)
        expect_string = """CREATE TABLE test (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, testname VARCHAR(50), testname2 JSON);"""
        self.assertEqual(test_str, expect_string)
        del STF

    @patch('sscpackage.tests_ssc.simp_tablefuncs.mysql.connector')
    def test_create_commit(self, mock_connector):
        STF = simp_tablefuncs.Simp_TableFuncs()
        commitstr = STF.create_table('test', True, **testarg_create)
        STF.create_commit(commitstr)

        correctcallconnect = unittest.mock.call(database='sscdb', host='localhost', password=os.getenv("DB_PASS"), user=os.getenv("DB_USER"))
        correctcallexecute = unittest.mock.call(commitstr, multi=True)
        self.assertEqual(mock_connector.connect.call_args, correctcallconnect)
        mock_execute = mock_connector.connect.return_value.__enter__.return_value.cursor.return_value\
            .__enter__.return_value.execute.call_args
        self.assertEqual(mock_execute, correctcallexecute)
        del STF
        del mock_connector

    def test_delete_table(self):
        STF = sscpackage.tests_ssc.simp_tablefuncs.Simp_TableFuncs()
        test_value = STF.delete_table("test")
        correct_value = "DROP TABLE IF EXISTS test;"
        self.assertEqual(test_value, correct_value)
        del STF

    def test_create_sqlfunc(self):
        STF = sscpackage.tests_ssc.simp_tablefuncs.Simp_TableFuncs()
        STF.create_sqlfunc(None)
        del STF

    def test_runfunc(self):
        STF = sscpackage.tests_ssc.simp_tablefuncs.Simp_TableFuncs()
        self.assertEqual(((STF.runfunc('tableExistsOrNot', 'logentry'))[0])[0], 1)
        del STF


if __name__ == '__main__':
    unittest.main()
