import dictpullssc
import json
import fetchshelfssc_mod


class ParseIndustry:
    """
    Process 'sector' data to pull stocks industry designation
    """

    def parseindustry(self, uniquename, ind_rawdata):

        uniquesplitlist = uniquename.split("__")
        ticker, key, idssc, timestampidpind = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                              uniquesplitlist[3]

        setpathssc_parsesscind = r"C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parseindshelf"

        DP_SSC = dictpullssc.DictPullSSC()
        secdata = DP_SSC.dictpullssc(json.loads(ind_rawdata), "Industry")

        FST_SSC = fetchshelfssc_mod.FetchShelfSSC(ticker=ticker, fetchstoreshelf=setpathssc_parsesscind)
        FST_SSC.fetchstore(key=key, idssc=idssc, fetch_data=secdata, timestampidfs=timestampidpind)
        del FST_SSC
        del DP_SSC