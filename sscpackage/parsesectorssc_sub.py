"""
Subclass of parsesectorssc.ParseSec - to account for change in API
"""
import sscpackage.parsesectorssc
import dictpullssc
import fetchshelfssc_mod


class ParseSec_Sub(sscpackage.parsesectorssc.ParseSector):
    def __init__(self):
        super().__init__()

    def parsesector(self, uniquename, ps_rawdata):
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, key, idssc, timestampidpsec = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                                  uniquesplitlist[3]

            DP_SSCPSEC = dictpullssc.DictPullSSC()
            secdata = DP_SSCPSEC.dictpullssc(ps_rawdata, "sector")


            fetchstorename = uniquename
            FST_SSC = fetchshelfssc_mod.FetchShelfSSC(fetchstoreshelf=self.setpathssc_parsesscsec)
            FST_SSC.fetchstore(ticker=ticker, fetchstorename=fetchstorename, fetch_data=secdata)
            del FST_SSC
            del DP_SSCPSEC
        except Exception as er:
            print("Exception in ParseSector: method 'parsesector' ")
            print(er)