import shelve
import dictpullssc
import fetchshelfssc_mod

import dotenv
import os

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv("CORE_DIR_STOR")


class ParseSector:
    """
    Process raw JSON data for Sector to prepare for grading algorithm
    """

    def __init__(self):
        self.setpathssc_parsesscsec = ROOT_VAR_SSC + "parsesecshelf"

    def parse_sectpurge(self):
        try:
            with shelve.open(self.setpathssc_parsesscsec) as purge_sec:
                if purge_sec.keys():
                    for key in purge_sec.keys():
                        del purge_sec[key]
                    if purge_sec.keys():
                        return 1
                    else:
                        return 0
        except Exception as er:
            print("Exception in ParseSector: method 'parse_sectpurge' ")
            print(er)

    def parsesector(self, uniquename, ps_rawdata):
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, key, idssc, timestampidpsec = (
                uniquesplitlist[0],
                uniquesplitlist[1],
                uniquesplitlist[2],
                uniquesplitlist[3],
            )

            DP_SSCPSEC = dictpullssc.DictPullSSC()
            secdata = DP_SSCPSEC.dictpullssc(ps_rawdata, "Sector")

            FST_SSC = fetchshelfssc_mod.FetchShelfSSC(
                fetchstoreshelf=self.setpathssc_parsesscsec
            )
            FST_SSC.fetchstore(
                ticker=ticker,
                key=key,
                idssc=idssc,
                fetch_data=secdata,
                timestampidfs=timestampidpsec,
            )
            del FST_SSC
            del DP_SSCPSEC
        except Exception as er:
            print("Exception in ParseSector: method 'parsesector' ")
            print(er)

    def fetch_parsesector(self, timestampidpsec):
        try:
            with shelve.open(self.setpathssc_parsesscsec) as pibank:
                for key in pibank.keys():
                    if timestampidpsec in key:
                        pushdata = pibank[key]
                    else:
                        continue

                return pushdata
        except Exception as Er:
            print("Exception: 'fetch_parsebalance'\n")
            print(Er)
