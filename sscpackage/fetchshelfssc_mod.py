import os
import shelve
import fetchlogssc
import dotenv

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv("CORE_DIR_STOR")


class FetchShelfSSC:
    """
    Attributes:
        -self.ticker
        -self.fetchstoreshelf
        -self.fetchstorename

    Methods:
        -fetchstore() - stores the fetch data in "fetchfiledb" shelve
        -fetchdbpull() - pulls and returns the shelve "fetchfiledb"
    """

    setpath_fetchshelfssc = ROOT_VAR_SSC

    def __init__(self, fetchstoreshelf=setpath_fetchshelfssc + r"fetchfiledb"):
        self.fetchstoreshelf = fetchstoreshelf
        self.fetchstorename = ""

    def fetchstore(self, ticker, fetchstorename, fetch_data, *args, **kwargs):
        self.ticker = ticker
        self.fetchstorename = fetchstorename
        filedb = shelve.open(self.fetchstoreshelf)
        filedb[fetchstorename] = fetch_data
        filedb.close()
        return self.fetchstorename

    def fetchdbpull(self, *args, **kwargs) -> dict:
        with shelve.open(self.fetchstoreshelf) as fetchshelf_pull:
            if fetchshelf_pull.keys():
                bank = dict(fetchshelf_pull)
                return bank
            else:
                print("Shelf Empty")

    def fetch_shelvepurge(self):
        with shelve.open(self.fetchstoreshelf) as fetchstoreshelf_del:
            if fetchstoreshelf_del.keys():
                for key in fetchstoreshelf_del.keys():
                    del fetchstoreshelf_del[key]
            if fetchstoreshelf_del.keys():
                return 1
            else:
                return 0


if __name__ == "__main__":

    import fetchlogssc

    FL = fetchlogssc.FetchLogSSC()

    DB = FetchShelfSSC()

    FL.ssc_fetchlogclear()
    DB.fetch_shelvepurge()

    # testname = "MSFT__TEST1__TEST1__TEST1"
    # testdata = "DATATEST1"
    # testticker = 'MSFT'
    #
    # FS = FetchShelfSSC()
    # FS.fetch_shelvepurge()
    # FS.fetchstore(testticker, testname, testdata)
    #
    # tempdb = FS.fetchdbpull()
    #
    # if testname in tempdb.keys():
    #     print(True)
    # else:
    #     print(False)
