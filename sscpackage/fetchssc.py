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
import fetchlogssc

import sscerrors
import fetchshelfssc_mod
import fetchurlssc
import fetchurlssc_sub

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv("CORE_DIR_STOR")


def theshuffler(basket: [], countage: int) -> None:
    while countage > 0:
        random.shuffle(basket)
        countage -= 1


def myownrandom(keylength: int = 10) -> str:
    try:
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
    except Exception as er:
        print("Exception in fetchssc-> myownrandom")
        print(er)


class FetchSSC:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def ticker_fail(self, fetchname: str) -> None:
        try:
            temp_list = []
            with shelve.open(ROOT_VAR_SSC + "ticker_fail") as ticker_fshelve:
                if ticker_fshelve.keys():
                    if ticker_fshelve["ticker_fail"]:
                        temp_list = ticker_fshelve["ticker_fail"]
                        temp_list.append(fetchname)
                        ticker_fshelve["ticker_fail"] = temp_list
                    else:
                        temp_list.append(fetchname)
                        ticker_fshelve["ticker_fail"] = temp_list
                else:
                    temp_list.append(fetchname)
                    ticker_fshelve["ticker_fail"] = temp_list
        except Exception as er:
            print("Exception in FetchSSC-> ticker_fail")

    @staticmethod
    def pull_tickerfail():
        try:
            res_list = []
            with shelve.open(ROOT_VAR_SSC + "ticker_fail") as ticker_fshelve2:
                if ticker_fshelve2.keys():
                    if ticker_fshelve2["ticker_fail"]:
                        templist = [x for x in ticker_fshelve2["ticker_fail"]]
                        for item in templist:
                            ticker, delvar1, delvar2, uniqueid = item.split("__")
                            res_list.append((ticker, uniqueid))
                        return res_list
                    else:
                        return []
                else:
                    return []
        except Exception as er:
            print("Exception in fetchssc-> pull_tickerfail")
            print(er)

    @staticmethod
    def purge_tickerfail():
        try:
            with shelve.open(ROOT_VAR_SSC + "ticker_fail") as ticker_failpurge:
                if ticker_failpurge:
                    if ticker_failpurge.keys():
                        for key in ticker_failpurge:
                            del ticker_failpurge[key]
                    if ticker_failpurge.keys():
                        return 1
                    else:
                        return 0
        except Exception as er:
            print("Exception in fetchssc -> purge_tickerfail")

    try:

        async def rapid_fetch(self, ticker, *args, **kwargs):
            print("In rapid_fetch ::: " + str(ticker))
            try:
                self.ticker = ticker
                sscrandomkey = myownrandom(15)
                FetchRF = sscpackage.fetchurlssc_sub.FetchUrlSSCSUB(self.ticker)
                FetchRF.fetchshelfinitialize()
                self.url_bank = FetchRF.pullfetchshelf()

            except Exception as er:
                print("Inner Exception: Block 1: Fetchssc")

            for tag in self.url_bank.keys():
                url = self.url_bank[tag]["url"]
                qs = self.url_bank[tag]["qs"]
                head = self.url_bank[tag]["headers"]
                response = requests.request(
                    "GET", url=url, headers=head, params=qs
                )  # Request data

                self.response = response

                self.fetchstorename = (
                    f"{self.ticker}__{tag}__{id(self)}__{sscrandomkey}"
                )

                if (
                    response.status_code == 200
                ):  # If received 'all good' response from API for first request, continue
                    self.fetch_data = dict(response.json())
                    FSSC = sscpackage.fetchshelfssc_mod.FetchShelfSSC()
                    FSSC.fetchstore(
                        ticker=ticker,
                        fetchstorename=self.fetchstorename,
                        fetch_data=self.fetch_data,
                    )
                    FS_SSC = fetchlogssc.FetchLogSSC()
                    FS_SSC.ssc_fetchlogwrite(fetchstorename=self.fetchstorename)
                    del FS_SSC
                    self.statusfetch = True
                    print(f"Success for ticker : {ticker}")
                elif response.status_code == 401:
                    self.ticker_fail(self.fetchstorename)
                    print("Invalid API Key - Check User Information")
                    self.statusfetch = False
                elif response.status_code == 502:
                    self.ticker_fail(self.fetchstorename)
                    print("API Server Gateway Error - API not currently working")
                    self.statusfetch = False
                else:
                    print(f"OTHER RESPONSE ERROR CODE: {response.status_code}")
                    # TODO: Utilize FetchSSC.ticker_fail list to avoid parsing/grading tickers with failed fetches
                    self.ticker_fail(self.fetchstorename)
                    print(f"{self.ticker} - failed fetch")
                    self.statusfetch = False
                await asyncio.sleep(1)

    except Exception as er:
        print("Outer Level Exception: fetchssc - rapid_fetch")


if __name__ == "__main__":
    print(myownrandom())
