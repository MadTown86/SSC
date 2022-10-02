import shelve
import fetchshelfssc_mod
import dotenv
import os
dotenv.load_dotenv(dotenv_path=r'C:\SSC\SimpleStockChecker_REV1\venv\.env')
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')


class ParseBalance:
    """
    Process raw JSON data for Balance Sheets to prepare for grading algorithm
    """

    def __init__(self):
        self.setpathssc_parsesscpb = ROOT_VAR_SSC + "parsebalanceshelf"

    def parse_shelvepullkeys(self):
        with shelve.open(self.setpathssc_parsesscpb) as svpk:
            if svpk.keys():
                return [x for x in svpk.keys()]

    def parse_balancepurge(self):
        with shelve.open(self.setpathssc_parsesscpb) as purge_bal:
            if purge_bal.keys():
                for key in purge_bal.keys():
                    del purge_bal[key]
                if purge_bal.keys():
                    return 1
                else:
                    return 0
    def parsebalance(self, uniquename: 'str', pb_rawdata: dict) -> None:
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, key, idssc, timestampidpb = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                                uniquesplitlist[3]

            bsheets_data = pb_rawdata

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

            FST_SSC_PB = fetchshelfssc_mod.FetchShelfSSC(fetchstoreshelf=self.setpathssc_parsesscpb)
            FST_SSC_PB.fetchstore(ticker=ticker, key=key, idssc=idssc, fetch_data=bsheets_dict, timestampidfs=timestampidpb)
            del FST_SSC_PB

        except Exception as Er:
            print("Exception in ParseBalance.parsebalance  ::  ")
            print(str(Er))

    def fetch_parsebalance(self, timestampidpb):
        pushdata = {}
        try:
            with shelve.open(self.setpathssc_parsesscpb) as pibank:
                if pibank:
                    for key in pibank.keys():
                        if timestampidpb in key:
                            pushdata = pibank[key]
                        else:
                            continue
                    if pushdata:
                        return pushdata
                    else:
                        return -1

        except Exception as Er:
            print("Exception: 'fetch_parsebalance'")
            print(Er)
