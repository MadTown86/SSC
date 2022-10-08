import fetchurlssc
import os
import shelve


class FetchUrlSSCSUB(fetchurlssc.FetchUrlSSC):
    def __init__(self, ticker, *args, **kwargs):
        super().__init__(ticker, *args, **kwargs)
        self.url_income = "https://yh-finance.p.rapidapi.com/stock/v2/get-financials"
        self.url_balance = self.url_income
        self.url_sectordata = "https://yh-finance.p.rapidapi.com/stock/v2/get-profile"
        self.qs_inc_bal = {"symbol": self.ticker, "region": "US"}

        pass

    def fetchshelfinitialize(self):
        try:
            if self.checkpaths():
                self.purge_fetchurlshelf()
                # These are the two variables necessary to ping the API's, first two take qs, url_ar takes 2
                qs_ar = {"symbol": self.ticker, "region": "US"}
                qs_val = {"ticker_symbol": self.ticker, "format": "json"}
                qs_sector = {"ticker_symbol": self.ticker}

                # header information including RAPI_key environment variable, necessary for API data fetch
                headers = {
                    'x-rapidapi-host': "stock-market-data.p.rapidapi.com",
                    'x-rapidapi-key': os.getenv("RAPI_key")
                }

                # Header for the _ar request
                headers_ar_inc_bal = {
                    'x-rapidapi-host': "yh-finance.p.rapidapi.com",
                    'x-rapidapi-key': os.getenv("RAPI_key")
                }

                # Create and prime shelf with core necessary fetches
                fetchshelf = shelve.open(self.pathnamefetchurls)
                self.fetch_apidict = {"url_income": {"url": self.url_income, "qs": self.qs_inc_bal, "headers": headers_ar_inc_bal},
                                      "url_balance": {"url": self.url_balance, "qs": self.qs_inc_bal, "headers": headers_ar_inc_bal},
                                      "url_ar": {"url": self.url_ar, "qs": qs_ar, "headers": headers_ar_inc_bal},
                                      "url_val": {"url": self.url_val, "qs": qs_val, "headers": headers},
                                      "url_sectordata": {"url": self.url_sectordata, "qs": qs_sector, "headers": headers}}
                fetchshelf[self.shelfkey] = self.fetch_apidict
                self.fetchbank = fetchshelf[self.shelfkey]
                fetchshelf.close()
            else:
                # TODO: finish looking into 'raise' 'exception' structure for sscerror.py
                pass
        except Exception as er:
            print(er)

