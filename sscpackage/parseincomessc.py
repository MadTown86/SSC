import json
import fetchshelfssc_mod
import shelve


class ParseIncome:
    """
    Class for parseincome, in case API format changes and needs to be altered in the future, use inheritance without
    breaking application
    """
    def __init__(self):
        self.setpathssc_parsessc = r"C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parseincomeshelf"

    def parseincome(self, uniquename: 'str', pi_rawdata: 'json') -> None:
        """
        Converts raw json string to usable format for grading purposes

        :param uniquename: String from fetchlog, acts as key for fetchshelf
        :param pi_rawdata: url_income fetch data from shelve
        :return: None
        """
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, key, idssc, timestampidpi = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                                uniquesplitlist[3]

            isheets_data = pi_rawdata

            isheets_zip = list(
                zip(
                    [isheets_data["annual_historical_income_statements"][0][keys] for keys in
                     isheets_data["annual_historical_income_statements"][0]],
                    [isheets_data["annual_historical_income_statements"][1][keys] for keys in
                     isheets_data["annual_historical_income_statements"][1]],
                    [isheets_data["annual_historical_income_statements"][2][keys] for keys in
                     isheets_data["annual_historical_income_statements"][2]],
                    [isheets_data["annual_historical_income_statements"][3][keys] for keys in
                     isheets_data["annual_historical_income_statements"][3]],
                )
            )

            isheets_keys = [key for key in isheets_data["annual_historical_income_statements"][0]]

            isheets_dict = {}
            for x in range(len(isheets_keys)):
                isheets_dict[isheets_keys[x]] =isheets_zip[x]

            FST_SSC = fetchshelfssc_mod.FetchShelfSSC(ticker=ticker, fetchstoreshelf=self.setpathssc_parsessc)
            FST_SSC.fetchstore(key=key, idssc=idssc, fetch_data=isheets_dict, timestampidfs=timestampidpi)
            del FST_SSC

        except Exception as Er:
            print("Exception in 'ParseIncome.parseincome'  ::  ")
            print(str(Er))

    def fetch_parseincome(self, timestampidpi):
        try:
            with shelve.open(self.setpathssc_parsessc) as pibank:
                for key in pibank.keys():
                    if timestampidpi in key:
                        pushdata = pibank[key]
                    else:
                        continue

                return pushdata
        except Exception as Er:
            print("Exception: 'fetch_parseincome'\n")
            print(Er)