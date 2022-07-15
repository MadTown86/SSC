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

        pv_tempkeylist = [key for key in vals_data.keys()]
        datadict = val_dict["historical valuation measures"]
        listcollection = []

        keylist = [key for key in vals_data.keys()]

        for indexer in range(len(datadict)):
            listcollection.append([datadict[indexer][key] for key in datadict[indexer].keys()])

        print(listcollection)

        def zipperzip(*args):
            return list(zip(*args))

        newlist = zipperzip(*listcollection)

        dictit = {}

        for indexer in range(len(keylist)):
            dictit[keylist[indexer]] = newlist[indexer]






        FST_SSC = fetchshelfssc_mod.FetchShelfSSC(ticker=ticker, fetchstoreshelf=setpathssc_parsesscval)
        FST_SSC.fetchstore(key=key, idssc=idssc, fetch_data=val_dict, timestampidfs=timestampidpval)
        del FST_SSC