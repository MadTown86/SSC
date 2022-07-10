import dictpullssc
import json
import fetchshelfssc_mod
import shelve


class ParseSector:
    """
    Process raw JSON data for Sector to prepare for grading algorithm
    """

    def __init__(self):
        self.setpathssc_parsesscsec = r"C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parsesecshelf"

    def parsesector(self, uniquename, ps_rawdata):
        uniquesplitlist = uniquename.split("__")
        ticker, key, idssc, timestampidpsec = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                              uniquesplitlist[3]


        DP_SSCPSEC = dictpullssc.DictPullSSC()
        secdata = DP_SSCPSEC.dictpullssc(json.loads(ps_rawdata), "Sector")

        FST_SSC = fetchshelfssc_mod.FetchShelfSSC(ticker=ticker, fetchstoreshelf=self.setpathssc_parsesscsec)
        FST_SSC.fetchstore(key=key, idssc=idssc, fetch_data=secdata, timestampidfs=timestampidpsec)
        del FST_SSC
        del DP_SSCPSEC

    def fetch_parsesector(self, timestampidpsec):
        try:
            with shelve.open(self.setpathssc_parsesscsec) as pibank:
                for key in pibank.keys():
                    if timestampidpsec in key:
                        pushdata = pibank[key]
                    else:
                        continue

                return pushdata
        except Exception as Er:
            print("Exception: 'fetch_parsebalance'\n")
            print(Er)