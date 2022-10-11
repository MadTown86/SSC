import fetchurlssc
import os
import shelve


class FetchUrlSSCSUB(fetchurlssc.FetchUrlSSC):
    def __init__(self, ticker, *args, **kwargs):
        super().__init__(ticker, *args, **kwargs)

        self.url_income = "https://yh-finance.p.rapidapi.com/stock/v2/get-financials"
        self.url_balance = self.url_income
        self.url_sectordata = "https://yh-finance.p.rapidapi.com/stock/v2/get-profile"
        self.url_val = "https://yh-finance.p.rapidapi.com/stock/v3/get-statistics"

        self.qs_inc_bal = {"symbol": self.ticker, "region": "US"}
        self.qs_sector = {"symbol": self.ticker, "region": "US"}
        self.qs_val = {"symbol": self.ticker}

        pass

    def fetchshelfinitialize(self):
        try:
            if self.checkpaths():
                self.purge_fetchurlshelf()

                headers = {
                    'x-rapidapi-host': "yh-finance.p.rapidapi.com",
                    'x-rapidapi-key': os.getenv("RAPI_key")
                }

                # Create and prime shelf with core necessary fetches
                fetchshelf = shelve.open(self.pathnamefetchurls)
                self.fetch_apidict = {"url_income": {"url": self.url_income, "qs": self.qs_inc_bal,
                                                     "headers": headers},

                                      "url_balance": {"url": self.url_balance, "qs": self.qs_inc_bal,
                                                      "headers": headers},

                                      "url_ar": {"url": self.url_ar, "qs": self.qs_ar, "headers": headers},

                                      "url_val": {"url": self.url_val, "qs": self.qs_val, "headers": headers},

                                      "url_sectordata": {"url": self.url_sectordata, "qs": self.qs_sector,
                                                         "headers": headers}
                                      }

                fetchshelf[self.shelfkey] = self.fetch_apidict
                self.fetchbank = fetchshelf[self.shelfkey]
                fetchshelf.close()
            else:
                # TODO: finish looking into 'raise' 'exception' structure for sscerror.py
                pass
        except Exception as er:
            print(er)

if __name__ == "__main__":
    pass


