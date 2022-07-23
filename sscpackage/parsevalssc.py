import json
import fetchshelfssc_mod
import shelve


class ParseVal:
    """
    Process raw JSON data
    """
    def __init__(self):
        self.setpathssc_parsesscval = r"C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parsevalshelf"

    def parseval(self, uniquename, pval_rawdata):
        uniquesplitlist = uniquename.split("__")
        ticker, key, idssc, timestampidpval = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                              uniquesplitlist[3]

        vals_data = json.loads(pval_rawdata)
        val_dict = dict(vals_data)

        datadict = val_dict["historical valuation measures"]
        listcollection = []

        keylist = [key for key in vals_data.keys()]

        for indexer in range(len(datadict)):
            listcollection.append([datadict[indexer][key] for key in datadict[indexer].keys()])

        ziplistcollect = list(zip(*[line for line in listcollection]))

        keyedlistcollect = {}

        for indexno in range(len(keylist)):
            keyedlistcollect[keylist[indexno]] = ziplistcollect[indexno]

        FST_SSC = fetchshelfssc_mod.FetchShelfSSC(ticker=ticker, fetchstoreshelf=self.setpathssc_parsesscval)
        FST_SSC.fetchstore(key=key, idssc=idssc, fetch_data=keyedlistcollect, timestampidfs=timestampidpval)
        del FST_SSC

    def fetchparseval(self, timestampidpval):
        try:
            with shelve.open(self.setpathssc_parsesscval) as psscval:
                if timestampidpval in psscval.keys():
                    return psscval[timestampidpval]
                else:
                    return 0

        except Exception as Er:
            print("Error: parsevalssc.fetchparseval")
            print(Er)


