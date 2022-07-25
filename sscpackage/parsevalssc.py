import json
import fetchshelfssc_mod
import shelve
import shelfpeekssc



class ParseVal:
    """
    Process raw JSON data
    """
    def __init__(self):
        self.setpathssc_parsesscval = r"C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parsevalshelf"

    def parseval(self, uniquename, pval_rawdata):

        uniquesplitlist = uniquename.split("__")
        ticker, name_key, idssc, timestampidpval = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                              uniquesplitlist[3]

        vals_data = pval_rawdata
        val_dict = dict(vals_data)

        datadict = val_dict["historical valuation measures"]
        listcollection = []

        keylist = [data_key for data_key in datadict[0].keys()]

        for indexer in range(len(datadict)):
            listcollection.append([datadict[indexer][key] for key in datadict[indexer].keys()])

        ziplistcollect = list(map(list, zip(*[line for line in listcollection])))

        keyedlistcollect = {}

        for indexno in range(len(keylist)):
            keyedlistcollect[keylist[indexno]] = ziplistcollect[indexno]

        FST_SSC = fetchshelfssc_mod.FetchShelfSSC(ticker=ticker, fetchstoreshelf=self.setpathssc_parsesscval)
        FST_SSC.fetchstore(key=name_key, idssc=idssc, fetch_data=keyedlistcollect, timestampidfs=timestampidpval)
        del FST_SSC

    def fetchparseval(self, timestampidpval):
        try:
            with shelve.open(self.setpathssc_parsesscval) as psscval:
                if psscval.keys():
                    for fetchparseval_key in psscval.keys():
                        if timestampidpval in fetchparseval_key:
                            return dict(psscval[fetchparseval_key])
                        else:
                            return 0
                else:
                    return 0

        except Exception as Er:
            print("Error: parsevalssc.fetchparseval")
            print(Er)


