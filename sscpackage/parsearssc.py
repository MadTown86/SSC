import json
import fetchshelfssc_mod

class ParseAr:
    """
    Process raw JSON data for upgrades-downgrades for grading algorithm
    """

    def parsear(self, uniquename, par_rawdata):
        uniquesplitlist = uniquename.split("__")
        ticker, key, idssc, timestampidar = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                            uniquesplitlist[3]
        setpathssc_parsesscar = r"C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parsearshelf"

        ardict = dict(json.loads(par_rawdata))

        FST_SSC = fetchshelfssc_mod.FetchShelfSSC(ticker=ticker, fetchstoreshelf=setpathssc_parsesscar)
        FST_SSC.fetchstore(key=key, idssc=idssc, fetch_data=ardict, timestampidfs=timestampidar)
        del FST_SSC
