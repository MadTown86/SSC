"""
Core fetching logic - with Requests
"""

import asyncio
import datetime
import json
import math
import random
import string
import time

import requests

import sscpackage.fetchshelfssc_mod
import sscpackage.fetchurlssc


def theshuffler(basket, countage):
    while countage > 0:
        random.shuffle(basket)
        countage -= 1


def myownrandom(keylength=10):
    place = 0
    startbasket = string.digits + string.ascii_letters
    binbasket = [str(x) for x in startbasket]
    random.shuffle(binbasket)
    keyresult = ""
    while len(keyresult) < keylength:
        random.shuffle(binbasket)
        if place == 4:
            timestamp = int(math.floor(time.time() * 2000))
            while math.floor(timestamp) > 61:
                today = datetime.date.today()
                timestamp /= random.randint(1, (today.day+1))
            keyresult += binbasket[int(math.floor(timestamp))]
            place += 1
            theshuffler(binbasket, timestamp)
        elif place == 7:
            seeder = "GroverDaniellePotterShoeDonlonPennPantsMom"
            add = seeder[random.randint(1, 34)]
            keyresult += add
            place += 1
        else:
            keyresult += binbasket[random.randint(1, 61)]
            place += 1

    return keyresult




class FetchSSC:
    ticker_fail = ""

    @staticmethod
    def pull_fetchfaillist():
        return FetchSSC.ticker_fail

    def __init__(self, *args, **kwargs):
        pass

    try:
        async def rapid_fetch(self, ticker, *args, **kwargs):
            print("In rapid_fetch ::: " + str(ticker))
            try:
                self.ticker = ticker
                print(self.ticker)
                timestampidrf = myownrandom(15)
                print("After Timestamp")
                FetchRF = sscpackage.fetchurlssc.FetchUrlSSC(self.ticker)
                print("After FetchURL Instantiation")
                FetchRF.fetchshelfinitialize()
                print("After .fetchshelfinitialize")
                self.url_bank = FetchRF.pullfetchshelf()
            except Exception as er:
                print("Inner Exception: Block 1: Fetchssc")

            for key in self.url_bank.keys():
                url = self.url_bank[key]["url"]
                qs = self.url_bank[key]["qs"]
                head = self.url_bank[key]["headers"]
                print("Right before request")
                response = requests.request("GET", url=url, headers=head, params=qs)  # Request data
                print("Right after request")
                self.response = response
                if response.status_code == 200:  # If received 'all good' response from API for first request, continue
                    textcast_ssc = response.text
                    self.fetch_data = dict(json.loads(textcast_ssc))
                    FSSC = sscpackage.fetchshelfssc_mod.FetchShelfSSC()
                    FSSC.fetchstore(ticker=ticker, key=key, idssc=id(self), fetch_data=self.fetch_data, timestampidfs=timestampidrf)
                    self.statusfetch = True
                    print(f'Success for ticker : {ticker}')
                elif response.status_code == 401:
                    if key == list(self.url_bank.keys())[-1:]:
                        FetchSSC.ticker_fail += str(self.ticker) + "__" + str(url)
                    FetchSSC.ticker_fail += str(self.ticker) + "__" + str(url) + ", "
                    print("Invalid API Key - Check User Information")
                    self.statusfetch = False
                else:
                    if key == list(self.url_bank.keys())[-1:]:
                        FetchSSC.ticker_fail += str(self.ticker) + "__" + str(url)
                    FetchSSC.ticker_fail += str(self.ticker) + "__" + str(url) + ", "
                    print(f'{self.ticker} - failed fetch')
                    self.statusfetch = False
                await asyncio.sleep(1)

    except Exception as er:
        print("Outer Level Exception: fetchssc - rapid_fetch")


if __name__ == "__main__":
    print(myownrandom())
