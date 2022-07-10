import json
import fetchshelfssc_mod
import shelve

class ParseBalance:
    """
    Process raw JSON data for Balance Sheets to prepare for grading algorithm
    """
    def __init__(self):
        self.setpathssc_parsesscpb = r"C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parsebalanceshelf"

    def parsebalance(self, uniquename: 'str', pb_rawdata: 'json') -> None:
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, key, idssc, timestampidpb = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                                uniquesplitlist[3]

            setpathssc_parsesscpb = r"C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parsebalanceshelf"

            bsheets_data = json.loads(pb_rawdata)

            bsheets_zip = list(
                zip(
                    [bsheets_data["annual_historical_balance_sheets"][0][keys] for keys in
                     bsheets_data["annual_historical_balance_sheets"][0]],
                    [bsheets_data["annual_historical_balance_sheets"][1][keys] for keys in
                     bsheets_data["annual_historical_balance_sheets"][1]],
                    [bsheets_data["annual_historical_balance_sheets"][2][keys] for keys in
                     bsheets_data["annual_historical_balance_sheets"][2]],
                    [bsheets_data["annual_historical_balance_sheets"][3][keys] for keys in
                     bsheets_data["annual_historical_balance_sheets"][3]],
                )
            )

            bsheets_keys = [key for key in bsheets_data["annual_historical_balance_sheets"][0]]
            bsheets_dict = {}
            for x in range(len(bsheets_keys)):
                bsheets_dict[bsheets_keys[x]] = bsheets_zip[x]

            FST_SSC_PB = fetchshelfssc_mod.FetchShelfSSC(ticker=ticker, fetchstoreshelf=self.setpathssc_parsesscpb)
            FST_SSC_PB.fetchstore(key=key, idssc=idssc, fetch_data=bsheets_dict, timestampidfs=timestampidpb)
            del FST_SSC_PB

        except Exception as Er:
            print("Exception in ParseBalance.parsebalance  ::  ")
            print(str(Er))

    def fetch_parsebalance(self, timestampidpb):
        try:
            with shelve.open(self.setpathssc_parsesscpb) as pibank:
                for key in pibank.keys():
                    if timestampidpb in key:
                        pushdata = pibank[key]
                    else:
                        continue

                return pushdata
        except Exception as Er:
            print("Exception: 'fetch_parsebalance'\n")
            print(Er)