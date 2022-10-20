"""
Subclass of ParseIndustry - due to change in API source from Stock Market Data by Lattice
to YH Finance
"""
import dictpullssc
import fetchshelfssc_mod
import parseindssc
import sscerrors


class ParseIndustry_Sub(parseindssc.ParseIndustry):
    def __init__(self):
        super().__init__()

    def parseindustry(self, uniquename, ind_rawdata):
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, key, idssc, timestampidpind = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                                  uniquesplitlist[3]

            DP_SSC = dictpullssc.DictPullSSC()
            secdata = DP_SSC.dictpullssc(ind_rawdata, "Industry")
            if not secdata:
                secdata = DP_SSC.dictpullssc(ind_rawdata, 'industry')

            try:
                sscerrors.gotmilk(secdata)
            except sscerrors.GotNoMilk as er:
                print(er)

            fetchstorename = uniquename
            FST_SSC = fetchshelfssc_mod.FetchShelfSSC(fetchstoreshelf=self.setpathssc_parsesscind)
            FST_SSC.fetchstore(ticker=ticker, fetchstorename=fetchstorename, fetch_data=secdata)
            del FST_SSC
            del DP_SSC
        except Exception as er:
            print("Exception in ParseIndSSC: method 'parseindustry' ")
            print(er)