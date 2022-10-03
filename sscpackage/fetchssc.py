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
import shelve
import dotenv
import os
import requests
import sscpackage.fetchshelfssc_mod
import sscpackage.fetchurlssc

dotenv.load_dotenv(dotenv_path=r'C:\SSC\SimpleStockChecker_REV1\venv\.env')
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')




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
                timestamp /= random.randint(1, (today.day + 1))
            keyresult += binbasket[int(math.floor(timestamp))]
            place += 1
            theshuffler(binbasket, timestamp)
        elif place == 7:
            seeder = "All Your Base Are Belong To Us Feeter Viper Ticked A Keck Of Lickled Freckles"
            add = seeder[random.randint(1, 34)]
            keyresult += add
            place += 1
        else:
            keyresult += binbasket[random.randint(1, 61)]
            place += 1

    return keyresult


class FetchSSC:

    @staticmethod
    def pull_fetchfaillist():
        return FetchSSC.ticker_fail

    def __init__(self, *args, **kwargs):
        pass

    def ticker_fail(self, fetchname: str):
        temp_list = []
        with shelve.open(ROOT_VAR_SSC + "ticker_fail") as ticker_fshelve:
            if ticker_fshelve["ticker_fail"]:
                temp_list = ticker_fshelve["ticker_fail"]
                temp_list.append(fetchname)
                ticker_fshelve["ticker_fail"] = temp_list
            else:
                temp_list.append(fetchname)
                ticker_fshelve["ticker_fail"] = temp_list

    @staticmethod
    def purge_tickerfail():
        with shelve.open(ROOT_VAR_SSC + "ticker_fail") as ticker_failpurge:
            if ticker_failpurge:
                if ticker_failpurge.keys():
                    for key in ticker_failpurge:
                        del ticker_failpurge[key]
                if ticker_failpurge.keys():
                    return 1
                else:
                    return 0

    try:
        async def rapid_fetch(self, ticker, *args, **kwargs):
            print("In rapid_fetch ::: " + str(ticker))
            try:
                self.ticker = ticker
                sscrandomkey = myownrandom(15)
                FetchRF = sscpackage.fetchurlssc.FetchUrlSSC(self.ticker)
                FetchRF.fetchshelfinitialize()
                self.url_bank = FetchRF.pullfetchshelf()

            except Exception as er:
                print("Inner Exception: Block 1: Fetchssc")

            for tag in self.url_bank.keys():
                url = self.url_bank[tag]["url"]
                qs = self.url_bank[tag]["qs"]
                head = self.url_bank[tag]["headers"]
                response = requests.request("GET", url=url, headers=head, params=qs)  # Request data
                self.response = response
                if response.status_code == 200:  # If received 'all good' response from API for first request, continue
                    textcast_ssc = response.text
                    self.fetch_data = dict(json.loads(textcast_ssc))
                    FSSC = sscpackage.fetchshelfssc_mod.FetchShelfSSC()
                    fetchstorename = self.ticker + "__" + tag + "__" + str(id(self)) + "__" + sscrandomkey
                    FSSC.fetchstore(ticker=ticker, tag=tag, sscrandomkey=sscrandomkey,
                                    fetchstorename=fetchstorename, fetch_data=self.fetch_data)
                    self.statusfetch = True
                    print(f'Success for ticker : {ticker}')
                elif response.status_code == 401:
                    ticker_failname = self.ticker + "__" + url
                    self.ticker_fail(ticker_failname)
                    print("Invalid API Key - Check User Information")
                    self.statusfetch = False
                else:
                    # TODO: Utilize FetchSSC.ticker_fail list to avoid parsing/grading tickers with failed fetches
                    ticker_failname = self.ticker + "__" + url
                    self.ticker_fail(ticker_failname)
                    print(f'{self.ticker} - failed fetch')
                    self.statusfetch = False
                await asyncio.sleep(1)

    except Exception as er:
        print("Outer Level Exception: fetchssc - rapid_fetch")


if __name__ == "__main__":
    print(myownrandom())
