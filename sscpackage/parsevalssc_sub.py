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
                "quarterlyforwardPeRatio": "Forward P/E",
                "quarterlyPegRatio": "PEG Ratio (5 yr expected)",
                "quarterlyPsRatio": "Price/Sales (ttm)",
                "quarterlyPbRatio": "Price/Book (mrq)",
                "quarterlyEnterprisesValueRevenueRatio": "Enterprise Value/Revenue",
                "quarterlyEnterprisesValueEBITDARatio": "Enterprise Value/EBITDA",
            }

            output_dict_parseval = {}

            for key in keybin_transfer.keys():
                print(key)
                temp_list = []
                if key in local_json.keys():
                    print([key for key in local_json.keys()])
                    print(local_json[key])
                    print(type(local_json[key]))
                    for indexno in range(len(local_json[key])):
                        local_copy1 = local_json[key]
                        local_copy2 = local_copy1[indexno]
                        # local_copy3

                        print(f'ITEM VALUE: {local_copy2["raw"]}')
                        temp_list.append(local_json[key][indexno]["raw"])
                        print(f"TEMP LIST CONTENTS: {temp_list}")
                    output_dict_parseval[keybin_transfer[key]] = temp_list

            for key, value in output_dict_parseval.items():
                print(f"KEY:::{key} >>> VALUE::: {value}")

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
        except Exception as er:
            print("Exception in ParseVal: method 'parseval' ")
            print(er)
