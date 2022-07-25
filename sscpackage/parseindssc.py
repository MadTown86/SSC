import dictpullssc
import json
import fetchshelfssc_mod
import shelve


class ParseIndustry:
    """
    Process 'sector' data to pull stocks industry designation
    """
    def __init__(self):
        self.setpathssc_parsesscind = r"C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parseindshelf"

    def parseindustry(self, uniquename, ind_rawdata):

        uniquesplitlist = uniquename.split("__")
        ticker, key, idssc, timestampidpind = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                              uniquesplitlist[3]

        DP_SSC = dictpullssc.DictPullSSC()
        secdata = DP_SSC.dictpullssc(ind_rawdata, "Industry")

        FST_SSC = fetchshelfssc_mod.FetchShelfSSC(ticker=ticker, fetchstoreshelf=self.setpathssc_parsesscind)
        FST_SSC.fetchstore(key=key, idssc=idssc, fetch_data=secdata, timestampidfs=timestampidpind)
        del FST_SSC
        del DP_SSC

    def fetch_parseindustry(self, timestampidpind):
        try:
            with shelve.open(self.setpathssc_parsesscind) as pibank:
                for key in pibank.keys():
                    if timestampidpind in key:
                        pushdata = pibank[key]
                    else:
                        continue

                return pushdata
        except Exception as Er:
            print("Exception: 'fetch_parsebalance'\n")
            print(Er)
