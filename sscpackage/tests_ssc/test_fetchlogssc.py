import unittest
import os
import dotenv
import shelve

dotenv.load_dotenv(dotenv_path=r'C:\SSC\SimpleStockChecker_REV1\venv\.env')
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')

import fetchlogssc


class TestFetchLog(unittest.TestCase):

    def test_fetchlogwrite(self):
        FLOG = fetchlogssc.FetchLogSSC()
        FLOG.ssc_fetchlogwrite("TEST1")

        with shelve.open(ROOT_VAR_SSC + "fetchlog") as slv:
            temp_output = slv["fetchlog"][0]

        self.assertEqual("TEST1", temp_output)
        FLOG.ssc_fetchlogclear()

    def test_fetchlogclear(self):
        FLOG = fetchlogssc.FetchLogSSC()
        FLOG.ssc_fetchlogclear()

        with shelve.open(ROOT_VAR_SSC + "fetchlog") as slv:
            temp_shelvedict = dict(slv)

        self.assertEqual(temp_shelvedict, {})

    def test_logcompletefetch(self):
        FLOG = fetchlogssc.FetchLogSSC()
        output = FLOG.ssc_logcompletefetch()
        print(output)
    def test_logcompletewrite(self):
        FLOG = fetchlogssc.FetchLogSSC()
        FLOG.ssc_fetchlogclear()
        FLOG.ssc_logcompletepurge()
        log_forprint = FLOG.ssc_logfetch()
        logcomplete_forprint = FLOG.ssc_logcompletefetch()
        print(f'This is logfetch Initial::: {log_forprint}')
        print(f'This is logfetchcomplete Initial::: {logcomplete_forprint}')
        list_ftest = ["MSFT-Balance1", "MSFT-INCOME2", "MSFT-Crud3"]
        for item in list_ftest:
            FLOG.ssc_fetchlogwrite(item)
        output_test = FLOG.ssc_logfetch()
        print(f'Output_test 1 Values: {output_test}')
        #self.assertEqual(output_test, ["MSFT-Balance1", "MSFT-INCOME2", "MSFT-Crud3"])

        FLOG.ssc_logcompletewrite("MSFT", str(1))

        output_test2 = FLOG.ssc_logfetch()
        print(f'Output_test 2 Values: {output_test2}')
        output_test3 = FLOG.ssc_logcompletefetch()
        print(f'Output_test 3 Values: {output_test3}')
        self.assertEqual(output_test2, ["MSFT-INCOME2", "MSFT-Crud3"])
        self.assertEqual(output_test3, ["MSFT-Balance1"])




if __name__ == '__main__':
    unittest.main()
