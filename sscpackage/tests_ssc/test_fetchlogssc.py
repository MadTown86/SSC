import unittest
import os
import dotenv
import shelve

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')

import fetchlogssc
import fetchssc


class TestFetchLog(unittest.TestCase):

    def test_fetchlogwrite(self):
        FLOG = fetchlogssc.FetchLogSSC()
        FLOG.ssc_fetchlogclear()
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

    def test_fetchlogdeletedclear(self):
        FLOG = fetchlogssc.FetchLogSSC()
        FLOG.ssc_logdelete_purge()
        testval = FLOG.ssc_logdelete_fetch()
        self.assertEqual(testval, [])

    def test_fetchlogdeleted_add(self):
        FLOG = fetchlogssc.FetchLogSSC()
        FLOG.ssc_logdelete_purge()
        FLOG.ssc_logdelete_testadd("TEST")
        testval = FLOG.ssc_logdelete_fetch()
        self.assertEqual(testval, "TEST")

    def test_logcompletefetch_testwrite(self):
        FLOG = fetchlogssc.FetchLogSSC()
        FLOG.ssc_logcompletepurge()
        FLOG.ssc_logcomplete_testwrite("TESTWRITE")
        output = FLOG.ssc_logcompletefetch()
        self.assertEqual(["TESTWRITE"], output)

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
        # self.assertEqual(output_test, ["MSFT-Balance1", "MSFT-INCOME2", "MSFT-Crud3"])

        FLOG.ssc_logcompletewrite("MSFT", str(1))

        output_test2 = FLOG.ssc_logfetch()
        print(f'Output_test 2 Values: {output_test2}')
        output_test3 = FLOG.ssc_logcompletefetch()
        print(f'Output_test 3 Values: {output_test3}')
        self.assertEqual(output_test2, ["MSFT-INCOME2", "MSFT-Crud3"])
        self.assertEqual(output_test3, ["MSFT-Balance1"])

    def test_fetchlogdeleted(self):
        try:
            FLOG = fetchlogssc.FetchLogSSC()
            FLOG.ssc_fetchlogclear()
            FLOG.ssc_logdelete_purge()
            FS = fetchssc.FetchSSC()
            FS.purge_tickerfail()
        except Exception as er:
            print("First try block - test_fetchlogdelete")
            print(er)
            pass

        ticker_list = ["MSFT__a1__b1__c1", "MSFT__a2__b2__c1", "MSFT__a3__b3__c1", "NVDA__g4__g5__g6"]
        ticker_fail = ["MSFT__a1__b1__c1"]

        try:
            for item in ticker_list:
                FLOG.ssc_fetchlogwrite(item)

            log_test = FLOG.ssc_logfetch()
        except Exception as er:
            print("Second try block - test_fetchlogdeleted")
            print(er)

        self.assertEqual(log_test, ticker_list)

        print(f'This is initial log: {FLOG.ssc_logfetch()}')

        for item2 in ticker_fail:
            FS.ticker_fail(item2)

        print(f'This is initial faillist: {FS.pull_tickerfail()}')
        temp_faillist = FS.pull_tickerfail()
        for item in temp_faillist:
            print(type(item))
            print(item)
            FLOG.ssc_fetchlogdeleted(*item)

        self.assertEqual(FLOG.ssc_logfetch(), ["NVDA__g4__g5__g6"])


if __name__ == '__main__':
    unittest.main()
