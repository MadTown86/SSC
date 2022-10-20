import sscpackage.parsevalssc
import fetchshelfssc_mod
import dictpullssc


class ParseValSSC_Sub(sscpackage.parsevalssc.ParseVal):
    def __init__(self):
        super().__init__()

    def parseval(self, uniquename, pval_rawdata):
        try:
            uniquesplitlist = uniquename.split("__")
            ticker, name_key, idssc, timestampidpval = (
                uniquesplitlist[0],
                uniquesplitlist[1],
                uniquesplitlist[2],
                uniquesplitlist[3],
            )

            local_json = pval_rawdata["timeSeries"]

            keybin_transfer = {
                "quarterlyMarketCap": "Market Cap (intraday)",
                "quarterlyPeRatio": "Trailing P/E",
                "quarterlyForwardPeRatio": "Forward P/E",
                "quarterlyPegRatio": "PEG Ratio (5 yr expected)",
                "quarterlyPsRatio": "Price/Sales (ttm)",
                "quarterlyPbRatio": "Price/Book (mrq)",
                "quarterlyEnterprisesValueRevenueRatio": "Enterprise Value/Revenue",
                "quarterlyEnterprisesValueEBITDARatio": "Enterprise Value/EBITDA",
            }

            output_dict_parseval = {}

            DS = dictpullssc.DictPullSSC()

            for key in keybin_transfer.keys():
                output_list = []
                temp_pulledlist = DS.dictpullssc(local_json, key)
                if temp_pulledlist:
                    for dictionary in temp_pulledlist:
                        tval = DS.dictpullssc(dictionary, 'raw')
                        if tval:
                            output_list.append(tval)
                        else:
                            output_list.append(0)
                    output_dict_parseval[keybin_transfer[key]] = output_list

            fetchstorename = uniquename
            FST_SSC = fetchshelfssc_mod.FetchShelfSSC(
                fetchstoreshelf=self.setpathssc_parsesscval
            )
            FST_SSC.fetchstore(
                ticker=ticker,
                fetchstorename=fetchstorename,
                fetch_data=output_dict_parseval,
            )
            del FST_SSC

            print(f'Finished: {ticker}')

        except Exception as er:
            print("Exception in ParseVal: method 'parseval' ")
            print(er)

if __name__ == "__main__":
    import fetchshelfssc_mod
    import dictpullssc

    FS = fetchshelfssc_mod.FetchShelfSSC()
    DS = dictpullssc.DictPullSSC()


    local_db = FS.fetchdbpull()
    keylist = [x for x in local_db.keys() if 'val' in x]
    test_key = keylist[0]

    temp_dictpart = DS.dictpullssc(local_db[test_key], 'quarterlyForwardPeRatio')

    PVAL = ParseValSSC_Sub()
    PVAL.parseval(test_key, local_db[test_key])
