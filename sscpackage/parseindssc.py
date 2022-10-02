import shelve
import dictpullssc
import fetchshelfssc_mod
import dotenv
import os
dotenv.load_dotenv(dotenv_path=r'C:\SSC\SimpleStockChecker_REV1\venv\.env')
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')


class ParseIndustry:
    """
    Process 'sector' data to pull stocks industry designation
    """

    def __init__(self):
        self.setpathssc_parsesscind = ROOT_VAR_SSC + "parseindshelf"

    def parse_indpurge(self):
        with shelve.open(self.setpathssc_parsesscind) as purge_ind:
            if purge_ind.keys():
                for key in purge_ind.keys():
                    del purge_ind[key]
                if purge_ind.keys():
                    return 1
                else:
                    return 0

    def parseindustry(self, uniquename, ind_rawdata):
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, key, idssc, timestampidpind = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                                  uniquesplitlist[3]

            DP_SSC = dictpullssc.DictPullSSC()
            secdata = DP_SSC.dictpullssc(ind_rawdata, "Industry")

            FST_SSC = fetchshelfssc_mod.FetchShelfSSC(fetchstoreshelf=self.setpathssc_parsesscind)
            FST_SSC.fetchstore(ticker=ticker, key=key, idssc=idssc, fetch_data=secdata, timestampidfs=timestampidpind)
            del FST_SSC
            del DP_SSC
        except Exception as er:
            print("Exception in ParseIndSSC: method 'parseindustry' ")
            print(er)

    def fetch_parseindustry(self, timestampidpind):
        try:
            with shelve.open(self.setpathssc_parsesscind) as pibank:
                for key in pibank.keys():
                    if timestampidpind in key:
                        pushdata = pibank[key]
                    else:
                        continue

                return pushdata
        except Exception as Er:
            print("Exception: 'fetch_parsebalance'\n")
            print(Er)
