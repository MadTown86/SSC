import shelve

class FetchShelfSSC:
    """
    Attributes:
        -self.ticker
        -self.fetchstoreshelf

    Methods:
        -fetchstore() - stores the fetch data in "fetchfiledb" shelve
        -fetchdbpull() - pulls and returns the shelve "fetchfiledb"
    """
    def __init__(self, ticker="MSFT", fetchstoreshelf="fetchfiledb"):
        self.ticker = ticker
        self.fetchstoreshelf = fetchstoreshelf

    def fetchstore(self, key="url_income", idssc="DEFAULTID", fetch_data="DEFAULTDATA",
                   *args, **kwargs):
        filedb = shelve.open(self.fetchstoreshelf)
        fetchstorename = str(self.ticker) + "__" + str(key) + "__" + str(idssc)
        filedb[fetchstorename] = fetch_data
        filedb.close()
        return fetchstorename

    def fetchdbpull(self, *args, **kwargs):
        with shelve.open(self.fetchstoreshelf) as fetchshelf_pull:
            if fetchshelf_pull.keys():
                bank = dict(fetchshelf_pull)
                fetchshelf_pull.close()
                return bank
            else:
                print("Shelf Empty")
