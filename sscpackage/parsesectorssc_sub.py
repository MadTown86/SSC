"""
Subclass of parsesectorssc.ParseSec - to account for change in API
"""
import sscpackage.parsesectorssc
import dictpullssc
import fetchshelfssc_mod


class ParseSec_Sub(sscpackage.parsesectorssc.ParseSector):
    def __init__(self):
        super().__init__()

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
            secdata = DP_SSCPSEC.dictpullssc(ps_rawdata, "sector")

            fetchstorename = uniquename
            FST_SSC = fetchshelfssc_mod.FetchShelfSSC(
                fetchstoreshelf=self.setpathssc_parsesscsec
            )
            FST_SSC.fetchstore(
                ticker=ticker, fetchstorename=fetchstorename, fetch_data=secdata
            )
            del FST_SSC
            del DP_SSCPSEC
            print(secdata)
            print(f'Finished ticker:: {ticker}')
        except Exception as er:
            print("Exception in ParseSector: method 'parsesector' ")
            print(er)

if __name__ == "__main__":
    import fetchshelfssc_mod
    import dictpullssc

    FS = fetchshelfssc_mod.FetchShelfSSC()
    DS = dictpullssc.DictPullSSC()
    PSEC = ParseSec_Sub()

    local_db = FS.fetchdbpull()
    keylist = [x for x in local_db.keys() if "sector" in x]
    test_key = keylist[0]
    test_output = DS.dictpullssc(local_db[test_key], 'sector')

    PSEC.parsesector(test_key, local_db[test_key])
