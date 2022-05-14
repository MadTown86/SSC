import shelve

class FetchShelfSSC:
    """
    This class will store the fetched data into the shelf after it is received from API.
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
