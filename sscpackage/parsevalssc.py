import json
import fetchshelfssc_mod


class ParseVal:
    """
    Process raw JSON data
    """

    def parseval(self, uniquename, pval_rawdata):
        uniquesplitlist = uniquename.split("__")
        ticker, key, idssc, timestampidpval = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                              uniquesplitlist[3]

        setpathssc_parsesscval = r"C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parsevalshelf"

        vals_data = json.loads(pval_rawdata)
        val_dict = dict(vals_data)

        FST_SSC = fetchshelfssc_mod.FetchShelfSSC(ticker=ticker, fetchstoreshelf=setpathssc_parsesscval)
        FST_SSC.fetchstore(key=key, idssc=idssc, fetch_data=val_dict, timestampidfs=timestampidpval)
        del FST_SSC