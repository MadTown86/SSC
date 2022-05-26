import sscpackage.fetchurlssc
import asyncio
import requests
import sscpackage.fetchshelfssc_mod
import json


class FetchSSC:
    def __init__(self, ticker="MSFT", *args, **kwargs):
        self.ticker = ticker

    async def rapid_fetch(self, *args, **kwargs):
        FetchRF = sscpackage.fetchurlssc.FetchUrlSSC()
        self.url_bank = FetchRF.pullfetchshelf()
        for key in self.url_bank.keys():
            url = self.url_bank[key]["url"]
            qs = self.url_bank[key]["qs"]
            head = self.url_bank[key]["headers"]
            response = requests.request("GET", url=url, headers=head, params=qs)  # Request data
            self.response = response
            if response.status_code == 200:  # If received 'all good' response from API for first request, continue
                self.fetch_data = dict(json.loads(response.text))
                FSSC = sscpackage.fetchshelfssc_mod.FetchShelfSSC()
                FSSC.fetchstore(self.ticker, key, id(self), self.fetch_data)
                self.statusfetch = True
            else:
                self.statusfetch = False
            await asyncio.sleep(1)


