class ParseSector:
    """
    Process raw JSON data for Sector to prepare for grading algorithm
    """

    def parsesector(self, uniquename, ps_rawdata):
        uniquesplitlist = uniquename.split("__")
        ticker, key, idssc, timestampidpsec = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                              uniquesplitlist[3]

        setpathssc_parsesscsec = r"C:\SSC\SimpleStockChecker_REV1\sscpackage\storage\parsesecshelf"

        DP_SSC = dictpullssc.DictPullSSC()
        secdata = DP_SSC.dictpullssc(json.loads(ps_rawdata), "Sector")

        FST_SSC = fetchshelfssc_mod.FetchShelfSSC(ticker=ticker, fetchstoreshelf=setpathssc_parsesscsec)
        FST_SSC.fetchstore(key=key, idssc=idssc, fetch_data=secdata, timestampidfs=timestampidpsec)
        del FST_SSC
        del DP_SSC