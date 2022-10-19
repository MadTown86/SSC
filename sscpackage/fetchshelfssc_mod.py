import shelve
import fetchlogssc
import dotenv
import os

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

    def __init__(self, fetchstoreshelf=setpath_fetchshelfssc + r"\fetchfiledb"):
        self.fetchstoreshelf = fetchstoreshelf
        self.fetchstorename = ""

    def fetchstore(self, ticker, fetchstorename, fetch_data, *args, **kwargs):
        self.ticker = ticker
        try:
            self.fetchstorename = fetchstorename
            filedb = shelve.open(self.fetchstoreshelf)
            filedb[fetchstorename] = fetch_data
            filedb.close()
            FS_SSC = fetchlogssc.FetchLogSSC()
            FS_SSC.ssc_fetchlogwrite(fetchstorename=self.fetchstorename)
            del FS_SSC
            return fetchstorename
        except Exception as er:
            print("Exception Fetchstore Method:")
            print(er)

    def fetchdbpull(self, *args, **kwargs):
        with shelve.open(self.fetchstoreshelf) as fetchshelf_pull:
            if fetchshelf_pull.keys():
                bank = dict(fetchshelf_pull)
                fetchshelf_pull.close()
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
