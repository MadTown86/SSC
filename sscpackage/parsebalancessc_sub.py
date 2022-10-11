import parsebalancessc
import dictpullssc
import sscerrors

import dotenv
import os

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv('CORE_DIR_STOR')


class ParseBalance_Sub(parsebalancessc.ParseBalance):
    def __init__(self):
        super().__init__()

    def parsebalance(self, uniquename: 'str', pb_rawdata: dict) -> None:

        try:
            uniquesplitlist = uniquename.split("__")
            ticker, tag, idselfssc, uniquekey = uniquesplitlist[0], uniquesplitlist[1], uniquesplitlist[2], \
                                                uniquesplitlist[3]

            # Converting YH-Finance dataset to pre-existing keys
            key_transferdict = {
                "totalLiab": "Total Liabilities",
                "totalStockholderEquity": "Total Stockholder Equity",
                "otherCurrentLiab": "Other Current Liabilities",
                "totalAssets": "Total Assets",
                "commonStock": "Common Stock",
                "otherCurrentAssets": "Other Current Assets",
                "retainedEarnings": "Retained Earnings",
                "otherLiab": "Other Liabilities",
                "treasuryStock": "Treasury Stock",
                "otherAssets": "Other Assets",
                "cash": "Cash",
                "totalCurrentLiabilities": "Total Current Liabilities",
                "shortLongTermDebt": "Short Long Term Debt",
                "otherStockholderEquity": "Other Stockholder Equity",
                "propertyPlantEquipment": "Property Plant Equipment",
                "totalCurrentAssets": "Total Current Assets",
                "longTermInvestments": "Long Term Investments",
                "netTangibleAssets": "Net Tangible Assets",
                "shortTermInvestments": "Short Term Investments",
                "netReceivables": "Net Receivables",
                "longtermdebt": "Long Term Debt",
                "inventory": "Inventory",
                "accountsPayable": "Accounts Payable"
            }

            DS = dictpullssc.DictPullSSC()
            pulled_balance = DS.dictpullssc(pb_rawdata, "balanceSheetHistory")

            pulled_balance = pulled_balance['balanceSheetStatements']

            output_dict = {}
            if len(pulled_balance) >= 4:
                for key in key_transferdict.keys():
                    temp_list = []
                    if key in pulled_balance[0].keys():
                        temp_list.append(pulled_balance[0][key]['raw'])
                    else:
                        temp_list.append(0)
                    if key in pulled_balance[1].keys():
                        temp_list.append(pulled_balance[1][key]['raw'])
                    else:
                        temp_list.append(0)
                    if key in pulled_balance[2].keys():
                        temp_list.append(pulled_balance[2][key]['raw'])
                    else:
                        temp_list.append(0)
                    if key in pulled_balance[3].keys():
                        temp_list.append(pulled_balance[3][key]['raw'])
                    else:
                        temp_list.append(0)

                    output_dict[key_transferdict[key]] = temp_list
            elif len(pulled_balance) == 3:
                for key in key_transferdict.keys():
                    temp_list = []
                    if key in pulled_balance[0].keys():
                        temp_list.append(pulled_balance[0][key]['raw'])
                    else:
                        temp_list.append(0)
                    if key in pulled_balance[1].keys():
                        temp_list.append(pulled_balance[1][key]['raw'])
                    else:
                        temp_list.append(0)
                    if key in pulled_balance[2].keys():
                        temp_list.append(pulled_balance[2][key]['raw'])
                    else:
                        temp_list.append(0)
            elif len(pulled_balance) == 2:
                for key in key_transferdict.keys():
                    temp_list = []
                    if key in pulled_balance[0].keys():
                        temp_list.append(pulled_balance[0][key]['raw'])
                    else:
                        temp_list.append(0)
                    if key in pulled_balance[1].keys():
                        temp_list.append(pulled_balance[1][key]['raw'])
                    else:
                        temp_list.append(0)
            else:
                # TODO: add ticker to "ticker fail" list and remove from remaining processes
                pass


            fetchstorename = uniquename
            FST_SSC_PB = fetchshelfssc_mod.FetchShelfSSC(fetchstoreshelf=self.setpathssc_parsesscpb)
            FST_SSC_PB.fetchstore(ticker=ticker, fetch_data=output_dict, fetchstorename=fetchstorename)
            del FST_SSC_PB

            print(f'Finished Ticker: {ticker}')

        except Exception as Er:
            print("Exception in ParseBalance.parsebalance  ::  ")
            print(str(Er))


if __name__ == "__main__":
    import fetchshelfssc_mod

    FS = fetchshelfssc_mod.FetchShelfSSC()
    localdb = FS.fetchdbpull()
    bal_keylist = [key for key in FS.fetchdbpull().keys() if "url_balance" in key]
    PS = ParseBalance_Sub()

    for key in bal_keylist:
        print(key)

    for key in bal_keylist:
        PS.parsebalance(key, localdb[key])

    uniquetimestampbin = []
    for key in bal_keylist:
        ticker, var1, var2, uniqueid = key.split("__")
        print(ticker)
        print(uniqueid)
        uniquetimestampbin.append(uniqueid)

    fetchbin = []
    for uniqueid in uniquetimestampbin:
        PS.fetch_parsebalance(uniqueid)

    if fetchbin:
        for key, value in fetchbin[0].items():
            print(f'KEY:::{key} >>>>> VALUE:::: {value}')
