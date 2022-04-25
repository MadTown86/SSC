import json
import shelve
import asyncio
import requests
import os
import sys
import unittest
from unittest.mock import Mock
from unittest.mock import patch



"""
2/4/22 - GD

ssc_ft is a module that houses the scripts for querying data from RapidAPI and writing it to file for use in ssc_pt
"""
"""
global prog_time
prog_time = None

"""

"""
This is to test branch functionality GIT/Pycharm
"""

"""
def get_financials(ticker_entry: "string" = "MSFT"):
import time

# A function attribute to allow ticker_entry value to be pulled after import into other module
get_financials.ticker_entryf = ticker_entry

"""
"""
2/4/22 - GD
This function receives the ticker symbol from SSC_GUI that is user input

It uses this ticker symbol as a variable for fetching data from RapidAPI.

It parses the data from raw response bytestring to python dict, then stores the python dict as JSON

:param ticker_entry: this is the ticker symbol that was qualified from SSC_GUI
:return: no returns
"""
"""

print("Entering get financials")
print(ticker_entry)
# 2/8/22 - GD - Idea to make a nested function in get_financials that updates the global value with the elapsed time
global prog_time
global res_json # setting res_json as formatted version of JSON blob from RapidAPI
global res_direct # direct results from connection
# As I learn more Python, I believe these are unnecessary and could be prone to error

# These are three variables holding the API locations for the information calls
url_income = "https://stock-market-data.p.rapidapi.com/stock/financials/income-statement/annual-historical"
url_balance = "https://stock-market-data.p.rapidapi.com/stock/financials/balance-sheet/annual-historical"
url_ar = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-upgrades-downgrades"
url_val = "https://stock-market-data.p.rapidapi.com/stock/valuation/historical-valuation-measures"

# 2/8/22 - GD - Adding sector data, need to start to grade by sector eventually
url_sectordata = "https://stock-market-data.p.rapidapi.com/stock/company-info"

# These are the two variables necessary to ping the API's, first two take qs, url_ar takes 2
qs_inc_bal = {"ticker_symbol": ticker_entry, "format": "json"}
qs_ar = {"symbol": ticker_entry, "region": "US"}
qs_val = {"ticker_symbol": ticker_entry, "format": "json"}
qs_sector = {"ticker_symbol": ticker_entry}

# header information including RAPI_key environment variable, necessary for API data fetch
headers = {
    'x-rapidapi-host': "stock-market-data.p.rapidapi.com",
    'x-rapidapi-key': os.getenv("RAPI_key")
}

# Header for the _ar request
headers_ar = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': os.getenv("RAPI_key")
}

url_bank = {"url_income": [url_income, qs_inc_bal, headers], "url_balance": [url_balance, qs_inc_bal, headers],
            "url_ar": [url_ar, qs_ar, headers_ar],
            "url_val": [url_val, qs_val, headers],
            "url_sectordata": [url_sectordata, qs_sector, headers]}


# response = url_income JSON, response_balance = url_balance JSON, response_ar = url_ar JSON
# Following code requests information from the API's and assigns the data to the aforementioned variables

def response_fetch(*response_arg):
    global prog_time
    prog_time = 0
    res_time = 0
    for x in response_arg:
        res_time += x.elapsed.total_seconds()
    prog_time = res_time
    return

response = requests.request("GET", url_income, headers=headers, params=qs_inc_bal) # Request data for url_income
if response.status_code == 200:  # If received 'all good' response from API for first request, continue
    res_direct = response.text  # Used as a function attribute in ssc_gui to pass into log_entry
    fetch_data = dict(json.loads(response.text))
    print("In first fetch")

    with open("incomestatements.json", 'w') as income_statements:
        income_statements.truncate()
        json.dump(fetch_data, income_statements, indent=5, separators=(", ", ": "), sort_keys=False)
        income_statements.close()

    response_balance = requests.request("GET", url_balance, headers=headers, params=qs_inc_bal)  # fetch for url_bal
    if response_balance.status_code == 200:  # If received 'all good' continue
        rb_data = dict(json.loads(response_balance.text))
        print("In second fetch")

        with open("balancesheets.json", 'w') as balance_sheets:
            balance_sheets.truncate()
            json.dump(rb_data, balance_sheets, indent=5, separators=(", ", ": "), sort_keys=False)
            balance_sheets.close()

        response_ar = requests.request("GET", url_ar, headers=headers_ar, params=qs_ar) # Fetch url_ar
        if response_ar.status_code == 200:  # if received 'all good' start to reformat data
            ar_data = dict(json.loads(response_ar.text))
            print("In third fetch")

            with open("ardata.json", 'w') as ar_sheets:
                ar_sheets.truncate()
                json.dump(ar_data, ar_sheets, indent=5, separators=(", ", ": "), sort_keys=False)
                ar_sheets.close()

            response_val = requests.request("GET", url_val, headers=headers, params=qs_val) #Fetch  valuation
            if response_val.status_code == 200:
                val_data = dict(json.loads(response_val.text))
                print("In fourth fetch")

                with open("valdata.json", 'w') as val_sheets:
                    val_sheets.truncate()
                    json.dump(val_data, val_sheets, indent=5, separators=(", ", ": "), sort_keys=False)
                    val_sheets.close()

                response_sector = requests.request("GET", url_sectordata, headers=headers, params=qs_sector)
                if response_sector.status_code == 200:
                    response_data = dict(json.loads(response_sector.text))
                    print("In fifth fetch")

                    with open("sectordata.json", 'w') as sector_sheets:
                        sector_sheets.truncate()
                        json.dump(response_data, sector_sheets, indent=5, separators=(", ", ": "), sort_keys=False)
                        sector_sheets.close()

                    response_fetch(response, response_balance, response_val, response_ar, response_sector)
                    print(prog_time)

                else:
                    print("Unsuccessful fifth fetch from API")
                    print("API Response Status Code: " + str(response_sector.raise_for_status()))
                    raise ConnectionError

            else:
                print("Unsuccessful fourth fetch from API")
                print("API Response Status Code: " + str(response_val.raise_for_status()))
                raise ConnectionError
        else:
            print("Unsuccessful third fetch from API")  # If 'all good' response not received, raise error
            print("API Response Status Code: " + str(response_ar.raise_for_status()))
            raise ConnectionError
    else:
        print("Unsuccessful second fetch from API")  # If 'all good' response not received, raise error
        print("API Response Status Code: " + str(response_balance.raise_for_status()))
        raise ConnectionError
else:
    print("Unsuccessful first fetch from API")  # If 'all good' response not received, raise error
    print("API Response Status Code: " + str(response.raise_for_status()))
    raise ConnectionError

print("Done with fetch")
return ticker_entry
"""


# fetchurlshelfdb - default
class FetchDataStoreSSC:
    """
    This class will store the fetched data into the shelf after it is received from API.
    #5
    """

    def fetchstore(self, ticker="MSFT", key="url_income", idssc="DEFAULTID", fetch_data="DEFAULTDATA", fetchstoreshelf = "fetchfiledb", *args, **kwargs):
        filedb = shelve.open(fetchstoreshelf)
        fetchstorename = str(ticker) + "__" + str(key) + "__" + str(idssc)
        filedb[fetchstorename] = fetch_data
        filedb.close()
        return fetchstorename


# fetchurlshelfdb - default
class FetchUrlAddSSC:
    """
    This class is going to combine variables and pass to FetchCyclerSSC as arguments for 'requests' module
    It will also allow you to add another fetch

    #3
    """

    def addfetchssc(self, fetchnamessc="DEFAULTNAME", fetchurlssc="DEFAULTURL", fetchqsssc="DEFAULTSSC",
                      fetchheadersssc="DEFAULTHEADER", shelfnamessc="fetchurlshelfdb", *args, **kwargs):
        with shelve.open(shelfnamessc) as fetchshelf:
            temp_bankadd = dict(fetchshelf["fetch_bank"])
            temp_bankadd.update({fetchnamessc: {"url": fetchurlssc, "qs": fetchqsssc, "headers": fetchheadersssc}})
            fetchshelf["fetch_bank"] = temp_bankadd
            fetchshelf.close()


# fetchurlshelfdb - default
class FetchUrlDeleteSSC:
    """
    This class deletes a fetch dictionary from the shelf defined
    #5
    """
    def deletefetchssc(self, fetchnamessc="DEFAULTNAME", shelfnamessc="fetchrlshelfdb", *args, **kwargs):
        with shelve.open(shelfnamessc) as fetchshelfdel:
            temp_bankdel = dict(fetchshelfdel["fetch_bank"])
            temp_bankdel.pop(fetchnamessc)
            fetchshelfdel["fetch_bank"] = temp_bankdel
            fetchshelfdel.close()


# fetchurlshelfdb - default
class FetchUrlRequestShelfSSC:
    """
    This class is going to pull the fetchshelf information and return a dictionary containing the arguments for requests
    #4
    """

    def pullfetchshelf(self, fetchurlshelfnamessc = "fetchurlshelfdb", *args, **kwargs):
        FFISSC = FetchFirstInitializeSSC()
        FFISSC.fetchshelfinitialize()
        with shelve.open(fetchurlshelfnamessc) as fetchshelfpullssc:
            if fetchshelfpullssc["fetch_bank"]:
                bank = dict(fetchshelfpullssc["fetch_bank"])
                fetchshelfpullssc.close()
                return bank
            else:
                print("error in pullfetchshelf")


# fetchurlshelfdb - default
class FetchUrlCheckPrimerSSC:
    """
    This class checks to see if shelf already initialized to bypass over-writing shelf that stores fetch variables

    #1 Unit Test
    """

    def __init__(self, pathbakssc="fetchurlshelfdb.bak", pathdatssc="fetchurlshelfdb.dat",
                 pathdirssc="fetchurlshelfdb.dir", *args, **kwargs):
        self.pathbakssc = pathbakssc
        self.pathdatssc = pathdatssc
        self.pathdirssc = pathdirssc

    def checkpaths(self):
        fetchpaths = [self.pathbakssc, self.pathdatssc, self.pathdirssc]
        count = 0
        for path in fetchpaths:
            if os.path.exists(path):
                count += 1

        if count == 3:
            return True
        else:
            return False


# fetchurlshelfdb - default
class FetchUrlCheckShelfSSC:
    """
    Checks for existence of information on shelf at filepath
    """
    def checkshelfcontent(self, shelfname="fetchurlshelfdb"):
        with shelve.open(shelfname) as fetchshelfcheck:
            if fetchshelfcheck:
                return True
            else:
                return False


# either shelf can be cleared
class ClearFetchShelfSSC:
    """
    Process to purge existing URL shelf - Default filename = fetchurlshelfdb

    You can pass in "fetchfiledb" to clear other shelf
    """
    def clearfetchshelfssc(self, path="fetchurlshelfdb"):
        FEPrimerClearFetch = FetchUrlCheckPrimerSSC()
        if FEPrimerClearFetch.checkpaths():
            with shelve.open(path) as fetchshelf:
                for key in fetchshelf.keys():
                    del fetchshelf[key]
                fetchshelf.close()


# fetchurlshelfdb - default
class FetchFirstInitializeSSC:
    """
    These are the initial hardcoded fetches from API, it packages and stores them in a shelf
    #2 Unit Test
    """
    def fetchshelfinitialize(self, ticker="MSFT"):
        self.ticker = ticker
        FCP1 = FetchUrlCheckPrimerSSC()
        if FCP1.checkpaths():
            # These are variables holding the API locations for the information calls
            url_income = "https://stock-market-data.p.rapidapi.com/stock/financials/income-statement/annual-historical"
            url_balance = "https://stock-market-data.p.rapidapi.com/stock/financials/balance-sheet/annual-historical"
            url_ar = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-upgrades-downgrades"
            url_val = "https://stock-market-data.p.rapidapi.com/stock/valuation/historical-valuation-measures"
            url_sectordata = "https://stock-market-data.p.rapidapi.com/stock/company-info"


            # These are the two variables necessary to ping the API's, first two take qs, url_ar takes 2
            qs_inc_bal = {"ticker_symbol": self.ticker, "format": "json"}
            qs_ar = {"symbol": self.ticker, "region": "US"}
            qs_val = {"ticker_symbol": self.ticker, "format": "json"}
            qs_sector = {"ticker_symbol": self.ticker}

            # header information including RAPI_key environment variable, necessary for API data fetch
            headers = {
                'x-rapidapi-host': "stock-market-data.p.rapidapi.com",
                'x-rapidapi-key': os.getenv("RAPI_key")
            }

            # Header for the _ar request
            headers_ar = {
                'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
                'x-rapidapi-key': os.getenv("RAPI_key")
            }

            # Create and prime shelf with core necessary fetches
            fetchshelf = shelve.open("fetchurlshelfdb")
            self.fetch_apidict = {"url_income": {"url": url_income, "qs": qs_inc_bal, "headers": headers},
                             "url_balance": {"url": url_balance, "qs": qs_inc_bal, "headers": headers},
                             "url_ar": {"url": url_ar, "qs": qs_ar, "headers": headers_ar},
                             "url_val": {"url": url_val, "qs": qs_val, "headers": headers},
                             "url_sectordata": {"url": url_sectordata, "qs": qs_sector, "headers": headers}}
            fetchshelf["fetch_bank"] = self.fetch_apidict
            self.fetchbank = fetchshelf["fetch_bank"]
            fetchshelf.close()
        else:
            return 1


# fetchfiledb - default
class FetchPullDBSSC:
    def __init__(self, shelffile="fetchfiledb", *args, **kwargs):
        self.shelffile = shelffile
        pass

    def fetchdbpull(self, *args, **kwargs):
        with shelve.open(self.shelffile) as fetchshelf_pull:
            if fetchshelf_pull.keys():
                bank = dict(fetchshelf_pull)
                fetchshelf_pull.close()
                return bank
            else:
                print("Shelf Empty")


class FetchCyclerSSC:
    def __init__(self, ticker="MSFT", *args, **kwargs):
        self.ticker = ticker

    async def rapid_fetch(self, url_bank, *args, **kwargs):
        self.url_bank = url_bank
        print(self.url_bank)
        for key in self.url_bank.keys():
            print("KEY:  %s :::: Value:  %s  ::" % (key, self.url_bank[key]))
        for key in self.url_bank.keys():
            url = self.url_bank[key]["url"]
            qs = self.url_bank[key]["qs"]
            head = self.url_bank[key]["headers"]
            response = requests.request("GET", url=url, headers=head, params=qs)  # Request data
            self.response = response
            if response.status_code == 200:  # If received 'all good' response from API for first request, continue
                self.fetch_data = dict(json.loads(response.text))
                FSTORESSC = FetchDataStoreSSC()
                FSTORESSC.fetchstore(self.ticker, key, id(self), self.fetch_data)
                self.statusfetch = True
            else:
                self.statusfetch = False
            await asyncio.sleep(1)

        print("success")


class FetchStarterSSC:
    """
    This class accepts the tickerlist from user input as an arg, then starts parsing with asyncio and a maximum of 5
    concurrent fetches (max simultaneous RapidAPI will allow for my payment level)
    """

    def __init__(self, tickerlist=None):
        if tickerlist is None:
            tickerlist = ["MSFT", "AMD", "TTD", "ETSY", "UAA"]
        self.tickerlist = tickerlist

    async def fetch_cycle(self, *args, **kwargs):
        while self.tickerlist:
            if len(self.tickerlist) > 5:
                await asyncio.gather(
                    FetchCyclerSSC(self.tickerlist.pop(0)).rapid_fetch(),
                    FetchCyclerSSC(self.tickerlist.pop(0)).rapid_fetch(),
                    FetchCyclerSSC(self.tickerlist.pop(0)).rapid_fetch(),
                    FetchCyclerSSC(self.tickerlist.pop(0)).rapid_fetch(),
                    FetchCyclerSSC(self.tickerlist.pop(0)).rapid_fetch(),
                )
            else:
                for indexno in range(len(self.tickerlist)):
                    await asyncio.gather(FetchCyclerSSC(self.tickerlist.pop(0)).rapid_fetch())


class FetchContainerSSC:
    def __init__(self, *args, **kwargs):
        FetchContainerSSC.__initializeself(self)
        pass

    def __initializeself(self):
        self.fetchstoressc = FetchDataStoreSSC()
        self.fetchaddssc = FetchUrlAddSSC()
        self.fetchrequestshelfssc = FetchUrlRequestShelfSSC()
        self.fetchcheckprimer = FetchUrlCheckPrimerSSC()
        self.fetchfirstinitialize = FetchFirstInitializeSSC()
        self.fetchcycler = FetchCyclerSSC()
        self.fetchstarter = FetchStarterSSC()


class TestSSCShelvSystem(unittest.TestCase):
    """
    This test class houses unit tests for each class when possible
    """
    def test_fetchcheckprimer(self):
        FCP1 = FetchUrlCheckPrimerSSC()
        self.assertEqual(FCP1.checkpaths(), True, "Files will be created after first run")

    def test_fetchshelfinitialize(self):
        FFI1 = FetchFirstInitializeSSC()
        FFI1.fetchshelfinitialize()
        fetchdb = shelve.open("fetchurlshelfdb")
        bank = fetchdb["fetch_bank"]
        fetchdb.close()
        self.assertEqual(bank, FFI1.fetchbank, "Check Shelf for errors")

    def test_addfetchssc(self):
        result = ''
        FASSC1 = FetchUrlAddSSC()

        def resultadd():
            nonlocal result
            with shelve.open("fetchurlshelfdb") as fetchshelf2:
                test_bank2 = dict(fetchshelf2["fetch_bank"])
                result += str(bool("DEFAULTNAME" in test_bank2.keys()))
                fetchshelf2.close()

        resultadd()
        FASSC1.addfetchssc()
        resultadd()
        with shelve.open("fetchurlshelfdb") as fetchshelf3:
            test_bank3 = dict(fetchshelf3["fetch_bank"])
            test_bank3.pop("DEFAULTNAME")
            fetchshelf3["fetch_bank"] = test_bank3
            fetchshelf3.close()
        resultadd()
        self.assertEqual(result, "FalseTrueFalse")

    def test_clearfetchurlssc(self):
        result_clfessc = ''
        FECheckShelf = FetchUrlCheckShelfSSC()
        FEClearShelf = ClearFetchShelfSSC()
        if FECheckShelf.checkshelfcontent():
            result_clfessc += "True"
            FEClearShelf.clearfetchshelfssc()
            if FECheckShelf.checkshelfcontent():
                result_clfessc += "True"
            else:
                result_clfessc += "False"
        else:
            FEAdd = FetchUrlAddSSC()
            FEAdd.addfetchssc()
            if FECheckShelf.checkshelfcontent():
                result_clfessc += "True"
                FEClearShelf.clearfetchshelfssc()
                if FECheckShelf.checkshelfcontent():
                    result_clfessc += "True"
                else:
                    result_clfessc += "False"

        self.assertEqual(result_clfessc, "TrueFalse")

    def test_fetchrequestshelfssc(self):
        FRS1 = FetchUrlRequestShelfSSC()
        frsssc_bank = FRS1.pullfetchshelf()
        urllistssc = ["url_income", "url_balance", "url_ar", "url_val", "url_sectordata"]
        resultfetchssc=''
        for urltestname in urllistssc:
            if urltestname in frsssc_bank.keys():
                resultfetchssc += "TRUE"
            else:
                resultfetchssc += "FALSE"
            self.assertIn(resultfetchssc, "TRUETRUETRUETRUETRUE")

    def test_fetchstoreshelf(self):
        fstore1 = FetchDataStoreSSC()
        test_fetchstorename = fstore1.fetchstore()
        result = ''
        filedb = shelve.open("fetchfiledb")
        if bool(filedb[test_fetchstorename]):
            result += "True"
        else:
            result += "False"

        filedb.pop(test_fetchstorename)
        if test_fetchstorename in filedb.keys():
            result += "True"
        else:
            result += "False"

        self.assertEqual(result, "TrueFalse", "Check Test Fetch Store Shelf")

    def test_fetchpulldb(self):
        FPDBTest = FetchPullDBSSC()
        bank = FPDBTest.fetchdbpull()

    """
    async def testsscfetch(self):
        FS1 = FetchStarterSSC(["TTD", "MU"])
        print(FS1.tickerlist)

        FC1 = FetchCyclerSSC("MSFT")
        FC1.initialize_querydata()
        for key in FC1.url_bank.keys():
            print("Value: %s ::: Key: %s" % (FC1.url_bank[key], key))

        await FS1.fetch_cycle()


    def test_fetchstarter(self):
        FS1 = FetchStarterSSC()
        listlen = len(FS1.tickerlist)
        FPDB1 = FetchPullDBSSC()
        bankleninit = len(FPDB1.fetchdbpull().keys)
        FS1.fetch_cycle()
        banklenafter = len(FPDB1.fetchdbpull().keys)
        self.assertEqual((bankleninit + listlen), banklenafter, "Something is wrong with FetchStarterSSC")
    """




if __name__ == "__main__":
    unittest.main()













