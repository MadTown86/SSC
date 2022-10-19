import shelve
import fetchshelfssc_mod
import dotenv
import os

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv("CORE_DIR_STOR")


class ParseVal:

    """
    Process raw JSON data
    """

    def __init__(self):
        self.setpathssc_parsesscval = ROOT_VAR_SSC + "parsevalshelf"

    def parseval_keys(self):
        with shelve.open(self.setpathssc_parsesscval) as keys_parseval:
            if keys_parseval:
                return [x for x in keys_parseval.keys()]

    def parseval_shelvefetch(self):
        with shelve.open(self.setpathssc_parsesscval) as shelve_parseval:
            if shelve_parseval.keys():
                shelve_copy = dict(shelve_parseval)
                return shelve_copy

    def parse_valpurge(self):
        try:
            with shelve.open(self.setpathssc_parsesscval) as purge_val:
                if purge_val.keys():
                    for key in purge_val.keys():
                        del purge_val[key]
                    if purge_val.keys():
                        return 1
                    else:
                        return 0
        except Exception as er:
            print("Exception in ParseVal: method 'parse_valpurge'")
            print(er)

    def parseval(self, uniquename, pval_rawdata):
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, name_key, idssc, timestampidpval = (
                uniquesplitlist[0],
                uniquesplitlist[1],
                uniquesplitlist[2],
                uniquesplitlist[3],
            )

            vals_data = pval_rawdata
            val_dict = dict(vals_data)

            datadict = val_dict["historical valuation measures"]
            listcollection = []

            keylist = [
                data_key for data_key in datadict[0].keys() if data_key != "Date"
            ]

            for indexer in range(len(datadict)):
                listcollection.append(
                    [
                        datadict[indexer][key]
                        for key in datadict[indexer].keys()
                        if datadict[indexer][key] != "Date"
                    ]
                )

            ziplistcollect = list(map(list, zip(*[line for line in listcollection])))

            keyedlistcollect = {}

            for indexno in range(len(keylist)):
                keyedlistcollect[keylist[indexno]] = ziplistcollect[indexno]

            FST_SSC = fetchshelfssc_mod.FetchShelfSSC(
                fetchstoreshelf=self.setpathssc_parsesscval
            )
            FST_SSC.fetchstore(
                ticker=ticker,
                key=name_key,
                idssc=idssc,
                fetch_data=keyedlistcollect,
                timestampidfs=timestampidpval,
            )
            del FST_SSC
        except Exception as er:
            print("Exception in ParseVal: method 'parseval' ")
            print(er)

    def fetchparseval(self, timestampidpval):
        try:
            with shelve.open(self.setpathssc_parsesscval) as psscval:
                shelfpointerprob = psscval.keys()
                if not bool(shelfpointerprob):
                    psscval.close()
                    return 0
                else:
                    for key in psscval.keys():
                        if timestampidpval in key:
                            retvalpsscval = psscval[key]
                            psscval.close()
                            return retvalpsscval
                        else:
                            continue

        except Exception as Er:
            print("Error: parsevalssc.fetchparseval")
            print(Er)
