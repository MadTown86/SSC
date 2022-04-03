import json
import requests
import os
import sys
"""
2/4/22 - GD

ssc_ft is a module that houses the scripts for querying data from RapidAPI and writing it to file for use in ssc_pt
"""
global prog_time
prog_time = None

"""
This is to test branch functionality GIT/Pycharm
"""


def get_financials(ticker_entry: "string" = "MSFT"):
    import time

    # A function attribute to allow ticker_entry value to be pulled after import into other module
    get_financials.ticker_entryf = ticker_entry

    """
    2/4/22 - GD
    This function receives the ticker symbol from SSC_GUI that is user input

    It uses this ticker symbol as a variable for fetching data from RapidAPI.

    It parses the data from raw response bytestring to python dict, then stores the python dict as JSON

    :param ticker_entry: this is the ticker symbol that was qualified from SSC_GUI
    :return: no returns
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
    querystring = {"ticker_symbol": ticker_entry, "format": "json"}
    querystring2 = {"symbol": ticker_entry, "region": "US"}
    querystring3 = {"ticker_symbol": ticker_entry, "format": "json"}
    querystring4 = {"ticker_symbol": ticker_entry}

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

    response = requests.request("GET", url_income, headers=headers, params=querystring) # Request data for url_income
    if response.status_code == 200:  # If received 'all good' response from API for first request, continue
        res_direct = response.text  # Used as a function attribute in ssc_gui to pass into log_entry
        fetch_data = dict(json.loads(response.text))
        print("In first fetch")

        with open("incomestatements.json", 'w') as income_statements:
            income_statements.truncate()
            json.dump(fetch_data, income_statements, indent=5, separators=(", ", ": "), sort_keys=False)
            income_statements.close()

        response_balance = requests.request("GET", url_balance, headers=headers, params=querystring)  # fetch for url_bal
        if response_balance.status_code == 200:  # If received 'all good' continue
            rb_data = dict(json.loads(response_balance.text))
            print("In second fetch")

            with open("balancesheets.json", 'w') as balance_sheets:
                balance_sheets.truncate()
                json.dump(rb_data, balance_sheets, indent=5, separators=(", ", ": "), sort_keys=False)
                balance_sheets.close()

            response_ar = requests.request("GET", url_ar, headers=headers_ar, params=querystring2) # Fetch url_ar
            if response_ar.status_code == 200:  # if received 'all good' start to reformat data
                ar_data = dict(json.loads(response_ar.text))
                print("In third fetch")

                with open("ardata.json", 'w') as ar_sheets:
                    ar_sheets.truncate()
                    json.dump(ar_data, ar_sheets, indent=5, separators=(", ", ": "), sort_keys=False)
                    ar_sheets.close()

                response_val = requests.request("GET", url_val, headers=headers, params=querystring3) #Fetch  valuation
                if response_val.status_code == 200:
                    val_data = dict(json.loads(response_val.text))
                    print("In fourth fetch")

                    with open("valdata.json", 'w') as val_sheets:
                        val_sheets.truncate()
                        json.dump(val_data, val_sheets, indent=5, separators=(", ", ": "), sort_keys=False)
                        val_sheets.close()

                    response_sector = requests.request("GET", url_sectordata, headers=headers, params=querystring4)
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
class RapidFetcher:
"""

# This class is built to fetch the data from rapid api and store it for use in the grading system and elsewhere

"""
def __init__(self, ticker="MSFT", urlarg, queryarg, headersarg, storename):
    self.ticker = ticker
    self.urlarg = urlarg
    self.queryarg = queryarg
    self.headerasarg = headersarg
    self.storename = storename

def fetch_dataRAPI(self, typerit):
    if typerit == "income":
        pass
"""