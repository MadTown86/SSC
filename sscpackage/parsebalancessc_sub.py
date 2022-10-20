"""
GD - 10/19/2022 - Unit Test Success
"""

import parsebalancessc
import fetchshelfssc_mod
import dictpullssc
import fetchssc
import dotenv
import os

dotenv.load_dotenv(dotenv_path=os.getenv("LO_ROOT"))
ROOT_VAR_SSC = os.getenv("CORE_DIR_STOR")


def incbal_reformat(uniquename: str, jsonmix: [{}], transferbin: {}) -> dict:
    # TODO: add error handling
    output_dict = {}
    if len(jsonmix) >= 4:
        if jsonmix[0].keys():
            for key in transferbin.keys():
                temp_list = []
                if key in jsonmix[0].keys():
                    if jsonmix[0][key]:
                        temp_list.append(jsonmix[0][key]["raw"])
                    else:
                        temp_list.append(0)
                else:
                    temp_list.append(0)
                if key in jsonmix[1].keys():
                    if jsonmix[1][key]:
                        temp_list.append(jsonmix[1][key]["raw"])
                    else:
                        temp_list.append(0)
                else:
                    temp_list.append(0)
                if key in jsonmix[2].keys():
                    if jsonmix[2][key]:
                        temp_list.append(jsonmix[2][key]["raw"])
                    else:
                        temp_list.append(0)
                else:
                    temp_list.append(0)
                if key in jsonmix[3].keys():
                    if jsonmix[3][key]:
                        temp_list.append(jsonmix[3][key]["raw"])
                    else:
                        temp_list.append(0)
                else:
                    temp_list.append(0)

                output_dict[transferbin[key]] = temp_list
    elif len(jsonmix) == 3:
        if jsonmix[0].keys():
            for key in transferbin.keys():
                temp_list = []
                if key in jsonmix[0].keys():
                    if jsonmix[0][key]:
                        temp_list.append(jsonmix[0][key]["raw"])
                    else:
                        temp_list.append(0)
                else:
                    temp_list.append(0)
                if key in jsonmix[1].keys():
                    if jsonmix[1][key]:
                        temp_list.append(jsonmix[1][key]["raw"])
                    else:
                        temp_list.append(0)
                else:
                    temp_list.append(0)
                if key in jsonmix[2].keys():
                    if jsonmix[2][key]:
                        temp_list.append(jsonmix[2][key]["raw"])
                    else:
                        temp_list.append(0)
                else:
                    temp_list.append(0)

                output_dict[transferbin[key]] = temp_list
    elif len(jsonmix) == 2:
        if jsonmix[0].keys():
            for key in transferbin.keys():
                temp_list = []
                if key in jsonmix[0].keys():
                    if jsonmix[0][key]:
                        temp_list.append(jsonmix[0][key]["raw"])
                    else:
                        temp_list.append(0)
                else:
                    temp_list.append(0)
                if key in jsonmix[1].keys():
                    if jsonmix[1][key]:
                        temp_list.append(jsonmix[1][key]["raw"])
                    else:
                        temp_list.append(0)
                else:
                    temp_list.append(0)

                output_dict[transferbin[key]] = temp_list
    else:
        print("IN THE ELSE YOU WANT")
        fetchssc.FetchSSC().ticker_fail(fetchname=uniquename)
        # TODO: add ticker to "ticker fail" list and remove from remaining processes
        pass

    return output_dict


class ParseBalance_Sub(parsebalancessc.ParseBalance):
    def __init__(self):
        super().__init__()

    def parsebalance(self, uniquename: "str", pb_rawdata: dict) -> None:

        try:
            ticker, tag, idselfssc, uniquekey = uniquename.split("__")

            # Converting YH-Finance dataset to pre-existing keys
            transferbin = {
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
                "accountsPayable": "Accounts Payable",
            }

            DS = dictpullssc.DictPullSSC()

            dpssc_balance = DS.dictpullssc(pb_rawdata, "balanceSheetHistory")

            inner_balance = dpssc_balance["balanceSheetStatements"]

            data_output = incbal_reformat(uniquename, inner_balance, transferbin)

            fetchstorename = uniquename

            FST_SSC_PB = fetchshelfssc_mod.FetchShelfSSC(
                fetchstoreshelf=self.setpathssc_parsesscpb
            )
            FST_SSC_PB.fetchstore(
                ticker=ticker, fetch_data=data_output, fetchstorename=fetchstorename
            )
            del FST_SSC_PB

            print(f"Finished Ticker: {ticker}")

        except Exception as Er:
            print("Exception in ParseBalance.parsebalance  ::  ")
            print(str(Er))


if __name__ == "__main__":

    tempkeylist = ['MSFT__url_balance__1556069093072__bX6sOpMaQ1UaYNX',
                   'AMD__url_balance__1556069093008__4m0z80meXcuzk7l',
                   'NVDA__url_balance__1556069093200__HZLqG4SgOsjWivO',
                   'HOOD__url_balance__1556069093328__1apU5YmeN8CwQkW',
                   'AAPL__url_balance__1556069093520__a9q6bZrBpdTCaTc',
                   'META__url_balance__1556065592464__u0sCyHUlnfHOcVG']

    transferbin = {
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
        "accountsPayable": "Accounts Payable",
    }


    import fetchshelfssc_mod

    FS = fetchshelfssc_mod.FetchShelfSSC()
    localdb = FS.fetchdbpull()
    bal_key = tempkeylist[0]
    ticker, tag, uniqid, selfid = bal_key.split("__")
    DS = dictpullssc.DictPullSSC()
    jsonmix = DS.dictpullssc(localdb[bal_key], "balanceSheetHistory")
    jsonmix = jsonmix['balanceSheetStatements']

    if localdb:
        if localdb[bal_key]:
            if localdb[bal_key].keys():
                samp = incbal_reformat("TEST", jsonmix=jsonmix, transferbin=transferbin)

    PB = ParseBalance_Sub()
    PB.parsebalance(bal_key, localdb[bal_key])
