import shelve

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
    setpath_fetchshelfssc = r'C:\SSC\SimpleStockChecker_REV1\sscpackage\storage'

    def __init__(self, ticker="MSFT",
                 fetchstoreshelf=setpath_fetchshelfssc + r"\fetchfiledb"):
        self.ticker = ticker
        self.fetchstoreshelf = fetchstoreshelf
        self.fetchstorename = ""

    def fetchstore(self, key="url_income", idssc="DEFAULTID", fetch_data="DEFAULTDATA", timestampidfs="DEFTSID",
                   *args, **kwargs):
        filedb = shelve.open(self.fetchstoreshelf)
        fetchstorename = str(self.ticker) + "__" + str(key) + "__" + str(idssc) + "__" + str(timestampidfs)
        filedb[fetchstorename] = fetch_data
        filedb.close()
        self.fetchstorename = fetchstorename
        return fetchstorename

    def fetchdbpull(self, *args, **kwargs):
        with shelve.open(self.fetchstoreshelf) as fetchshelf_pull:
            if fetchshelf_pull.keys():
                bank = dict(fetchshelf_pull)
                fetchshelf_pull.close()
                return bank
            else:
                print("Shelf Empty")


