import json
import fetchshelfssc_mod
import shelve
import dictpullssc

class ParseAr:
    """
    Process raw JSON data for upgrades-downgrades for grading algorithm
    """
    def __init__(self):
        self.setpathssc_parsesscar= r"C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parsearshelf"

    def parsear(self, uniquename, par_rawdata):
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, key, idssc, timestampidar = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                                uniquesplitlist[3]
            DPssc = dictpullssc.DictPullSSC()
            ardict = DPssc.dictpullssc(par_rawdata, "history")

            FST_SSC = fetchshelfssc_mod.FetchShelfSSC(ticker=ticker, fetchstoreshelf=self.setpathssc_parsesscar)
            FST_SSC.fetchstore(key=key, idssc=idssc, fetch_data=ardict, timestampidfs=timestampidar)
            del FST_SSC
        except Exception as Er:
            print("Exception in parsearssc.ParseAr.parsear")
            print(Er)

    def fetch_parsear(self, timestampidar):
        try:
            with shelve.open(self.setpathssc_parsesscar) as pibank:
                for key in pibank.keys():
                    if timestampidar in key:
                        pushdata = pibank[key]
                    else:
                        continue
                return pushdata

        except Exception as Er:
            print("Exception: 'fetch_parsebalance'\n")
            print(Er)
