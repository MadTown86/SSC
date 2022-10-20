import shelve
import dictpullssc
import fetchshelfssc_mod

import dotenv
import os

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv("CORE_DIR_STOR")


class ParseAr:
    """
    Process raw JSON data for upgrades-downgrades for grading algorithm
    """

    def __init__(self):
        self.setpathssc_parsesscar = ROOT_VAR_SSC + "parsearshelf"

    def purge_parsear(self):
        try:
            with shelve.open(self.setpathssc_parsesscar) as purge_parse:
                if purge_parse.keys():
                    for item in purge_parse.keys():
                        del purge_parse[item]
                    if purge_parse.keys():
                        return 1
                    else:
                        return 0
        except Exception as er:
            print("Exception in ParseAr: method 'purge_parsear' ")
            print(er)

    def parsear(self, uniquename, par_rawdata):
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, key, idssc, timestampidar = uniquename.split("__")

            DPssc = dictpullssc.DictPullSSC()
            ardict = DPssc.dictpullssc(par_rawdata, "history")

            FST_SSC = fetchshelfssc_mod.FetchShelfSSC(
                fetchstoreshelf=self.setpathssc_parsesscar
            )

            fetchstorename = uniquename

            FST_SSC.fetchstore(
                ticker=ticker,
                fetchstorename=fetchstorename,
                fetch_data=ardict,
            )
            del FST_SSC

            print(f"Finished Ticker: {ticker}")

        except Exception as Er:
            print("Exception in parsearssc.ParseAr.parsear")
            print(Er)

    def fetch_parsear(self, timestampidar):
        try:
            with shelve.open(self.setpathssc_parsesscar) as pibank:
                # TODO: look into this, maybe change looping structure, timestamidar in pibank.keys(), no for loop
                for key in pibank.keys():
                    if timestampidar in key:
                        pushdata = pibank[key]
                    else:
                        continue
                return pushdata

        except Exception as Er:
            print("Exception: 'fetch_parsebalance'\n")
            print(Er)


if __name__ == "__main__":
    import fetchshelfssc_mod
    import dictpullssc

    FS = fetchshelfssc_mod.FetchShelfSSC()
    DS = dictpullssc.DictPullSSC()

    local_db = FS.fetchdbpull()
    keylist = [x for x in local_db.keys() if "ar" in x]
    ar_key = keylist[0]

    PS = ParseAr()
    PS.parsear(ar_key, local_db[ar_key])
